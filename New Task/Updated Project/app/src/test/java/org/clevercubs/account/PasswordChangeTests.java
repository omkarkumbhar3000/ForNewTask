package org.clevercubs.account;

import static org.assertj.core.api.Assertions.assertThat;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.post;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.content;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.jsonPath;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import java.time.LocalDateTime;
import java.util.ArrayList;
import java.util.List;
import java.util.UUID;
import java.util.stream.Collectors;

import org.clevercubs.platform.db.Timestamps;
import org.clevercubs.platform.security.Role;
import org.clevercubs.support.IntegrationTest;
import org.junit.jupiter.api.AfterEach;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.MediaType;
import org.springframework.jdbc.core.simple.JdbcClient;
import org.springframework.mock.web.MockHttpSession;
import org.springframework.security.core.context.SecurityContext;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.security.web.context.HttpSessionSecurityContextRepository;
import org.springframework.test.web.servlet.MockMvc;
import org.springframework.test.web.servlet.MvcResult;
import org.springframework.test.web.servlet.request.MockHttpServletRequestBuilder;

import ch.qos.logback.classic.Logger;
import ch.qos.logback.classic.spi.ILoggingEvent;
import ch.qos.logback.core.read.ListAppender;
import jakarta.servlet.http.Cookie;

/**
 * The password-change contract at the HTTP boundary: an account holding a temporary password proves the
 * password it has, chooses a new one, and is then a normal account again.
 *
 * <p>These are the tests that make the bootstrap usable. The Super Admin {@code AdminBootstrap} creates is
 * deliberately born with {@code must_change_password = true}, so without this endpoint a fresh deployment
 * has an administrator who can sign in and do nothing at all. Most tests here therefore use a flagged
 * account, and one uses a flagged Super Admin against the admin area, because that is the situation the
 * bootstrap actually produces.
 *
 * <p>Each test creates the account it needs and removes it afterwards, so the tests do not depend on each
 * other or on the order they run in. The CSRF token is taken from a real cookie, because that is the
 * exchange a browser and a future mobile client actually perform.
 */
class PasswordChangeTests extends IntegrationTest {

    private static final String LOGIN = "/api/v1/auth/login";
    private static final String ME = "/api/v1/auth/me";
    private static final String CHANGE = "/api/v1/auth/change-password";
    private static final String REAUTH = "/api/v1/auth/reauth";
    private static final String HEALTH = "/api/v1/public/health";

    /** One route only a parent may use, and one only a Super Admin may use. Neither has a controller yet. */
    private static final String PARENT_AREA = "/api/v1/parent/dashboard";
    private static final String ADMIN_AREA = "/api/v1/admin/accounts";

    /** The password an admin-issued temporary password stands in for, and the one chosen in its place. */
    private static final String TEMPORARY = "Temporary-Pass-1";
    private static final String CHOSEN = "Chosen-Passphrase-42";

    /** A {@code password_changed_at} far enough in the past that a change is unmistakable. */
    private static final LocalDateTime LONG_AGO = LocalDateTime.of(2020, 1, 1, 0, 0);

    @Autowired
    MockMvc mvc;

    @Autowired
    JdbcClient jdbc;

    @Autowired
    PasswordEncoder passwords;

    private final List<Long> createdAccounts = new ArrayList<>();

    @AfterEach
    void removeTheAccountsThisTestCreated() {
        for (long id : createdAccounts) {
            jdbc.sql("DELETE FROM user_account WHERE id = :id").param("id", id).update();
        }
        // Audit rows are left on purpose: audit_event is append-only, cc_app holds no DELETE on it, and the
        // container is thrown away with the suite.
        createdAccounts.clear();
    }

    // --- the endpoint exists and is reachable by the account that needs it -------------------------

    @Test
    @DisplayName("an account holding a temporary password can change it")
    void aFlaggedAccountCanChangeItsPassword() throws Exception {
        MockHttpSession session = signIn(flagged(Role.PARENT));

        mvc.perform(change(session, TEMPORARY, CHOSEN))
                .andExpect(status().isNoContent())
                .andExpect(content().string(""));

        assertThat(flagInDatabase(emailOf(session))).isFalse();
    }

