package org.clevercubs.account;

import static org.assertj.core.api.Assertions.assertThat;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.post;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.jsonPath;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import java.util.ArrayList;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;
import java.util.Optional;
import java.util.UUID;
import java.util.stream.Collectors;

import org.clevercubs.platform.config.CleverCubsProperties;
import org.clevercubs.platform.db.Timestamps;
import org.clevercubs.support.IntegrationTest;
import org.junit.jupiter.api.AfterEach;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.ApplicationRunner;
import org.springframework.context.ApplicationContext;
import org.springframework.http.MediaType;
import org.springframework.jdbc.core.simple.JdbcClient;
import org.springframework.mock.web.MockHttpSession;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.test.web.servlet.MvcResult;
import org.springframework.test.web.servlet.MockMvc;
import org.springframework.test.web.servlet.request.MockHttpServletRequestBuilder;

import ch.qos.logback.classic.Logger;
import ch.qos.logback.classic.spi.ILoggingEvent;
import ch.qos.logback.core.read.ListAppender;
import jakarta.servlet.http.Cookie;

/**
 * The initial Super Admin bootstrap, against the real MySQL: it creates the one account the deployment is
 * configured with, and on every other run it changes nothing at all.
 *
 * <p>The decision is a function of two strings and the state of {@code user_account}, so most tests call
 * {@link AdminBootstrap#createIfAbsent} with their own values rather than starting a second Spring context
 * with different bound properties. The two things that call adds — that the class really is a runner Spring
 * will invoke, and that it really reads {@code clevercubs.admin.bootstrap-*} — are proved on their own by
 * {@link #itIsARunnerThatReadsTheBootstrapConfiguration()}.
 *
 * <p>Each test removes the accounts it created. The audit rows are left behind on purpose:
 * {@code audit_event} is append-only, {@code cc_app} holds no DELETE on it, and the container is thrown
 * away with the suite. No test here therefore asserts on a total count of audit rows, which would depend on
 * which tests happened to run first.
 */
class AdminBootstrapTests extends IntegrationTest {

    private static final String HEALTH = "/api/v1/public/health";
    private static final String LOGIN = "/api/v1/auth/login";
    private static final String ME = "/api/v1/auth/me";

    /** An admin-only route with no controller behind it, to watch the temporary-password rule act. */
    private static final String ADMIN_AREA = "/api/v1/admin/settings";

    /** Test-only credentials. They exist in this file and the throwaway container, nowhere else. */
    private static final String PASSWORD = "Correct-Horse-9";

    /** Shorter than DD-01's floor, so the warning path is taken. */
    private static final String SHORT_PASSWORD = "short-one";

    @Autowired
    AdminBootstrap bootstrap;

    @Autowired
    JdbcClient jdbc;

    @Autowired
    PasswordEncoder passwords;

    @Autowired
    MockMvc mvc;

    @Autowired
    ApplicationContext context;

    @Autowired
    CleverCubsProperties properties;

    /**
     * Addresses this test may have created an account for. Tracked by address and not by id, and registered
     * by {@link #unusedEmail()} before the account exists, so cleanup cannot be defeated by the order of a
     * test's own statements: a leaked Super Admin would make every later test's bootstrap a no-op.
     */
    private final List<String> createdAddresses = new ArrayList<>();

    @AfterEach
    void removeTheAccountsThisTestCreated() {
        for (String email : createdAddresses) {
            jdbc.sql("DELETE FROM user_account WHERE email = :email").param("email", email).update();
        }
        createdAddresses.clear();
    }

    // --- the configured bootstrap creates the account -------------------------------------

