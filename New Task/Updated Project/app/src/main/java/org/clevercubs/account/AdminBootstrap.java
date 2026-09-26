package org.clevercubs.account;

import java.util.Map;
import java.util.Optional;

import org.clevercubs.audit.AuditLog;
import org.clevercubs.platform.config.CleverCubsProperties;
import org.clevercubs.platform.security.Role;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.boot.ApplicationArguments;
import org.springframework.boot.ApplicationRunner;
import org.springframework.dao.DuplicateKeyException;
import org.springframework.jdbc.core.simple.JdbcClient;
import org.springframework.jdbc.support.GeneratedKeyHolder;
import org.springframework.jdbc.support.KeyHolder;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.stereotype.Component;

/**
 * Creates the one initial Super Admin that the deployment is configured with, so the application is
 * reachable before anyone has registered ({@code CC_ADMIN_EMAIL} and {@code CC_ADMIN_INITIAL_PASSWORD},
 * bound as {@code clevercubs.admin.bootstrap-*}, documented in {@code .env.example}).
 *
 * <p>This is the bootstrap of a single configured account, not an account-management feature: there is no
 * endpoint here, no way to call it, and no way to point it at a second address. A Super Admin that is
 * created later is created by a later phase through the admin APIs, which do not exist yet.
 *
 * <p>It runs as an {@link ApplicationRunner} on purpose. That is after the whole context has refreshed, so
 * Flyway has already applied V1 and the {@code user_account} table and its grants are certain to exist; a
 * component that touched the table from its own constructor would depend on bean initialisation order and
 * could read a database that has not been migrated.
 *
 * <p>Three properties make it safe to leave in the configuration and start repeatedly:
 * <ul>
 *   <li><b>Nothing configured, nothing happens.</b> Both values are required, and both default to empty in
 *       every profile, so the common case of a deployment with no bootstrap configured is a no-op rather
 *       than a failure. Half-configured is a warning, because it is almost always a forgotten value rather
 *       than an intention.</li>
 *   <li><b>An existing account is never touched.</b> The bootstrap only ever inserts. It does not update a
 *       password, does not reset a flag and does not re-activate a disabled account, so restarting cannot
 *       undo a change an operator made deliberately — the single most dangerous thing a bootstrap like this
 *       could do.</li>
 *   <li><b>It refuses to add a second Super Admin.</b> It skips when the configured address already has an
 *       account, and also when any Super Admin already exists, so a stale value left in {@code .env} cannot
 *       quietly mint another one. The unique key on {@code email} is the third line of defence: if two
 *       instances start at once, one insert loses and is treated as a skip rather than a failure.</li>
 * </ul>
 *
 * <p>The account is created {@code ACTIVE} with {@code must_change_password = true}, which is the whole
 * point of a bootstrap password: it is a deployment secret, not a password a person chose, and
 * {@code PasswordChangeRequiredFilter} holds the account to its own account until it is replaced.
 * {@code POST /api/v1/auth/change-password} is the one route it may still reach, and it is reachable for no
 * other reason: until the password is actually changed, the flag is still in {@code user_account} and every
 * other route stays refused.
 *
 * <p>Nothing secret is written anywhere. The plaintext password is read from configuration, passed straight
 * to the {@link PasswordEncoder} and never retained, logged or echoed; only the resulting hash reaches the
 * database. The address itself is logged once, at startup, because an operator who cannot tell which
 * account was bootstrapped has no way to use it. It is deliberately kept out of the audit trail, which
 * refers to records by id ({@link AuditLog}).
 */
@Component
class AdminBootstrap implements ApplicationRunner {

    private static final Logger log = LoggerFactory.getLogger(AdminBootstrap.class);

    /**
     * {@code DD-01}'s floor, applied as a warning only. This is not the {@code DD-01} check, which also
     * covers a common-password list and is not built; see {@code docs/04} §4.2. A deployment whose
     * configured password is short still gets its Super Admin, because {@code must_change_password} forces
     * a replacement at the first sign-in, and refusing here would leave the deployment with no way in at
     * all — a worse outcome than a weak temporary password.
     */
    private static final int MINIMUM_PASSWORD_LENGTH = 12;

    private static final String ACTION_BOOTSTRAPPED = "ADMIN_BOOTSTRAPPED";

    /** There is no signed-in account yet at startup, so the trail records the system, as elsewhere. */
    private static final String SYSTEM = "SYSTEM";

    private final JdbcClient jdbc;
    private final PasswordEncoder passwords;
    private final AuditLog audit;
    private final CleverCubsProperties properties;

    AdminBootstrap(JdbcClient jdbc, PasswordEncoder passwords, AuditLog audit,
            CleverCubsProperties properties) {
        this.jdbc = jdbc;
        this.passwords = passwords;
        this.audit = audit;
        this.properties = properties;
    }