    @Test
    @DisplayName("an ordinary account can change its password too")
    void anOrdinaryAccountCanAlsoChangeItsPassword() throws Exception {
        MockHttpSession session = signIn(ordinary(Role.PARENT));

        mvc.perform(change(session, TEMPORARY, CHOSEN)).andExpect(status().isNoContent());

        assertThat(storedHash(emailOf(session)))
                .as("this endpoint is not a privilege of the flagged state; it is how a password is replaced")
                .isNotEqualTo(passwords.encode(TEMPORARY));
    }

    // --- proving the current password ---------------------------------------------------------

    @Test
    @DisplayName("a wrong current password is refused, and nothing changes")
    void aWrongCurrentPasswordIsRefusedAndChangesNothing() throws Exception {
        String email = flagged(Role.PARENT);
        MockHttpSession session = signIn(email);
        String hashBefore = storedHash(email);

        mvc.perform(change(session, "not-the-password", CHOSEN))
                .andExpect(status().isUnauthorized())
                .andExpect(content().contentTypeCompatibleWith("application/problem+json"))
                .andExpect(jsonPath("$.code").value("invalid-credentials"))
                .andExpect(jsonPath("$.type").value("urn:clevercubs:problem:invalid-credentials"));

        assertThat(storedHash(email)).as("the stored password is untouched").isEqualTo(hashBefore);
        assertThat(flagInDatabase(email)).as("and so is the flag").isTrue();
        mvc.perform(get(ME).session(session))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.mustChangePassword").value(true));
    }

    @Test
    @DisplayName("the refusal for a wrong current password says no more than the refusal at a sign-in")
    void theRefusalRevealsNothingAboutTheAccount() throws Exception {
        String email = flagged(Role.PARENT);
        MockHttpSession session = signIn(email);

        String atSignIn = mvc.perform(postJson(LOGIN, credentials(email, "not-the-password"), csrfToken()))
                .andExpect(status().isUnauthorized())
                .andReturn().getResponse().getContentAsString();

        String atChange = mvc.perform(change(session, "not-the-password", CHOSEN))
                .andExpect(status().isUnauthorized())
                .andReturn().getResponse().getContentAsString();

        // RFC 9457 'instance' names the endpoint that failed, so it is the one field allowed to differ.
        assertThat(withoutInstance(atChange)).isEqualTo(withoutInstance(atSignIn));
        assertThat(atChange).doesNotContain(email).doesNotContain(TEMPORARY).doesNotContain(CHOSEN);
    }

    // --- the new password's policy ---------------------------------------------------------------

    @Test
    @DisplayName("a new password under twelve characters is rejected as invalid input")
    void aShortNewPasswordIsRejected() throws Exception {
        String email = flagged(Role.PARENT);
        MockHttpSession session = signIn(email);
        String hashBefore = storedHash(email);

        mvc.perform(change(session, TEMPORARY, "eleven-char"))
                .andExpect(status().isBadRequest())
                .andExpect(content().contentTypeCompatibleWith("application/problem+json"))
                .andExpect(jsonPath("$.code").value("invalid-input"))
                .andExpect(jsonPath("$.fields[0].field").value("newPassword"))
                .andExpect(jsonPath("$.fields[0].message").value("must be between 12 and 200 characters"));

        assertThat(storedHash(email)).as("a rejected value is never written").isEqualTo(hashBefore);
        assertThat(flagInDatabase(email)).isTrue();
    }

    @Test
    @DisplayName("a missing new password is rejected as invalid input")
    void aMissingNewPasswordIsRejected() throws Exception {
        MockHttpSession session = signIn(flagged(Role.PARENT));

        mvc.perform(change(session, TEMPORARY, ""))
                .andExpect(status().isBadRequest())
                .andExpect(jsonPath("$.code").value("invalid-input"));
    }