    @Test
    @DisplayName("a configured bootstrap creates one ACTIVE Super Admin that must change its password")
    void configuredBootstrapCreatesTheAccount() {
        String email = unusedEmail();

        Optional<Long> created = bootstrap.createIfAbsent(email, PASSWORD);

        assertThat(created).as("the bootstrap reports the account it made").isPresent();

        Map<String, Object> row = rowOf(email);
        assertThat(rowsWithAddress(email)).as("exactly one account carries the configured address").isEqualTo(1);
        assertThat(row.get("role")).isEqualTo("SUPER_ADMIN");
        assertThat(row.get("status")).isEqualTo("ACTIVE");
        assertThat(row.get("must_change_password"))
                .as("a bootstrap password is never one the owner chose, so it must be replaced")
                .isEqualTo(Boolean.TRUE);
        assertThat(row.get("failed_logins")).isEqualTo(0);
        assertThat(row.get("locked_until")).as("a new account is not locked").isNull();
    }

    @Test
    @DisplayName("the bootstrap password is stored only as a BCrypt hash")
    void passwordIsStoredAsABcryptHash() {
        String email = unusedEmail();
        bootstrap.createIfAbsent(email, PASSWORD);

        String stored = hashOf(email);

        assertThat(stored)
                .isNotEqualTo(PASSWORD)
                .startsWith("$2")
                .hasSizeLessThanOrEqualTo(100); // the column is VARCHAR(100); a wider hash would not fit
        assertThat(passwords.matches(PASSWORD, stored)).as("the configured password is the one that was set")
                .isTrue();
        assertThat(passwords.matches("not-the-password", stored)).isFalse();

        // Stronger than looking at password_hash alone: no column of the row may hold the plaintext.
        assertThat(rowOf(email).values())
                .as("the plaintext is nowhere in the created row")
                .allSatisfy(value -> assertThat(String.valueOf(value)).doesNotContain(PASSWORD));
    }

    @Test
    @DisplayName("the created account signs in, and the fail-closed temporary-password rule holds it")
    void theCreatedAccountIsUsableAndStillHeldToThePasswordChange() throws Exception {
        String email = unusedEmail();
        bootstrap.createIfAbsent(email, PASSWORD);

        MockHttpSession session = signIn(email);

        // The account is real: it authenticates and it can read its own account.
        mvc.perform(get(ME).session(session))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.email").value(email))
                .andExpect(jsonPath("$.role").value("SUPER_ADMIN"))
                .andExpect(jsonPath("$.mustChangePassword").value(true));

        // ...and it reaches nothing else. The bootstrap must not hand out a usable admin session, and the
        // existing filter is what stops it, unchanged: setting the flag was the only thing required of this
        // task, and no part of the fail-closed rule was touched to get here.
        mvc.perform(get(ADMIN_AREA).session(session))
                .andExpect(status().isForbidden())
                .andExpect(jsonPath("$.code").value("password-change-required"));
    }

    // --- running again changes nothing ----------------------------------------------------

    @Test
    @DisplayName("running again over an existing account overwrites neither the password nor the flags")
    void rerunningDoesNotOverwriteAnExistingAccount() {
        String email = unusedEmail();
        bootstrap.createIfAbsent(email, PASSWORD);

        // What an operator who has taken over would have done: chosen their own password, replaced the
        // temporary one, and disabled the account.
        String chosen = "Owner-Chosen-4";
        jdbc.sql("""
                        UPDATE user_account
                        SET password_hash = :hash, must_change_password = FALSE, status = 'DISABLED',
                            updated_at = :now
                        WHERE id = :id""")
                .param("now", Timestamps.now())
                .param("hash", passwords.encode(chosen))
                .param("id", idOf(email))
                .update();

        // The same configuration is applied again, as it would be on the next restart.
        Optional<Long> second = bootstrap.createIfAbsent(email, PASSWORD);

        assertThat(second).as("the rerun created nothing").isEmpty();
        assertThat(rowsWithAddress(email)).as("still exactly one account, not a second one").isEqualTo(1);
        assertThat(passwords.matches(chosen, hashOf(email))).as("the owner's own password is untouched").isTrue();
        assertThat(passwords.matches(PASSWORD, hashOf(email))).as("the bootstrap password did not come back")
                .isFalse();
        assertThat(rowOf(email).get("status")).as("a deliberate status change is not undone")
                .isEqualTo("DISABLED");
        assertThat(rowOf(email).get("must_change_password")).as("a cleared flag is not set again")
                .isEqualTo(Boolean.FALSE);
    }

