package org.clevercubs.account;

import java.util.Map;

import org.clevercubs.audit.AuditLog;
import org.clevercubs.platform.security.CurrentUser;
import org.clevercubs.platform.security.PasswordPolicy;
import org.clevercubs.platform.security.ReauthenticationToken;
import org.clevercubs.platform.security.SessionAuthentication;
import org.clevercubs.platform.web.ApiException;
import org.springframework.http.HttpStatus;
import org.springframework.jdbc.core.simple.JdbcClient;
import org.springframework.security.authentication.AuthenticationManager;
import org.springframework.security.core.AuthenticationException;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.stereotype.Component;

/**
 * Replaces a signed-in account's password, and with it the temporary-password restriction the account was
 * carrying.
 *
 * <p>This exists because the bootstrap creates its Super Admin with {@code must_change_password = true}
 * ({@code D69}) and {@link org.clevercubs.platform.security.PasswordChangeRequiredFilter} then closes
 * everything except the account's own. Without this class the deployment has an administrator who can sign
 * in and then do nothing at all, which is the state the previous slice deliberately left visible.
 *
 * <p>Three properties are the point of the class:
 *
 * <ul>
 *   <li><b>The current password is proved, not trusted.</b> The request carries the account's own password
 *       and the session already knows who the caller is, but neither is enough: the password goes through
 *       {@link org.clevercubs.platform.security.AccountAuthenticationProvider} exactly as a sign-in does,
 *       via {@link ReauthenticationToken}. So the BCrypt comparison, the equalising hash that keeps the cost
 *       of a refusal constant, the lock and disabled checks, and the {@code AUTH_LOGIN_REFUSED} audit row are
 *       all the existing ones. {@code ReauthenticationToken} rather than a plain
 *       {@code UsernamePasswordAuthenticationToken} is deliberate and load-bearing: the provider treats it
 *       as "not a sign-in", so {@code last_login_at} and {@code AUTH_LOGIN_SIGNED_IN} are left alone. Neither
 *       of those happened, and a trail that records a sign-in that did not occur is worse than one that
 *       records nothing ({@code DD-14}).</li>
 *   <li><b>Only the password changes.</b> The update names {@code password_hash},
 *       {@code must_change_password}, {@code password_changed_at} and {@code updated_at} and nothing else,
 *       so role, status, lock, {@code failed_logins} and {@code last_login_at} cannot drift as a side
 *       effect. The account is found by the session's id, never by anything in the request, so this cannot
 *       be pointed at somebody else's account.</li>
 *   <li><b>The requirement is cleared in the session as well as in the database.</b> Clearing only the
 *       column would leave the filter reading a stale principal and refusing the very next request from an
 *       account that had just chosen a password of its own. The new identity is returned to the caller,
 *       which stores it in the session; the session id is not reissued and the session is not invalidated,
 *       so a client that changes a password mid-task keeps working.</li>
 * </ul>
 *
 * <p>Nothing secret is written anywhere. The audit row carries identifiers and the outcome only, and the
 * log says nothing at all about the call — logs are copied around far more freely than the audit table is
 * read. A refusal is audited by {@link org.clevercubs.platform.security.AccountAuthenticationProvider} in
 * its usual secret-free shape, so this class adds no second audit path for a failed password.
 */
@Component
public class PasswordChangeService {

    /**
     * The one number the policy is, from {@code DD-01}: a password must be at least this long. The
     * upper bound exists only so a huge body cannot be turned into expensive hashing, exactly as on
     * {@code POST /api/v1/auth/reauth}.
     *
     * <p>{@code DD-01} also asks for a check against {@code resources/security/common-passwords.txt}, and
     * that file ships with the application. It is still wired to nothing — on any path, not only this one —
     * so it is deliberately not introduced here: this slice ends the lockout, and a password-policy change
     * is its own piece of work with its own decision.
     */
    public static final int MINIMUM_LENGTH = 12;

    /** The maximum length accepted, so an enormous body cannot be turned into expensive hashing. */
    public static final int MAXIMUM_LENGTH = 200;

    /**
     * One message for every refusal, the same one the sign-in uses. A different answer for "wrong current
     * password" than for anything else would say something about the account behind the session, and this
     * endpoint is only reachable by an account that is already signed in — so the caller knows the address
     * exists and must learn nothing more.
     */
    private static final String INVALID_CREDENTIALS =
            "That email address and password do not match an account.";

    private final JdbcClient jdbc;
    private final PasswordEncoder passwords;
    private final AuditLog audit;
    private final AuthenticationManager authenticationManager;
    private final CurrentUser currentUser;
    private final PasswordPolicy policy;

    public PasswordChangeService(JdbcClient jdbc, PasswordEncoder passwords, AuditLog audit,
            AuthenticationManager authenticationManager, CurrentUser currentUser, PasswordPolicy policy) {
        this.jdbc = jdbc;
        this.passwords = passwords;
        this.audit = audit;
        this.authenticationManager = authenticationManager;
        this.currentUser = currentUser;
        this.policy = policy;
    }

    /**
     * Changes the password of the account behind the current session, and returns the identity that session
     * should now hold: the same account, with the requirement cleared.
     *
     * <p>Nothing is written unless the current password is proved first, and a wrong current password
     * changes nothing at all — not the password, not the flag, not the session.
     *
     * @throws ApiException {@code invalid-credentials} if the current password does not match, or if the
     *     account is locked or disabled; {@code unauthenticated} if there is no session
     */
    SessionAuthentication change(String currentPassword, String newPassword) {
        SessionAuthentication session = currentUser.session();
        var account = session.account();

        try {
            authenticationManager.authenticate(
                    ReauthenticationToken.of(account.email(), currentPassword));
        } catch (AuthenticationException refused) {
            // Locked and disabled accounts are refused here too, as they are at a sign-in, and they are
            // refused in the same generic words: this endpoint does not become a way to probe an account's
            // state by answering differently for a locked one.
            throw new ApiException(HttpStatus.UNAUTHORIZED, "invalid-credentials", INVALID_CREDENTIALS);
        }

        // DD-01 in full, now that the policy has one home (PasswordPolicy): length, the common-password list and
        // the account's own address. Checked only after the current password is proved.
        policy.check(newPassword, account.email(), "newPassword");

        // Hashed before it is written and never retained beyond this line; only the hash reaches the column.
        String hash = passwords.encode(newPassword);

        jdbc.sql("""
                        UPDATE user_account
                        SET password_hash = :hash,
                            must_change_password = FALSE,
                            password_changed_at = UTC_TIMESTAMP(6),
                            updated_at = UTC_TIMESTAMP(6)
                        WHERE id = :id""")
                .param("hash", hash)
                .param("id", account.accountId())
                .update();

        // One row, per DD-14. The details are empty on purpose: the account id is the target, the actor and
        // the target are the same person, and there is nothing about a password change to add to that.
        audit.record(account.accountId(), account.role().name(), "PASSWORD_CHANGED", "user_account",
                account.accountId(), Map.of());

        // withPasswordChanged() also drops the stored hash from the principal, so the session never carries
        // one — the same guarantee AccountPrincipal makes at a sign-in.
        return session.withPrincipal(account.withPasswordChanged());
    }
}