    @Test
    @DisplayName("a missing current password is rejected as invalid input, without reaching the account")
    void aMissingCurrentPasswordIsRejected() throws Exception {
        String email = flagged(Role.PARENT);
        MockHttpSession session = signIn(email);

        mvc.perform(change(session, "", CHOSEN))
                .andExpect(status().isBadRequest())
                .andExpect(jsonPath("$.code").value("invalid-input"));
        // BCrypt is salted, so the stored value can never be compared to a fresh encoding of the same
        // password; it is verified the way the application verifies it.
        assertThat(passwords.matches(TEMPORARY, storedHash(email)))
                .as("a rejected request writes nothing")
                .isTrue();
    }

    // --- what the change writes -------------------------------------------------------------------

    @Test
    @DisplayName("the change clears the flag in the database and moves password_changed_at forward")
    void theChangeUpdatesTheStoredAccount() throws Exception {
        String email = flagged(Role.PARENT);
        MockHttpSession session = signIn(email);

        assertThat(passwordChangedAt(email))
                .as("the account was created with a password_changed_at far in the past")
                .isEqualTo(LONG_AGO);

        mvc.perform(change(session, TEMPORARY, CHOSEN)).andExpect(status().isNoContent());

        assertThat(flagInDatabase(email))
                .as("the restriction is lifted")
                .isFalse();
        assertThat(passwordChangedAt(email))
                .as("and the account records when the password was last replaced")
                .isAfter(LONG_AGO);
    }

    @Test
    @DisplayName("the new password is stored only as a BCrypt hash")
    void theNewPasswordIsStoredAsAHash() throws Exception {
        String email = flagged(Role.PARENT);
        MockHttpSession session = signIn(email);

        mvc.perform(change(session, TEMPORARY, CHOSEN)).andExpect(status().isNoContent());

        String stored = storedHash(email);
        assertThat(stored)
                .isNotEqualTo(CHOSEN)
                .isNotEqualTo(TEMPORARY)
                .startsWith("$2")
                .hasSizeLessThanOrEqualTo(100); // the column is VARCHAR(100)
        assertThat(passwords.matches(CHOSEN, stored)).isTrue();
        assertThat(passwords.matches(TEMPORARY, stored)).isFalse();

        // Nothing anywhere in the row is the plaintext: not the hash column, and not a column that was not
        // supposed to hold it either.
        assertThat(jdbc.sql("SELECT * FROM user_account WHERE email = :email")
                .param("email", email)
                .query((rs, n) -> {
                    StringBuilder all = new StringBuilder();
                    var meta = rs.getMetaData();
                    for (int i = 1; i <= meta.getColumnCount(); i++) {
                        all.append(rs.getObject(i)).append(' ');
                    }
                    return all.toString();
                }).single())
                .doesNotContain(CHOSEN)
                .doesNotContain(TEMPORARY);
    }

    @Test
    @DisplayName("the old password stops working and the new one starts")
    void theNewPasswordReplacesTheOld() throws Exception {
        String email = flagged(Role.PARENT);
        MockHttpSession session = signIn(email);

        mvc.perform(change(session, TEMPORARY, CHOSEN)).andExpect(status().isNoContent());

        mvc.perform(postJson(LOGIN, credentials(email, CHOSEN), csrfToken()))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.mustChangePassword").value(false));

        mvc.perform(postJson(LOGIN, credentials(email, TEMPORARY), csrfToken()))
                .andExpect(status().isUnauthorized())
                .andExpect(jsonPath("$.code").value("invalid-credentials"));
    }

    @Test
    @DisplayName("role, status, lock state and failed_logins are untouched by a password change")
    void aPasswordChangeTouchesNothingElse() throws Exception {
        String email = flagged(Role.SUPER_ADMIN);
        MockHttpSession session = signIn(email);
        long id = idOf(email);

        mvc.perform(change(session, TEMPORARY, CHOSEN)).andExpect(status().isNoContent());

        assertThat(textColumn(email, "role")).isEqualTo("SUPER_ADMIN");
        assertThat(textColumn(email, "status")).isEqualTo("ACTIVE");
        assertThat(failedLogins(email)).isZero();
        assertThat(lockedUntil(id))
                .as("a password change neither locks nor unlocks an account")
                .isNull();
    }