    @Test
    @DisplayName("a second Super Admin is not created while one already exists")
    void aSecondSuperAdminIsNotCreated() {
        String first = unusedEmail();
        bootstrap.createIfAbsent(first, PASSWORD);

        String second = unusedEmail();
        Optional<Long> refused = bootstrap.createIfAbsent(second, PASSWORD);

        assertThat(refused).as("a different address is refused too, because a Super Admin already exists")
                .isEmpty();
        assertThat(rowsWithAddress(second)).as("the second address was never used").isZero();
    }

    @Test
    @DisplayName("a rerun writes no second audit row for an account it did not create")
    void aSkipIsNotAuditedAsACreation() {
        String email = unusedEmail();
        bootstrap.createIfAbsent(email, PASSWORD);
        long id = idOf(email);
        long afterTheFirstRun = bootstrapAuditRows(id);

        bootstrap.createIfAbsent(email, PASSWORD);

        assertThat(bootstrapAuditRows(id))
                .as("the trail says the account was created once, not that it was touched again")
                .isEqualTo(afterTheFirstRun);
    }

    // --- nothing configured, nothing done ---------------------------------------------------

    @Test
    @DisplayName("missing or blank bootstrap configuration does nothing")
    void blankConfigurationDoesNothing() {
        long before = superAdminCount();

        assertThat(bootstrap.createIfAbsent("", PASSWORD)).isEmpty();
        assertThat(bootstrap.createIfAbsent("   ", PASSWORD)).isEmpty();
        assertThat(bootstrap.createIfAbsent(unusedEmail(), "")).isEmpty();
        assertThat(bootstrap.createIfAbsent(unusedEmail(), "   ")).isEmpty();
        assertThat(bootstrap.createIfAbsent(null, null)).isEmpty();
        assertThat(bootstrap.createIfAbsent(null, PASSWORD)).isEmpty();
        assertThat(bootstrap.createIfAbsent(unusedEmail(), null)).isEmpty();

        assertThat(superAdminCount()).as("no account was created by any of them").isEqualTo(before);
    }

    @Test
    @DisplayName("it is a runner that reads the bootstrap configuration, and with it unset it does nothing")
    void itIsARunnerThatReadsTheBootstrapConfiguration() {
        // The wiring the ApplicationRunner contract depends on: Spring will invoke this bean on startup.
        assertThat(context.getBeansOfType(ApplicationRunner.class).values())
                .as("the bootstrap is registered as a runner, not merely as a bean")
                .contains(bootstrap);

        // The binding the runner reads. application-test.yml leaves both values empty, which is also the
        // default in every other profile, so the resolved values must be the empty ones rather than null.
        assertThat(properties.admin().bootstrapEmail()).isEmpty();
        assertThat(properties.admin().bootstrapPassword()).isEmpty();

        long before = superAdminCount();
        bootstrap.run(null);

        assertThat(superAdminCount())
                .as("an unconfigured startup creates no Super Admin, which is every test profile's state")
                .isEqualTo(before);
    }

    // --- nothing secret gets out ------------------------------------------------------------

    @Test
    @DisplayName("the bootstrap password never reaches the log")
    void thePasswordIsNeverLogged() {
        CapturedLog captured = captureTheLogWhile(unusedEmail());

        assertThat(captured.log())
                .as("neither the configured password nor the weak one is echoed")
                .doesNotContain(PASSWORD)
                .doesNotContain(SHORT_PASSWORD)
                .as("nor is the hash the password became")
                .doesNotContain(captured.storedHash())
                .as("CleverCubsProperties.Admin masks the password in its own toString")
                .doesNotContain("bootstrapPassword=" + PASSWORD);
    }

    // --- helpers ----------------------------------------------------------------------------