    @Override
    public void run(ApplicationArguments args) {
        var admin = properties.admin();
        createIfAbsent(admin.bootstrapEmail(), admin.bootstrapPassword());
    }

    /**
     * Creates the initial Super Admin, or does nothing at all.
     *
     * <p>Package-private and taking the values as arguments so the whole decision can be exercised against
     * the real database without a second Spring context or a second set of bound properties: the only thing
     * {@link #run(ApplicationArguments)} adds is reading the two values out of configuration.
     *
     * @param email    the configured address; blank means not configured
     * @param password the configured password; blank means not configured
     * @return the new account's id, or empty when nothing was created
     */
    Optional<Long> createIfAbsent(String email, String password) {
        if (email == null || email.isBlank() || password == null || password.isBlank()) {
            reportNotConfigured(email, password);
            return Optional.empty();
        }

        String address = email.trim();

        if (exists(address)) {
            log.info("The Super Admin bootstrap did nothing: an account already uses the configured address. "
                    + "No account, password or flag was changed.");
            return Optional.empty();
        }

        if (anySuperAdminExists()) {
            log.info("The Super Admin bootstrap did nothing: a Super Admin already exists, so the configured "
                    + "address was not created. No account, password or flag was changed.");
            return Optional.empty();
        }

        if (password.length() < MINIMUM_PASSWORD_LENGTH) {
            log.warn("The configured initial Super Admin password is shorter than the {} characters DD-01 asks "
                    + "for. The account is still being created, and must_change_password means it has to be "
                    + "replaced at the first sign-in.", MINIMUM_PASSWORD_LENGTH);
        }

        return insert(address, password);
    }

    /**
     * The single insert. Everything the account needs is set here, so no later step has to complete it: a
     * half-created admin that is active but not flagged would be reachable in the whole application with a
     * deployment password, and one that is flagged but disabled could not sign in at all.
     *
     * <p>{@code password_changed_at} records when the credential was set, which for a bootstrap is now — the
     * column is NOT NULL and the user has not changed anything yet. A failed insert is a skip, not a
     * crash: it means another instance won the race between the check above and this statement.
     */
    private Optional<Long> insert(String address, String password) {
        KeyHolder keys = new GeneratedKeyHolder();
        try {
            jdbc.sql("""
                            INSERT INTO user_account (email, password_hash, role, status, failed_logins,
                                                      locked_until, must_change_password, password_changed_at,
                                                      created_at, updated_at)
                            VALUES (:email, :hash, 'SUPER_ADMIN', 'ACTIVE', 0, NULL, TRUE,
                                    UTC_TIMESTAMP(6), UTC_TIMESTAMP(6), UTC_TIMESTAMP(6))""")
                    .param("email", address)
                    .param("hash", passwords.encode(password))
                    .update(keys, "id");
        } catch (DuplicateKeyException anotherInstanceWon) {
            log.info("The Super Admin bootstrap did nothing: the account was created by another instance "
                    + "starting at the same time. No account, password or flag was changed.");
            return Optional.empty();
        }

        long id = keys.getKey().longValue();
        audit.record(null, SYSTEM, ACTION_BOOTSTRAPPED, "user_account", id,
                Map.of("role", Role.SUPER_ADMIN.name(), "source", "configuration"));
        log.info("Created the initial Super Admin account (id {}) from configuration. Its password must be "
                + "changed at the first sign-in.", id);
        return Optional.of(id);
    }

    private boolean exists(String email) {
        return jdbc.sql("SELECT COUNT(*) FROM user_account WHERE email = :email")
                .param("email", email)
                .query(Long.class)
                .single() > 0;
    }

    private boolean anySuperAdminExists() {
        return jdbc.sql("SELECT COUNT(*) FROM user_account WHERE role = :role")
                .param("role", Role.SUPER_ADMIN.name())
                .query(Long.class)
                .single() > 0;
    }

    /**
     * Reports half-configuration, and stays silent when both values are simply absent, which is the normal
     * state of every profile except a deployment that wants a bootstrap. Only the <em>missing</em> half is
     * ever named; neither value is echoed, so this line cannot become a place a password leaks from.
     */
    private void reportNotConfigured(String email, String password) {
        boolean hasEmail = email != null && !email.isBlank();
        boolean hasPassword = password != null && !password.isBlank();

        if (hasEmail && hasPassword) {
            return; // unreachable: the caller has already checked this pair
        }
        if (!hasEmail && !hasPassword) {
            log.debug("No initial Super Admin is configured, so none was created.");
            return;
        }
        log.warn("The initial Super Admin is only partly configured, so no account was created. Set "
                + (hasEmail ? "CC_ADMIN_INITIAL_PASSWORD" : "CC_ADMIN_EMAIL")
                + ", or clear both to say that no bootstrap is wanted.");
    }
}