    @Test
    @DisplayName("a password change is not a sign-in: last_login_at is left alone")
    void aPasswordChangeIsNotASignIn() throws Exception {
        String email = flagged(Role.PARENT);
        MockHttpSession session = signIn(email);
        long id = idOf(email);
        LocalDateTime lastLoginAfterSignIn = lastLoginAt(id);
        long signInsBefore = countAction(id, "AUTH_LOGIN_SIGNED_IN");

        mvc.perform(change(session, TEMPORARY, CHOSEN)).andExpect(status().isNoContent());

        assertThat(lastLoginAt(id))
                .as("proving and replacing a password is not signing in again")
                .isEqualTo(lastLoginAfterSignIn);
        assertThat(countAction(id, "AUTH_LOGIN_SIGNED_IN"))
                .as("and the trail must not claim a sign-in that did not happen")
                .isEqualTo(signInsBefore);
    }

    // --- the session ------------------------------------------------------------------------------

    @Test
    @DisplayName("the same session carries on working after the change, and is not reissued")
    void theSessionSurvivesTheChange() throws Exception {
        String email = flagged(Role.PARENT);
        MockHttpSession session = signIn(email);
        String idBefore = session.getId();

        mvc.perform(change(session, TEMPORARY, CHOSEN)).andExpect(status().isNoContent());

        assertThat(session.isInvalid()).as("the session is kept, not dropped").isFalse();
        assertThat(session.getId())
                .as("a client part-way through a task keeps its place")
                .isEqualTo(idBefore);
        mvc.perform(get(ME).session(session))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.email").value(email))
                .andExpect(jsonPath("$.mustChangePassword").value(false));
    }

    @Test
    @DisplayName("the session's own principal stops carrying the requirement, not only the column")
    void theSessionPrincipalIsUpdatedToo() throws Exception {
        MockHttpSession session = signIn(flagged(Role.PARENT));

        mvc.perform(change(session, TEMPORARY, CHOSEN)).andExpect(status().isNoContent());

        assertThat(principalMustChangePassword(session))
                .as("otherwise the filter would refuse the next request from an account that has changed it")
                .isFalse();
    }

    @Test
    @DisplayName("a parent reaches its own area after the change, which it could not before")
    void aProtectedRouteOpensAfterTheChange() throws Exception {
        String email = flagged(Role.PARENT);
        MockHttpSession session = signIn(email);

        mvc.perform(get(PARENT_AREA).session(session))
                .andExpect(status().isForbidden())
                .andExpect(jsonPath("$.code").value("password-change-required"));

        mvc.perform(change(session, TEMPORARY, CHOSEN)).andExpect(status().isNoContent());

        // The 404 that follows belongs to a phase that has not started (AGENTS.md §9); what is asserted is
        // that the temporary-password rule is no longer what stops the request.
        mvc.perform(get(PARENT_AREA).session(session))
                .andExpect(result -> assertThat(result.getResponse().getStatus())
                        .as("the request is no longer refused for its password")
                        .isNotIn(401, 403));
    }

    @Test
    @DisplayName("a bootstrapped Super Admin reaches the admin area after the change")
    void aBootstrappedSuperAdminIsUnblockedByTheChange() throws Exception {
        // The situation AdminBootstrap produces: role SUPER_ADMIN, must_change_password true.
        String email = flagged(Role.SUPER_ADMIN);
        MockHttpSession session = signIn(email);

        mvc.perform(get(ADMIN_AREA).session(session))
                .andExpect(status().isForbidden())
                .andExpect(jsonPath("$.code").value("password-change-required"));

        mvc.perform(change(session, TEMPORARY, CHOSEN)).andExpect(status().isNoContent());

        mvc.perform(get(ADMIN_AREA).session(session))
                .andExpect(result -> assertThat(result.getResponse().getStatus())
                        .as("the admin area is open to this account on its own role")
                        .isNotIn(401, 403));
    }

