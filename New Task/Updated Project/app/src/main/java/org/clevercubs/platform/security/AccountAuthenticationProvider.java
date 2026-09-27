package org.clevercubs.platform.security;

import java.time.Instant;
import java.time.LocalDateTime;
import java.time.ZoneOffset;
import java.util.Map;
import java.util.Optional;

import org.clevercubs.audit.AuditLog;
import org.clevercubs.platform.db.SqlDialect;
import org.clevercubs.platform.db.Timestamps;
import org.springframework.jdbc.core.simple.JdbcClient;
import org.springframework.security.authentication.AuthenticationProvider;
import org.springframework.security.authentication.BadCredentialsException;
import org.springframework.security.authentication.DisabledException;
import org.springframework.security.authentication.LockedException;
import org.springframework.security.authentication.UsernamePasswordAuthenticationToken;
import org.springframework.security.core.Authentication;
import org.springframework.security.core.AuthenticationException;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.stereotype.Component;

/**
 * Turns an email address and a password into the {@link SessionAuthentication} the rest of the application
 * already uses, so a sign-in is a server session and never a token the browser keeps (DD-02, docs/04 4.1).
 *
 * <p>The account model is {@code user_account} (docs/05-data-model.md 3.1). The sign-in identifier is the
 * email address, which is the unique key and is what {@link AccountPrincipal#getUsername()} returns. A
 * child has no account and no password at all: a parent enters child mode (D58).
 *
 * <p>Three properties matter more than the happy path:
 *
 * <ul>
 *   <li><b>No enumeration.</b> An unknown address costs exactly as much as a known one: the BCrypt
 *       comparison is always performed, against a dummy hash when no account was found. A stranger cannot
 *       tell a registered address from an unregistered one by timing, by status code or by message.
 *   <li><b>The hash goes no further.</b> It is compared, then erased from the principal before the
 *       authentication is returned, so it is never serialised into the session and never reaches a
 *       response. Only BCrypt is ever compared; nothing is decrypted and no password is ever stored.
 *   <li><b>The trail, not the log.</b> Every outcome is written to {@code audit_event}, which holds the
 *       account id and the reason and never an address, a password or a hash. Nothing is written to the
 *       application log, because logs are copied around far more freely than the audit table is read.
 *       A re-authentication ({@link ReauthenticationToken}) is audited on refusal, like any other failed
 *       attempt, and is not a sign-in on success, so it records no sign-in either.
 * </ul>
 */
@Component
public class AccountAuthenticationProvider implements AuthenticationProvider {

    /**
     * A valid BCrypt hash of an unrevealed value, compared against only when no account was found, so that
     * the refusal costs the same time as a wrong password. It authenticates nothing: no account can hold
     * this value, because no account is ever created with a password equal to it.
     */
    private final String equalisingHash;

    private final JdbcClient jdbc;
    private final PasswordEncoder passwords;
    private final AuditLog audit;
    private final SqlDialect dialect;

    public AccountAuthenticationProvider(JdbcClient jdbc, PasswordEncoder passwords, AuditLog audit,
            SqlDialect dialect) {
        this.dialect = dialect;
        this.jdbc = jdbc;
        this.passwords = passwords;
        this.audit = audit;
        // Made with the live encoder, so it always costs exactly what a real account's hash costs.
        this.equalisingHash = passwords.encode(java.util.UUID.randomUUID().toString());
    }

    @Override
    public Authentication authenticate(Authentication authentication) throws AuthenticationException {
        if (!supports(authentication.getClass())) {
            return null;
        }

        String email = String.valueOf(authentication.getPrincipal()).trim();
        String password = String.valueOf(authentication.getCredentials());

        Optional<AccountRow> found = findByEmail(email);
        AccountRow row = found.orElse(null);

        // Always paid for, whether or not an account exists, so the answer does not depend on the address.
        String storedHash = row == null ? equalisingHash : row.passwordHash();
        boolean passwordMatches = passwords.matches(password, storedHash);

        if (row == null || !passwordMatches) {
            refuse(row, row == null ? "UNKNOWN_ACCOUNT" : "BAD_PASSWORD");
            if (row != null) {
                registerFailure(row);
            }
            throw new BadCredentialsException("The email address or the password is not correct");
        }

        AccountPrincipal principal = row.toPrincipal();

        if (!principal.isAccountNonLocked() || row.isLockedByStatus()) {
            audit.record(row.id(), row.role().name(), "AUTH_LOGIN_REFUSED", "user_account", row.id(),
                    Map.of("reason", "LOCKED"));
            throw new LockedException("The account is locked");
        }
        if (!principal.isEnabled()) {
            audit.record(row.id(), row.role().name(), "AUTH_LOGIN_REFUSED", "user_account", row.id(),
                    Map.of("reason", row.status()));
            throw new DisabledException("The account is not active");
        }

        // A proven password ends any run of failures (DD-05).
        jdbc.sql("UPDATE user_account SET failed_logins = 0 WHERE id = :id AND failed_logins <> 0")
                .param("id", row.id())
                .update();

        // The hash has done its job. It must not travel into the session (AccountPrincipal is serialised).
        principal.eraseCredentials();
        // A re-confirmation for a session that is already open is not a sign-in, so last_login_at and the
        // AUTH_LOGIN_SIGNED_IN row are left exactly as the sign-in wrote them. A refusal was audited above,
        // whichever kind of request it came from.
        if (!(authentication instanceof ReauthenticationToken)) {
            recordSignIn(row);
        }
        return SessionAuthentication.signedIn(principal);
    }