    /**
     * Runs the three paths that can log, captures the root logger around them, and leaves behind exactly
     * one account for {@link #removeTheAccountsThisTestCreated()} to remove: the create path with a good
     * password, the refused rerun, and the warning path with a short one. The short-password run needs the
     * first account gone, or the "a Super Admin already exists" guard would refuse it and the warning would
     * never be taken.
     */
    private CapturedLog captureTheLogWhile(String email) {
        Logger root = (Logger) LoggerFactory.getLogger(Logger.ROOT_LOGGER_NAME);
        ListAppender<ILoggingEvent> captured = new ListAppender<>();
        captured.start();
        root.addAppender(captured);

        try {
            bootstrap.createIfAbsent(email, PASSWORD);
            bootstrap.createIfAbsent(email, PASSWORD); // refused: the account now exists
            jdbc.sql("DELETE FROM user_account WHERE email = :email").param("email", email).update();
            bootstrap.createIfAbsent(email, SHORT_PASSWORD);
        } finally {
            root.detachAppender(captured);
            captured.stop();
        }
        return new CapturedLog(captured.list.stream()
                .map(ILoggingEvent::getFormattedMessage)
                .collect(Collectors.joining("\n")), hashOf(email));
    }

    private record CapturedLog(String log, String storedHash) {
    }

    private MockHttpSession signIn(String email) throws Exception {
        MvcResult result = mvc.perform(postJson(LOGIN, credentials(email, PASSWORD)))
                .andExpect(status().isOk())
                .andReturn();
        return (MockHttpSession) result.getRequest().getSession(false);
    }

    /** The real token exchange: a first request is issued the cookie, and the token is sent back in the header. */
    private String csrfToken() throws Exception {
        Cookie cookie = mvc.perform(get(HEALTH)).andReturn().getResponse().getCookie("XSRF-TOKEN");
        assertThat(cookie).as("the CSRF cookie is issued on the first request").isNotNull();
        return cookie.getValue();
    }

    private MockHttpServletRequestBuilder postJson(String path, String body) throws Exception {
        String token = csrfToken();
        return post(path)
                .contentType(MediaType.APPLICATION_JSON)
                .content(body)
                .cookie(new Cookie("XSRF-TOKEN", token))
                .header("X-XSRF-TOKEN", token);
    }

    private static String credentials(String email, String password) {
        return """
                {"email":"%s","password":"%s"}""".formatted(email, password);
    }

    /** A fresh address, registered for cleanup whether or not an account is ever created for it. */
    private String unusedEmail() {
        String email = "bootstrap-" + UUID.randomUUID() + "@example.test";
        createdAddresses.add(email);
        return email;
    }

    /** Every column of the one row with this address, so an assertion can cover all of them at once. */
    private Map<String, Object> rowOf(String email) {
        return jdbc.sql("SELECT * FROM user_account WHERE email = :email")
                .param("email", email)
                .query((rs, n) -> {
                    Map<String, Object> row = new LinkedHashMap<>();
                    for (int column = 1; column <= rs.getMetaData().getColumnCount(); column++) {
                        row.put(rs.getMetaData().getColumnLabel(column), rs.getObject(column));
                    }
                    return row;
                })
                .single();
    }

    private String hashOf(String email) {
        return jdbc.sql("SELECT password_hash FROM user_account WHERE email = :email")
                .param("email", email).query(String.class).single();
    }

    private long rowsWithAddress(String email) {
        return jdbc.sql("SELECT COUNT(*) FROM user_account WHERE email = :email")
                .param("email", email).query(Long.class).single();
    }

    private long superAdminCount() {
        return jdbc.sql("SELECT COUNT(*) FROM user_account WHERE role = 'SUPER_ADMIN'")
                .query(Long.class).single();
    }

    private long bootstrapAuditRows(long accountId) {
        return jdbc.sql("""
                        SELECT COUNT(*) FROM audit_event
                        WHERE action = 'ADMIN_BOOTSTRAPPED' AND target_id = :id""")
                .param("id", accountId).query(Long.class).single();
    }

    private long idOf(String email) {
        return jdbc.sql("SELECT id FROM user_account WHERE email = :email")
                .param("email", email).query((rs, n) -> rs.getLong("id")).optional().orElse(0L);
    }
}