    @Test
    @DisplayName("the wrong role is still refused after a password change")
    void theRoleIsStillCheckedAfterTheChange() throws Exception {
        MockHttpSession session = signIn(flagged(Role.PARENT));

        mvc.perform(change(session, TEMPORARY, CHOSEN)).andExpect(status().isNoContent());

        mvc.perform(get(ADMIN_AREA).session(session))
                .andExpect(status().isForbidden())
                .andExpect(jsonPath("$.code").value("forbidden"));
    }

    // --- who may not do this ------------------------------------------------------------------------

    @Test
    @DisplayName("a caller with no session is refused as unauthenticated")
    void anUnauthenticatedCallerIsRefused() throws Exception {
        mvc.perform(postJson(CHANGE, changeBody(TEMPORARY, CHOSEN), csrfToken()))
                .andExpect(status().isUnauthorized())
                .andExpect(content().contentTypeCompatibleWith("application/problem+json"))
                .andExpect(jsonPath("$.code").value("unauthenticated"));
    }

    @Test
    @DisplayName("the change is refused without the CSRF token, and the session survives the refusal")
    void withoutACsrfTokenTheChangeIsRefused() throws Exception {
        String email = flagged(Role.PARENT);
        MockHttpSession session = signIn(email);

        mvc.perform(postJson(CHANGE, changeBody(TEMPORARY, CHOSEN), null).session(session))
                .andExpect(status().isForbidden())
                .andExpect(jsonPath("$.code").value("forbidden"));

        assertThat(passwords.matches(TEMPORARY, storedHash(email)))
                .as("the refused call wrote nothing")
                .isTrue();
        mvc.perform(get(ME).session(session)).andExpect(status().isOk());
    }

    @Test
    @DisplayName("an account disabled after signing in cannot change its password")
    void aDisabledAccountIsStillRefused() throws Exception {
        String email = flagged(Role.PARENT);
        MockHttpSession session = signIn(email);

        jdbc.sql("UPDATE user_account SET status = 'DISABLED' WHERE email = :email")
                .param("email", email).update();

        mvc.perform(change(session, TEMPORARY, CHOSEN))
                .andExpect(status().isUnauthorized())
                .andExpect(jsonPath("$.code").value("invalid-credentials"));

        assertThat(textColumn(email, "status")).isEqualTo("DISABLED");
        assertThat(flagInDatabase(email)).isTrue();
    }

    @Test
    @DisplayName("an account locked after signing in cannot change its password")
    void aLockedAccountIsStillRefused() throws Exception {
        String email = flagged(Role.PARENT);
        MockHttpSession session = signIn(email);

        jdbc.sql("UPDATE user_account SET locked_until = :until WHERE email = :email")
                .param("until", Timestamps.now().plusMinutes(15)).param("email", email).update();

        mvc.perform(change(session, TEMPORARY, CHOSEN))
                .andExpect(status().isUnauthorized())
                .andExpect(jsonPath("$.code").value("invalid-credentials"));

        assertThat(flagInDatabase(email)).isTrue();
    }

    // --- the trail and the log -----------------------------------------------------------------------

    @Test
    @DisplayName("one secret-free audit row is written for a successful change")
    void aSuccessfulChangeIsAudited() throws Exception {
        String email = flagged(Role.PARENT);
        long id = idOf(email);
        MockHttpSession session = signIn(email);
        long before = countAction(id, "PASSWORD_CHANGED");

        mvc.perform(change(session, TEMPORARY, CHOSEN)).andExpect(status().isNoContent());

        assertThat(countAction(id, "PASSWORD_CHANGED"))
                .as("exactly one row per change")
                .isEqualTo(before + 1);
        String details = jdbc.sql("""
                        SELECT details FROM audit_event
                        WHERE actor_account_id = :id AND action = 'PASSWORD_CHANGED'
                        ORDER BY id DESC LIMIT 1""")
                .param("id", id).query(String.class).optional().orElse("");
        assertThat(details)
                .as("an empty details map is stored as null: there is nothing to say about a password change")
                .doesNotContain(email)
                .doesNotContain(TEMPORARY)
                .doesNotContain(CHOSEN)
                .doesNotContain("$2");
    }