    @Override
    public boolean supports(Class<?> authentication) {
        return UsernamePasswordAuthenticationToken.class.isAssignableFrom(authentication);
    }

    /**
     * Records the refusal, without the address that was tried: the audit trail is where a repeated attempt
     * against one account id is spotted, and it is not where an email address belongs.
     */
    private void refuse(AccountRow row, String reason) {
        if (row == null) {
            audit.record(null, "ANONYMOUS", "AUTH_LOGIN_REFUSED", null, null, Map.of("reason", reason));
        } else {
            audit.record(row.id(), row.role().name(), "AUTH_LOGIN_REFUSED", "user_account", row.id(),
                    Map.of("reason", reason));
        }
    }

    /**
     * DD-05: after {@link #MAX_FAILURES} wrong passwords in a row the account is locked for
     * {@link #LOCK_DURATION}; the counter restarts, so every further run of failures locks it again. Two
     * statements, because MySQL evaluates an UPDATE's assignments left to right against the new values.
     */
    private void registerFailure(AccountRow row) {
        jdbc.sql("UPDATE user_account SET failed_logins = failed_logins + 1 WHERE id = :id")
                .param("id", row.id())
                .update();
        int locked = jdbc.sql("""
                        UPDATE user_account SET locked_until = :until, failed_logins = 0
                        WHERE id = :id AND failed_logins >= :max""")
                .param("until", LocalDateTime.now(ZoneOffset.UTC).plus(LOCK_DURATION))
                .param("id", row.id())
                .param("max", MAX_FAILURES)
                .update();
        if (locked == 1) {
            audit.record(row.id(), row.role().name(), "AUTH_ACCOUNT_LOCKED", "user_account", row.id(),
                    Map.of("minutes", LOCK_DURATION.toMinutes()));
        }
    }

    static final int MAX_FAILURES = 5;
    static final java.time.Duration LOCK_DURATION = java.time.Duration.ofMinutes(15);

    private void recordSignIn(AccountRow row) {
        jdbc.sql("UPDATE user_account SET last_login_at = :now WHERE id = :id")
                .param("now", Timestamps.now())
                .param("id", row.id())
                .update();
        audit.record(row.id(), row.role().name(), "AUTH_LOGIN_SIGNED_IN", "user_account", row.id(), Map.of());
    }

    /**
     * Reads one account by its unique email. The column ignores letter case (MySQL's collation, PostgreSQL's
     * CITEXT), so the comparison does too; the stored value is returned unchanged, so what the client sees is
     * what the database holds.
     */
    private Optional<AccountRow> findByEmail(String email) {
        return jdbc.sql("""
                        SELECT id, email, password_hash, role, status, locked_until, must_change_password
                        FROM user_account WHERE email =\s""" + dialect.caseInsensitive("email"))
                .param("email", email)
                .query((rs, rowNumber) -> {
                    LocalDateTime lockedUntil = rs.getObject("locked_until", LocalDateTime.class);
                    return new AccountRow(
                            rs.getLong("id"),
                            rs.getString("email"),
                            rs.getString("password_hash"),
                            Role.valueOf(rs.getString("role")),
                            rs.getString("status"),
                            lockedUntil == null ? null : lockedUntil.toInstant(ZoneOffset.UTC),
                            rs.getBoolean("must_change_password"));
                })
                .optional();
    }

    /**
     * One row of {@code user_account}, already shaped for {@link AccountPrincipal}. Timestamps are stored
     * as UTC (V1__schema.sql) and read as UTC here, never in the JVM's own zone.
     */
    private record AccountRow(long id, String email, String passwordHash, Role role, String status,
            Instant lockedUntil, boolean mustChangePassword) {

        boolean isLockedByStatus() {
            return "LOCKED".equals(status);
        }

        AccountPrincipal toPrincipal() {
            return new AccountPrincipal(id, email, passwordHash, role, "ACTIVE".equals(status), lockedUntil,
                    mustChangePassword);
        }
    }
}