    @Test
    @DisplayName("a refused change is audited by the authentication path, not a second one")
    void aRefusedChangeIsAuditedLikeAnyFailedAttempt() throws Exception {
        String email = flagged(Role.PARENT);
        long id = idOf(email);
        MockHttpSession session = signIn(email);
        long refusalsBefore = countAction(id, "AUTH_LOGIN_REFUSED");
        long changesBefore = countAction(id, "PASSWORD_CHANGED");

        mvc.perform(change(session, "not-the-password", CHOSEN)).andExpect(status().isUnauthorized());

        assertThat(countAction(id, "AUTH_LOGIN_REFUSED"))
                .as("the provider's own refusal row, with no address and no secret in it")
                .isEqualTo(refusalsBefore + 1);
        assertThat(countAction(id, "PASSWORD_CHANGED"))
                .as("and no row claiming a change that did not happen")
                .isEqualTo(changesBefore);

        String details = jdbc.sql("""
                        SELECT details FROM audit_event
                        WHERE actor_account_id = :id AND action = 'AUTH_LOGIN_REFUSED'
                        ORDER BY id DESC LIMIT 1""")
                .param("id", id).query(String.class).single();
        assertThat(details)
                .contains("BAD_PASSWORD")
                .doesNotContain(email)
                .doesNotContain(TEMPORARY)
                .doesNotContain(CHOSEN)
                .doesNotContain("$2");
    }

    @Test
    @DisplayName("no password, hash or address reaches the log on either path")
    void nothingSecretReachesTheLog() throws Exception {
        String email = flagged(Role.PARENT);
        MockHttpSession session = signIn(email);
        String temporaryHash = storedHash(email);

        Logger root = (Logger) LoggerFactory.getLogger(Logger.ROOT_LOGGER_NAME);
        ListAppender<ILoggingEvent> captured = new ListAppender<>();
        captured.start();
        root.addAppender(captured);

        try {
            mvc.perform(change(session, "not-the-password", CHOSEN)).andExpect(status().isUnauthorized());
            mvc.perform(change(session, TEMPORARY, CHOSEN)).andExpect(status().isNoContent());
        } finally {
            root.detachAppender(captured);
            captured.stop();
        }

        String chosenHash = storedHash(email);
        String logged = captured.list.stream()
                .map(ILoggingEvent::getFormattedMessage)
                .collect(Collectors.joining("\n"));

        assertThat(logged)
                .doesNotContain(TEMPORARY)
                .doesNotContain(CHOSEN)
                .doesNotContain("not-the-password")
                .doesNotContain(temporaryHash)
                .doesNotContain(chosenHash)
                .doesNotContain(email);
    }

    @Test
    @DisplayName("the answer to a change carries nothing, and the session holds no hash afterwards")
    void theAnswerAndTheSessionCarryNothing() throws Exception {
        MockHttpSession session = signIn(flagged(Role.PARENT));

        String body = mvc.perform(change(session, TEMPORARY, CHOSEN))
                .andExpect(status().isNoContent())
                .andReturn().getResponse().getContentAsString();

        assertThat(body).isEmpty();
        Object stored = session.getAttribute(
                HttpSessionSecurityContextRepository.SPRING_SECURITY_CONTEXT_KEY);
        var context = (SecurityContext) stored;
        assertThat(((org.clevercubs.platform.security.SessionAuthentication) context.getAuthentication())
                .account().getPassword())
                .as("withPasswordChanged() drops the hash, so the session never carries one")
                .isNull();
    }

    // --- re-authentication is unaffected ---------------------------------------------------------------

    @Test
    @DisplayName("re-authentication still works before and after a change, and is still refused when wrong")
    void reauthenticationIsUnaffected() throws Exception {
        String email = flagged(Role.PARENT);
        MockHttpSession session = signIn(email);

        mvc.perform(postJson(REAUTH, passwordOnly(TEMPORARY), csrfToken()).session(session))
                .andExpect(status().isNoContent());

        mvc.perform(change(session, TEMPORARY, CHOSEN)).andExpect(status().isNoContent());

        mvc.perform(postJson(REAUTH, passwordOnly(TEMPORARY), csrfToken()).session(session))
                .andExpect(status().isUnauthorized())
                .andExpect(jsonPath("$.code").value("invalid-credentials"));
        mvc.perform(postJson(REAUTH, passwordOnly(CHOSEN), csrfToken()).session(session))
                .andExpect(status().isNoContent());
        mvc.perform(get(ME).session(session)).andExpect(status().isOk());
    }

    @Test
    @DisplayName("a re-authentication still proves a password and does not clear the requirement")
    void reauthenticationStillDoesNotClearTheRequirement() throws Exception {
        MockHttpSession session = signIn(flagged(Role.PARENT));

        mvc.perform(postJson(REAUTH, passwordOnly(TEMPORARY), csrfToken()).session(session))
                .andExpect(status().isNoContent());

        assertThat(principalMustChangePassword(session))
                .as("only changing the password ends this state, and that is the point of the new endpoint")
                .isTrue();
        mvc.perform(get(PARENT_AREA).session(session))
                .andExpect(status().isForbidden())
                .andExpect(jsonPath("$.code").value("password-change-required"));
    }

    // --- helpers -------------------------------------------------------------------------------------------

    private MockHttpSession signIn(String email) throws Exception {
        MvcResult result = mvc.perform(postJson(LOGIN, credentials(email, TEMPORARY), csrfToken()))
                .andExpect(status().isOk())
                .andReturn();
        return (MockHttpSession) result.getRequest().getSession(false);
    }

    /** An account that must change its password — the state the bootstrap puts its Super Admin in. */
    private String flagged(Role role) {
        return createAccount(role, "ACTIVE", null, true);
    }

    /** An account with a password of its own choosing. */
    private String ordinary(Role role) {
        return createAccount(role, "ACTIVE", null, false);
    }

    private MockHttpServletRequestBuilder change(MockHttpSession session, String current, String proposed)
            throws Exception {
        return postJson(CHANGE, changeBody(current, proposed), csrfToken()).session(session);
    }

    private static String changeBody(String current, String proposed) {
        return """
                {"currentPassword":"%s","newPassword":"%s"}""".formatted(current, proposed);
    }

    private static String passwordOnly(String password) {
        return """
                {"password":"%s"}""".formatted(password);
    }

    private static String credentials(String email, String password) {
        return """
                {"email":"%s","password":"%s"}""".formatted(email, password);
    }

    /**
     * The real token exchange: a first request is answered with the XSRF-TOKEN cookie, and the token is
     * then sent back in the header. A null token omits both, which is how the refusals are exercised.
     */
    private String csrfToken() throws Exception {
        Cookie cookie = mvc.perform(get(HEALTH)).andReturn().getResponse().getCookie("XSRF-TOKEN");
        assertThat(cookie).as("the CSRF cookie is issued on the first request").isNotNull();
        return cookie.getValue();
    }

    private MockHttpServletRequestBuilder postJson(String path, String body, String csrfToken) {
        MockHttpServletRequestBuilder request = post(path).contentType(MediaType.APPLICATION_JSON);
        if (body != null) {
            request.content(body);
        }
        if (csrfToken != null) {
            request.cookie(new Cookie("XSRF-TOKEN", csrfToken)).header("X-XSRF-TOKEN", csrfToken);
        }
        return request;
    }

    private static String withoutInstance(String problemBody) {
        return problemBody.replaceAll("\"instance\":\"[^\"]*\",", "");
    }

    /**
     * Inserts an account as the bootstrap does, with a BCrypt hash of the temporary password and a
     * {@code password_changed_at} far in the past so that a change to it is unmistakable.
     */
    private String createAccount(Role role, String status, LocalDateTime lockedUntil, boolean mustChangePassword) {
        String email = role.name().toLowerCase() + "-" + UUID.randomUUID() + "@example.test";
        jdbc.sql("""
                        INSERT INTO user_account (email, password_hash, role, status, failed_logins, locked_until,
                                                  must_change_password, password_changed_at, created_at, updated_at)
                        VALUES (:email, :hash, :role, :status, 0, :lockedUntil, :mustChange,
                                :passwordChangedAt, :now, :now)""")
                .param("now", Timestamps.now())
                .param("email", email)
                .param("hash", passwords.encode(TEMPORARY))
                .param("role", role.name())
                .param("status", status)
                .param("lockedUntil", lockedUntil)
                .param("mustChange", mustChangePassword)
                .param("passwordChangedAt", LONG_AGO)
                .update();
        long id = idOf(email);
        createdAccounts.add(id);
        return email;
    }

    private long idOf(String email) {
        return jdbc.sql("SELECT id FROM user_account WHERE email = :email")
                .param("email", email).query(Long.class).single();
    }

    private String emailOf(MockHttpSession session) {
        Object stored = session.getAttribute(
                HttpSessionSecurityContextRepository.SPRING_SECURITY_CONTEXT_KEY);
        var context = (SecurityContext) stored;
        return ((org.clevercubs.platform.security.SessionAuthentication) context.getAuthentication())
                .account().email();
    }

    private String storedHash(String email) {
        return jdbc.sql("SELECT password_hash FROM user_account WHERE email = :email")
                .param("email", email).query(String.class).single();
    }

    private boolean flagInDatabase(String email) {
        return jdbc.sql("SELECT must_change_password FROM user_account WHERE email = :email")
                .param("email", email).query(Boolean.class).single();
    }

    private LocalDateTime passwordChangedAt(String email) {
        return jdbc.sql("SELECT password_changed_at FROM user_account WHERE email = :email")
                .param("email", email).query(LocalDateTime.class).single();
    }

    private LocalDateTime lastLoginAt(long accountId) {
        return jdbc.sql("SELECT last_login_at FROM user_account WHERE id = :id")
                .param("id", accountId).query(LocalDateTime.class).single();
    }

    /**
     * A text column, read as text. {@code query(Object.class)} hands back whatever the driver chose to
     * materialise the value as, which is not necessarily a {@code String} and cannot be compared with
     * {@code isEqualTo} against one.
     */
    private String textColumn(String email, String name) {
        return jdbc.sql("SELECT " + name + " FROM user_account WHERE email = :email")
                .param("email", email).query(String.class).single();
    }

    private int failedLogins(String email) {
        return jdbc.sql("SELECT failed_logins FROM user_account WHERE email = :email")
                .param("email", email).query(Integer.class).single();
    }

    /**
     * A nullable timestamp, read with an explicit type. Asked for as {@code Object.class} the driver hands
     * back a placeholder instance for a NULL rather than {@code null}, and {@code single()} refuses a row that
     * mapped to null, so this goes through {@code optional()} on the way to a plain nullable value.
     */
    private LocalDateTime lockedUntil(long accountId) {
        return jdbc.sql("SELECT locked_until FROM user_account WHERE id = :id")
                .param("id", accountId)
                .query((rs, n) -> rs.getObject("locked_until", LocalDateTime.class))
                .optional()
                .orElse(null);
    }

    private boolean principalMustChangePassword(MockHttpSession session) {
        Object stored = session.getAttribute(
                HttpSessionSecurityContextRepository.SPRING_SECURITY_CONTEXT_KEY);
        var context = (SecurityContext) stored;
        return ((org.clevercubs.platform.security.SessionAuthentication) context.getAuthentication())
                .account().mustChangePassword();
    }

    private long countAction(long accountId, String action) {
        return jdbc.sql("SELECT COUNT(*) FROM audit_event WHERE actor_account_id = :id AND action = :action")
                .param("id", accountId).param("action", action).query(Long.class).single();
    }
}
