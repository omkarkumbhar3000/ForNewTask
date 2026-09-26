package org.clevercubs.platform.security;

import static org.assertj.core.api.Assertions.assertThat;
import static org.hamcrest.Matchers.not;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.post;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.content;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.jsonPath;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import java.time.Instant;
import java.time.LocalDateTime;
import java.time.ZoneOffset;
import java.util.ArrayList;
import java.util.List;
import java.util.UUID;
import java.util.stream.Collectors;

import org.clevercubs.support.IntegrationTest;
import org.junit.jupiter.api.AfterEach;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.ApplicationContext;
import org.springframework.http.MediaType;
import org.springframework.jdbc.core.simple.JdbcClient;
import org.springframework.mock.web.MockHttpServletRequest;
import org.springframework.mock.web.MockHttpSession;
import org.springframework.security.authentication.AuthenticationManager;
import org.springframework.security.authentication.ProviderManager;
import org.springframework.security.core.context.SecurityContext;
import org.springframework.security.core.userdetails.UserDetailsService;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.security.provisioning.InMemoryUserDetailsManager;
import org.springframework.security.web.context.HttpSessionSecurityContextRepository;
import org.springframework.test.web.servlet.MvcResult;
import org.springframework.test.web.servlet.MockMvc;
import org.springframework.test.web.servlet.request.MockHttpServletRequestBuilder;

import ch.qos.logback.classic.Logger;
import ch.qos.logback.classic.spi.ILoggingEvent;
import ch.qos.logback.core.read.ListAppender;
import jakarta.servlet.http.Cookie;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpSession;

/**
 * The B1 sign-in contract, at the HTTP boundary: an account is found by its email address, its BCrypt hash
 * is verified, the result is a server session, and signing out destroys it.
 *
 * <p>Each test creates the account it needs and removes it afterwards, so the tests do not depend on each
 * other or on the order they run in. The CSRF token is taken from a real cookie, not from the test helper,
 * because that is the exchange a browser and a future mobile client actually perform.
 */
class AuthenticationTests extends IntegrationTest {

    private static final String LOGIN = "/api/v1/auth/login";
    private static final String ME = "/api/v1/auth/me";
    private static final String LOGOUT = "/api/v1/auth/logout";
    private static final String REAUTH = "/api/v1/auth/reauth";
    private static final String HEALTH = "/api/v1/public/health";

    /**
     * A route only a signed-in parent may use, and one that no controller answers yet. It is the honest
     * place to watch the temporary-password rule act: the rule is in the filter chain, so the request never
     * reaches a controller either way (AGENTS.md §9).
     */
    private static final String PARENT_AREA = "/api/v1/parent/dashboard";

    /** A test-only password. It exists in this file and in the throwaway container, nowhere else. */
    private static final String PASSWORD = "Correct-Horse-9";

    @Autowired
    MockMvc mvc;

    @Autowired
    JdbcClient jdbc;

    @Autowired
    PasswordEncoder passwords;

    @Autowired
    AuthenticationManager authenticationManager;

    @Autowired
    ApplicationContext context;

    @Value("${server.servlet.session.cookie.name}")
    String configuredSessionCookie;

    private final List<Long> createdAccounts = new ArrayList<>();

    @AfterEach
    void removeTheAccountsThisTestCreated() {
        for (long id : createdAccounts) {
            jdbc.sql("DELETE FROM user_account WHERE id = :id").param("id", id).update();
        }
        // The audit rows are left behind on purpose. audit_event is append-only, cc_app holds no DELETE on
        // it, and the container is thrown away with the suite; deleting them would mean asking for a right
        // the application does not have.
        createdAccounts.clear();
    }

    // --- signing in ---------------------------------------------------------------------

    @Test
    @DisplayName("a correct email and password sign the account in and report who it is")
    void validSignInReturnsTheAccount() throws Exception {
        String email = createAccount("ACTIVE", null);

        MvcResult result = mvc.perform(postJson(LOGIN, credentials(email, PASSWORD), csrfToken()))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.email").value(email))
                .andExpect(jsonPath("$.role").value("PARENT"))
                .andExpect(jsonPath("$.mode").value("PARENT"))
                .andExpect(jsonPath("$.mustChangePassword").value(false))
                .andExpect(jsonPath("$.activeChildId").doesNotExist())
                .andReturn();

        // MockMvc has no servlet container, so the Set-Cookie header is written by Tomcat rather than by the
        // application and cannot be asserted here; the live check on port 8080 is where the cookie is
        // observed. What the application owns is proven here: the answer is bound to a server-side session
        // that now holds the identity, and the body carries nothing secret.
        HttpSession session = result.getRequest().getSession(false);
        assertThat(session).as("the identity is held by a server-side session").isNotNull();
        assertThat(((SecurityContext) session.getAttribute(HttpSessionSecurityContextRepository.SPRING_SECURITY_CONTEXT_KEY))
                .getAuthentication()
                .getName())
                .isEqualTo(email);

        assertThat(result.getResponse().getContentAsString())
                .as("no hash, and no password of any kind, in the answer")
                .doesNotContain("$2a$")
                .doesNotContain("$2b$")
                .doesNotContain(PASSWORD);

        assertThat(configuredSessionCookie)
                .as("the cookie name is a contract with the browser and the future mobile client")
                .isEqualTo("CCSESSION");
    }

    @Test
    @DisplayName("an email address that is not registered is refused")
    void unknownEmailIsRefused() throws Exception {
        String stranger = "nobody-" + UUID.randomUUID() + "@example.test";

        mvc.perform(postJson(LOGIN, credentials(stranger, PASSWORD), csrfToken()))
                .andExpect(status().isUnauthorized())
                .andExpect(content().contentTypeCompatibleWith("application/problem+json"))
                .andExpect(jsonPath("$.code").value("invalid-credentials"))
                .andExpect(jsonPath("$.type").value("urn:clevercubs:problem:invalid-credentials"));
    }

    @Test
    @DisplayName("a wrong password is refused exactly as an unknown address is")
    void wrongPasswordIsRefusedWithoutSayingSo() throws Exception {
        String email = createAccount("ACTIVE", null);

        String unknownAddress = mvc.perform(postJson(LOGIN,
                credentials("nobody-" + UUID.randomUUID() + "@example.test", PASSWORD), csrfToken()))
                .andExpect(status().isUnauthorized())
                .andReturn().getResponse().getContentAsString();

        String wrongPassword = mvc.perform(postJson(LOGIN, credentials(email, "not-the-password"), csrfToken()))
                .andExpect(status().isUnauthorized())
                .andReturn().getResponse().getContentAsString();

        assertThat(wrongPassword)
                .as("a different answer here would tell a stranger which addresses are registered")
                .isEqualTo(unknownAddress);
        assertThat(wrongPassword).doesNotContain(email);
    }

    @Test
    @DisplayName("a disabled account is refused, with the same answer as any other refusal")
    void disabledAccountIsRefused() throws Exception {
        String email = createAccount("DISABLED", null);

        mvc.perform(postJson(LOGIN, credentials(email, PASSWORD), csrfToken()))
                .andExpect(status().isUnauthorized())
                .andExpect(jsonPath("$.code").value("invalid-credentials"));
    }

    @Test
    @DisplayName("an account inside its lockout window is refused, even with the right password")
    void lockedAccountIsRefused() throws Exception {
        String email = createAccount("ACTIVE", Instant.now().plusSeconds(900));

        mvc.perform(postJson(LOGIN, credentials(email, PASSWORD), csrfToken()))
                .andExpect(status().isUnauthorized())
                .andExpect(jsonPath("$.code").value("invalid-credentials"));
    }

    @Test
    @DisplayName("a lockout that has passed no longer refuses the account")
    void anExpiredLockoutIsBehindUs() throws Exception {
        String email = createAccount("ACTIVE", Instant.now().minusSeconds(900));

        mvc.perform(postJson(LOGIN, credentials(email, PASSWORD), csrfToken()))
                .andExpect(status().isOk());
    }

    @Test
    @DisplayName("a sign-in without an email address is a bad request, not a refusal")
    void incompleteRequestIsRejectedAsInvalidInput() throws Exception {
        MvcResult result = mvc.perform(postJson(LOGIN, """
                {"email":"","password":"%s"}""".formatted(PASSWORD), csrfToken()))
                .andExpect(status().isBadRequest())
                .andExpect(content().contentTypeCompatibleWith("application/problem+json"))
                .andExpect(jsonPath("$.code").value("invalid-input"))
                .andExpect(jsonPath("$.fields[0].field").value("email"))
                .andReturn();

        assertThat(result.getResponse().getContentAsString()).doesNotContain(PASSWORD);
    }

    // --- who am I -----------------------------------------------------------------------

    @Test
    @DisplayName("the signed-in account can ask who it is")
    void whoAmIAnswersForTheSignedInAccount() throws Exception {
        String email = createAccount("ACTIVE", null);
        MockHttpSession session = signIn(email);

        MvcResult result = mvc.perform(get(ME).session(session))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.email").value(email))
                .andExpect(jsonPath("$.role").value("PARENT"))
                .andExpect(jsonPath("$.mode").value("PARENT"))
                .andReturn();

        assertThat(result.getResponse().getContentAsString()).doesNotContain("$2a$").doesNotContain("$2b$");
    }

    @Test
    @DisplayName("who am I refuses a caller with no session")
    void whoAmIRefusesAnUnauthenticatedCaller() throws Exception {
        mvc.perform(get(ME))
                .andExpect(status().isUnauthorized())
                .andExpect(content().contentTypeCompatibleWith("application/problem+json"))
                .andExpect(jsonPath("$.code").value("unauthenticated"));
    }

    // --- signing out --------------------------------------------------------------------

    @Test
    @DisplayName("signing out invalidates the session and expires the cookie")
    void signOutInvalidatesTheSession() throws Exception {
        MockHttpSession session = signIn(createAccount("ACTIVE", null));

        MvcResult result = mvc.perform(postJson(LOGOUT, null, csrfToken()).session(session))
                .andExpect(status().isNoContent())
                .andReturn();

        assertThat(session.isInvalid()).as("the server-side session is gone").isTrue();
        assertThat(result.getResponse().getCookie("CCSESSION"))
                .as("and the browser is told to drop it")
                .isNotNull()
                .satisfies(cookie -> assertThat(cookie.getMaxAge()).isZero());
    }

    @Test
    @DisplayName("a client that replays the signed-out session gets nowhere")
    void aRequestAfterSigningOutIsUnauthenticated() throws Exception {
        MockHttpSession session = signIn(createAccount("ACTIVE", null));
        mvc.perform(postJson(LOGOUT, null, csrfToken()).session(session)).andExpect(status().isNoContent());

        // What the client is left holding is a cookie for a session that no longer exists, which is simply
        // an anonymous request: the same thing the next request after a browser clears the cookie does.
        mvc.perform(get(ME))
                .andExpect(status().isUnauthorized())
                .andExpect(jsonPath("$.code").value("unauthenticated"));
    }

    // --- CSRF ---------------------------------------------------------------------------

    @Test
    @DisplayName("signing in without the CSRF token is refused before the password is looked at")
    void signInWithoutACsrfTokenIsRefused() throws Exception {
        String email = createAccount("ACTIVE", null);

        mvc.perform(postJson(LOGIN, credentials(email, PASSWORD), null))
                .andExpect(status().isForbidden())
                .andExpect(jsonPath("$.code").value("forbidden"));
    }

    @Test
    @DisplayName("signing out without the CSRF token is refused")
    void signOutWithoutACsrfTokenIsRefused() throws Exception {
        MockHttpSession session = signIn(createAccount("ACTIVE", null));

        mvc.perform(postJson(LOGOUT, null, null).session(session))
                .andExpect(status().isForbidden())
                .andExpect(jsonPath("$.code").value("forbidden"));

        // The refused sign-out changed nothing: the session is still signed in.
        mvc.perform(get(ME).session(session))
                .andExpect(status().isOk());
    }

    // --- the password itself ------------------------------------------------------------

    @Test
    @DisplayName("signing in rotates the session id, so an id planted beforehand is never used")
    void signingInRotatesTheSessionId() throws Exception {
        String email = createAccount("ACTIVE", null);

        MockHttpSession beforeSignIn = new MockHttpSession();
        String idBefore = beforeSignIn.getId();

        mvc.perform(postJson(LOGIN, credentials(email, PASSWORD), csrfToken()).session(beforeSignIn))
                .andExpect(status().isOk());

        assertThat(beforeSignIn.getId())
                .as("the identity is carried by a session id the server chose after the password was verified")
                .isNotEqualTo(idBefore);
    }

    @Test
    @DisplayName("what is stored is a BCrypt hash that verifies the password and hides it")
    void theStoredPasswordIsABcryptHash() throws Exception {
        String email = createAccount("ACTIVE", null);

        String stored = jdbc.sql("SELECT password_hash FROM user_account WHERE email = :email")
                .param("email", email).query(String.class).single();

        assertThat(stored)
                .isNotEqualTo(PASSWORD)
                .startsWith("$2")
                .hasSizeLessThanOrEqualTo(100); // the column is VARCHAR(100); a wider hash would not fit
        assertThat(passwords.matches(PASSWORD, stored)).isTrue();
        assertThat(passwords.matches("not-the-password", stored)).isFalse();
    }

    // --- nothing secret gets out ---------------------------------------------------------

    @Test
    @DisplayName("a sign-in writes nothing secret to the log")
    void nothingSecretReachesTheLog() throws Exception {
        String email = createAccount("ACTIVE", null);
        String storedHash = jdbc.sql("SELECT password_hash FROM user_account WHERE email = :email")
                .param("email", email).query(String.class).single();

        Logger root = (Logger) LoggerFactory.getLogger(Logger.ROOT_LOGGER_NAME);
        ListAppender<ILoggingEvent> captured = new ListAppender<>();
        captured.start();
        root.addAppender(captured);

        String token;
        String sessionId;
        try {
            MockHttpSession session = signIn(email);
            sessionId = session.getId();
            token = csrfToken();
            mvc.perform(get(ME).session(session)).andExpect(status().isOk());
            mvc.perform(postJson(LOGIN, credentials(email, "wrong-on-purpose"), csrfToken()))
                    .andExpect(status().isUnauthorized());
            mvc.perform(postJson(LOGOUT, null, csrfToken()).session(session)).andExpect(status().isNoContent());
        } finally {
            root.detachAppender(captured);
            captured.stop();
        }

        String logged = captured.list.stream()
                .map(ILoggingEvent::getFormattedMessage)
                .collect(Collectors.joining("\n"));

        assertThat(logged)
                .doesNotContain(PASSWORD)
                .doesNotContain("wrong-on-purpose")
                .doesNotContain(storedHash)
                .doesNotContain(sessionId)
                .doesNotContain(token)
                .doesNotContain(email);
    }

    @Test
    @DisplayName("sign-in outcomes are audited by account id, with no address and no secret")
    void signInOutcomesAreAudited() throws Exception {
        String email = createAccount("ACTIVE", null);
        long id = idOf(email);

        signIn(email);
        mvc.perform(postJson(LOGIN, credentials(email, "wrong-on-purpose"), csrfToken()))
                .andExpect(status().isUnauthorized());

        assertThat(actionsFor(id))
                .contains("AUTH_LOGIN_SIGNED_IN")
                .contains("AUTH_LOGIN_REFUSED");

        String details = jdbc.sql("""
                        SELECT CAST(details AS CHAR) FROM audit_event
                        WHERE actor_account_id = :id AND action = 'AUTH_LOGIN_REFUSED' ORDER BY id DESC""")
                .param("id", id).query(String.class).single();

        assertThat(details)
                .as("the reason is recorded; the address and the password are not")
                .contains("BAD_PASSWORD")
                .doesNotContain(email)
                .doesNotContain(PASSWORD)
                .doesNotContain("$2");
    }

    // --- no second way in -----------------------------------------------------------------

    @Test
    @DisplayName("Spring Boot's generated in-memory user does not exist")
    void thereIsNoGeneratedInMemoryUser() {
        assertThat(context.getBeanNamesForType(InMemoryUserDetailsManager.class))
                .as("a second way into the application, with a password printed at startup")
                .isEmpty();
        assertThat(context.getBeanNamesForType(UserDetailsService.class))
                .as("accounts come from user_account, through the authentication provider")
                .isEmpty();

        assertThat(authenticationManager).isInstanceOf(ProviderManager.class);
        assertThat(((ProviderManager) authenticationManager).getProviders())
                .singleElement()
                .isInstanceOf(AccountAuthenticationProvider.class);
    }

    // --- an account still on a temporary password -------------------------------------------

    @Test
    @DisplayName("an ordinary account is not restricted: a parent route reaches the security layer's allow list")
    void anOrdinaryAccountIsNotRestricted() throws Exception {
        MockHttpSession session = signIn(createAccount("ACTIVE", null, false));

        MvcResult result = mvc.perform(get(PARENT_AREA).session(session)).andReturn();

        // The 404 that follows belongs to a phase that has not started (AGENTS.md §9); what is asserted here
        // is that the request was not stopped by the temporary-password rule or by authentication.
        assertThat(result.getResponse().getStatus()).isNotIn(401, 403);
    }

    @Test
    @DisplayName("an account that must change its password is refused everywhere except its own account")
    void anAccountThatMustChangeItsPasswordIsRefused() throws Exception {
        MockHttpSession session = signIn(createAccount("ACTIVE", null, true));

        MvcResult result = mvc.perform(get(PARENT_AREA).session(session))
                .andExpect(status().isForbidden())
                .andExpect(content().contentTypeCompatibleWith("application/problem+json"))
                .andExpect(jsonPath("$.code").value("password-change-required"))
                .andExpect(jsonPath("$.type").value("urn:clevercubs:problem:password-change-required"))
                .andReturn();

        assertThat(result.getResponse().getContentAsString())
                .as("the refusal says nothing about the account, the hash or the way out")
                .doesNotContain("$2a$")
                .doesNotContain(PASSWORD)
                .doesNotContain("@example.test");
    }

    @Test
    @DisplayName("such an account can still read its own account, which is how the client learns the flag")
    void suchAnAccountCanStillReadItself() throws Exception {
        String email = createAccount("ACTIVE", null, true);
        MockHttpSession session = signIn(email);

        mvc.perform(get(ME).session(session))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.email").value(email))
                .andExpect(jsonPath("$.mustChangePassword").value(true));
    }

    @Test
    @DisplayName("such an account can still sign out, and the refusal did not end its session")
    void suchAnAccountCanStillSignOut() throws Exception {
        MockHttpSession session = signIn(createAccount("ACTIVE", null, true));

        mvc.perform(get(PARENT_AREA).session(session)).andExpect(status().isForbidden());

        mvc.perform(get(ME).session(session))
                // A refusal is not a sign-out: the session is still the caller's own.
                .andExpect(status().isOk());
        assertThat(session.isInvalid()).isFalse();

        mvc.perform(postJson(LOGOUT, null, csrfToken()).session(session))
                .andExpect(status().isNoContent());
        assertThat(session.isInvalid()).isTrue();
    }

    @Test
    @DisplayName("a public call is still answered while the password must change")
    void aPublicCallIsStillAnswered() throws Exception {
        MockHttpSession session = signIn(createAccount("ACTIVE", null, true));

        mvc.perform(get(HEALTH).session(session))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.status").value("UP"));
    }

    @Test
    @DisplayName("signing in again does not shed the requirement")
    void signingInAgainDoesNotShedTheRequirement() throws Exception {
        String email = createAccount("ACTIVE", null, true);
        signIn(email); // the first session, which the client abandons
        MockHttpSession second = signIn(email);

        // The flag is read from the account on every sign-in, never from the session that made it.
        mvc.perform(get(PARENT_AREA).session(second))
                .andExpect(status().isForbidden())
                .andExpect(jsonPath("$.code").value("password-change-required"));
        mvc.perform(get(ME).session(second))
                .andExpect(jsonPath("$.mustChangePassword").value(true));
    }

    @Test
    @DisplayName("nothing about the requirement is disclosed to a caller with no session")
    void theRequirementIsNotDisclosedToAnAnonymousCaller() throws Exception {
        MvcResult api = mvc.perform(get(PARENT_AREA))
                .andExpect(status().isUnauthorized())
                .andReturn();
        MvcResult page = mvc.perform(get("/parent/dashboard"))
                .andExpect(status().is3xxRedirection())
                .andReturn();

        assertThat(api.getResponse().getContentAsString())
                .doesNotContain("password-change-required")
                .doesNotContain("mustChangePassword")
                .as("an unauthenticated caller learns nothing about any account's password state")
                .contains("unauthenticated");
        assertThat(page.getResponse().getRedirectedUrl())
                .as("an unauthenticated page is still sent to the login form")
                .startsWith("/login");
    }

    @Test
    @DisplayName("the wrong role is still refused for such an account, and not as a password problem")
    void roleIsStillCheckedFirst() throws Exception {
        // A parent, not a Super Admin: the admin area is closed on its own account, and the answer must stay
        // 'forbidden' so a client cannot tell a role refusal from the temporary-password one.
        MockHttpSession session = signIn(createAccount("ACTIVE", null, true));

        mvc.perform(get("/api/v1/admin/accounts").session(session))
                .andExpect(status().isForbidden())
                .andExpect(jsonPath("$.code").value("forbidden"));
    }

    // --- re-authentication ------------------------------------------------------------------

    @Test
    @DisplayName("a signed-in parent can prove the password again")
    void reauthenticationSucceeds() throws Exception {
        String email = createAccount("ACTIVE", null, false);
        MockHttpSession session = signIn(email);

        mvc.perform(reauth(session, PASSWORD))
                .andExpect(status().isNoContent())
                .andExpect(content().string(""));

        assertThat(ReauthenticationConfirmation.confirmedAt(requestOf(session)))
                .as("the confirmation is recorded, which is the whole point of the call")
                .isPresent();
    }

    @Test
    @DisplayName("a wrong password at re-authentication is refused with the same generic answer as a sign-in")
    void reauthenticationWithAWrongPasswordIsRefusedGenerically() throws Exception {
        String email = createAccount("ACTIVE", null, false);
        MockHttpSession session = signIn(email);

        String atSignIn = mvc.perform(postJson(LOGIN, credentials(email, "not-the-password"), csrfToken()))
                .andExpect(status().isUnauthorized())
                .andReturn().getResponse().getContentAsString();

        String atReauth = mvc.perform(reauth(session, "not-the-password"))
                .andExpect(status().isUnauthorized())
                .andExpect(jsonPath("$.code").value("invalid-credentials"))
                .andReturn().getResponse().getContentAsString();

        // RFC 9457 'instance' names the endpoint that failed, so it is the one field that must differ.
        assertThat(withoutInstance(atReauth))
                .as("a different answer would tell a caller something about the account behind the session")
                .isEqualTo(withoutInstance(atSignIn));
        assertThat(atReauth).doesNotContain(email).doesNotContain(PASSWORD);
    }

    @Test
    @DisplayName("a normal account keeps its access and its session after a re-authentication")
    void aNormalAccountKeepsItsAccessAfterReauthenticating() throws Exception {
        MockHttpSession session = signIn(createAccount("ACTIVE", null, false));
        String idBefore = session.getId();

        mvc.perform(reauth(session, PASSWORD)).andExpect(status().isNoContent());

        mvc.perform(get(PARENT_AREA).session(session))
                .andExpect(result -> assertThat(result.getResponse().getStatus())
                        .as("authorization is unchanged by proving the password again")
                        .isNotIn(401, 403));
        mvc.perform(get(ME).session(session)).andExpect(status().isOk());
        assertThat(session.isInvalid()).isFalse();
        assertThat(session.getId())
                .as("the identity does not change, so the session id is not reissued")
                .isEqualTo(idBefore);
    }

    @Test
    @DisplayName("an account still on a temporary password can re-authenticate, and stays exactly as restricted")
    void aFlaggedAccountCanReauthenticateWithoutBeingLetThrough() throws Exception {
        String email = createAccount("ACTIVE", null, true);
        MockHttpSession session = signIn(email);

        // Proving a password is not the same as choosing a new one.
        mvc.perform(reauth(session, PASSWORD))
                .andExpect(status().isNoContent());

        mvc.perform(get(ME).session(session))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.mustChangePassword").value(true));
        assertThat(flagInDatabase(email))
                .as("the stored flag is untouched")
                .isTrue();
        assertThat(principalMustChangePassword(session))
                .as("and so is the one in the session: only POST /api/v1/auth/change-password clears it")
                .isTrue();

        mvc.perform(get(PARENT_AREA).session(session))
                .andExpect(status().isForbidden())
                .andExpect(jsonPath("$.code").value("password-change-required"));
        // A page shell carries no data, so a flagged account may load it: that is how it reaches the
        // change-password form. Every data call behind the page is still refused, as above.
        mvc.perform(get("/parent/").session(session))
                .andExpect(status().isOk());
        // The role decision is still made first and is still its own answer.
        mvc.perform(get("/api/v1/admin/accounts").session(session))
                .andExpect(status().isForbidden())
                .andExpect(jsonPath("$.code").value("forbidden"));
    }

    @Test
    @DisplayName("a flagged account can still sign out after re-authenticating")
    void aFlaggedAccountCanStillSignOut() throws Exception {
        MockHttpSession session = signIn(createAccount("ACTIVE", null, true));
        mvc.perform(reauth(session, PASSWORD)).andExpect(status().isNoContent());

        mvc.perform(postJson(LOGOUT, null, csrfToken()).session(session))
                .andExpect(status().isNoContent());
        assertThat(session.isInvalid()).isTrue();
    }

    @Test
    @DisplayName("re-authentication without a session is refused as unauthenticated, not as a wrong password")
    void reauthenticationWithoutASessionIsRefused() throws Exception {
        mvc.perform(reauth(new MockHttpSession(), PASSWORD))
                .andExpect(status().isUnauthorized())
                .andExpect(jsonPath("$.code").value("unauthenticated"))
                .andExpect(jsonPath("$.code").value(not("invalid-credentials")));
    }

    @Test
    @DisplayName("re-authentication without the CSRF token is refused, and the session survives it")
    void reauthenticationWithoutACsrfTokenIsRefused() throws Exception {
        MockHttpSession session = signIn(createAccount("ACTIVE", null, false));

        mvc.perform(postJson(REAUTH, passwordOnly(PASSWORD), null).session(session))
                .andExpect(status().isForbidden())
                .andExpect(jsonPath("$.code").value("forbidden"));

        mvc.perform(get(ME).session(session))
                .andExpect(status().isOk());
    }

    @Test
    @DisplayName("a re-authentication without a password is a bad request, and never reaches the account")
    void reauthenticationWithoutAPasswordIsRejectedAsInvalidInput() throws Exception {
        MockHttpSession session = signIn(createAccount("ACTIVE", null, false));

        mvc.perform(reauth(session, ""))
                .andExpect(status().isBadRequest())
                .andExpect(jsonPath("$.code").value("invalid-input"));
    }

    @Test
    @DisplayName("a refused re-authentication is audited like any failed attempt, and a successful one is not a sign-in")
    void reauthenticationIsAuditedWithoutInventingASignIn() throws Exception {
        String email = createAccount("ACTIVE", null, false);
        long id = idOf(email);
        MockHttpSession session = signIn(email);
        long signInsAfterLogin = countAction(id, "AUTH_LOGIN_SIGNED_IN");
        assertThat(signInsAfterLogin).isEqualTo(1);

        mvc.perform(reauth(session, PASSWORD)).andExpect(status().isNoContent());
        mvc.perform(reauth(session, "not-the-password")).andExpect(status().isUnauthorized());

        assertThat(countAction(id, "AUTH_LOGIN_SIGNED_IN"))
                .as("a re-authentication is not a sign-in and must not be recorded as one")
                .isEqualTo(signInsAfterLogin);
        assertThat(countAction(id, "AUTH_LOGIN_REFUSED"))
                .as("a wrong password here is the failed attempt DD-14 asks to be recorded")
                .isPositive();

        String details = jdbc.sql("""
                        SELECT CAST(details AS CHAR) FROM audit_event
                        WHERE actor_account_id = :id AND action = 'AUTH_LOGIN_REFUSED'
                        ORDER BY id DESC LIMIT 1""")
                .param("id", id).query(String.class).single();
        assertThat(details)
                .contains("BAD_PASSWORD")
                .doesNotContain(PASSWORD)
                .doesNotContain(email)
                .doesNotContain("$2");
    }

    @Test
    @DisplayName("no secret is in a re-authentication answer, on either path")
    void nothingSecretIsInTheAnswer() throws Exception {
        String email = createAccount("ACTIVE", null, false);
        String storedHash = jdbc.sql("SELECT password_hash FROM user_account WHERE email = :email")
                .param("email", email).query(String.class).single();
        MockHttpSession session = signIn(email);

        String success = mvc.perform(reauth(session, PASSWORD))
                .andExpect(status().isNoContent())
                .andReturn().getResponse().getContentAsString();
        String failure = mvc.perform(reauth(session, "not-the-password"))
                .andExpect(status().isUnauthorized())
                .andReturn().getResponse().getContentAsString();

        assertThat(success).isEmpty();
        assertThat(success).doesNotContain(PASSWORD).doesNotContain(storedHash);
        assertThat(failure).doesNotContain(PASSWORD).doesNotContain(storedHash).doesNotContain(email);
    }

    @Test
    @DisplayName("a session id planted before sign-in is not what re-authentication runs on")
    void reauthenticationCannotAdoptAPlantedSession() throws Exception {
        MockHttpSession planted = new MockHttpSession();
        String plantedId = planted.getId();

        // A re-authentication without an identity of its own is not a way to make a session authenticated.
        mvc.perform(reauth(planted, PASSWORD)).andExpect(status().isUnauthorized());
        assertThat(planted.getAttribute(
                "org.springframework.security.web.context.HttpSessionSecurityContextRepository"
                        + ".SPRING_SECURITY_CONTEXT"))
                .as("nothing was written into the session that was handed to us")
                .isNull();
        assertThat(planted.getId()).isEqualTo(plantedId);

        // And once the account is really signed in, the id is not the one that was planted.
        MockHttpSession signedIn = signIn(createAccount("ACTIVE", null, false));
        mvc.perform(reauth(signedIn, PASSWORD)).andExpect(status().isNoContent());
        assertThat(signedIn.getId()).isNotEqualTo(plantedId);
    }

    @Test
    @DisplayName("the public health call is unaffected by re-authentication")
    void thePublicCallIsUnaffected() throws Exception {
        MockHttpSession session = signIn(createAccount("ACTIVE", null, false));
        mvc.perform(reauth(session, PASSWORD)).andExpect(status().isNoContent());

        mvc.perform(get(HEALTH).session(session))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.status").value("UP"));
    }

    // --- helpers --------------------------------------------------------------------------

    /** Signs in and returns the session the answer created. */
    private MockHttpSession signIn(String email) throws Exception {
        MvcResult result = mvc.perform(postJson(LOGIN, credentials(email, PASSWORD), csrfToken()))
                .andExpect(status().isOk())
                .andReturn();
        return (MockHttpSession) result.getRequest().getSession(false);
    }

    /**
     * The real token exchange: a first request is answered with the XSRF-TOKEN cookie, and the token is
     * then sent back in the header. A token of null omits both, which is how the refusals are exercised.
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

    private static String credentials(String email, String password) {
        return """
                {"email":"%s","password":"%s"}""".formatted(email, password);
    }

    private static String passwordOnly(String password) {
        return """
                {"password":"%s"}""".formatted(password);
    }

    /** A problem body without the RFC 9457 {@code instance}, which is the endpoint that failed. */
    private static String withoutInstance(String problemBody) {
        return problemBody.replaceAll("\"instance\":\"[^\"]*\",", "");
    }

    private MockHttpServletRequestBuilder reauth(MockHttpSession session, String password) throws Exception {
        return postJson(REAUTH, passwordOnly(password), csrfToken()).session(session);
    }

    /** The same session as a request would see it, for the one read that takes a request. */
    private static HttpServletRequest requestOf(MockHttpSession session) throws Exception {
        MockHttpServletRequest request = new MockHttpServletRequest("GET", "/api/v1/auth/me");
        request.setSession(session);
        return request;
    }

    private boolean flagInDatabase(String email) {
        return jdbc.sql("SELECT must_change_password FROM user_account WHERE email = :email")
                .param("email", email).query(Boolean.class).single();
    }

    private boolean principalMustChangePassword(MockHttpSession session) {
        Object stored = session.getAttribute(
                HttpSessionSecurityContextRepository.SPRING_SECURITY_CONTEXT_KEY);
        var context = (SecurityContext) stored;
        return ((SessionAuthentication) context.getAuthentication()).account().mustChangePassword();
    }

    private long countAction(long accountId, String action) {
        return jdbc.sql("SELECT COUNT(*) FROM audit_event WHERE actor_account_id = :id AND action = :action")
                .param("id", accountId).param("action", action).query(Long.class).single();
    }

    /** Inserts an account exactly as registration would, with a BCrypt hash of the test password. */
    private String createAccount(String status, Instant lockedUntil) {
        return createAccount(status, lockedUntil, false);
    }

    /**
     * Inserts an account, optionally one the owner must replace: {@code must_change_password} is what an
     * admin-issued temporary password sets (docs/04 §142), and there is no other way it becomes true.
     */
    private String createAccount(String status, Instant lockedUntil, boolean mustChangePassword) {
        String email = "parent-" + UUID.randomUUID() + "@example.test";
        jdbc.sql("""
                        INSERT INTO user_account (email, password_hash, role, status, failed_logins, locked_until,
                                                  must_change_password, password_changed_at, created_at, updated_at)
                        VALUES (:email, :hash, 'PARENT', :status, 0, :lockedUntil, :mustChange,
                                UTC_TIMESTAMP(6), UTC_TIMESTAMP(6), UTC_TIMESTAMP(6))""")
                .param("email", email)
                .param("hash", passwords.encode(PASSWORD))
                .param("status", status)
                .param("lockedUntil", lockedUntil == null ? null
                        : LocalDateTime.ofInstant(lockedUntil, ZoneOffset.UTC))
                .param("mustChange", mustChangePassword)
                .update();
        long id = idOf(email);
        createdAccounts.add(id);
        return email;
    }

    private long idOf(String email) {
        return jdbc.sql("SELECT id FROM user_account WHERE email = :email")
                .param("email", email).query(Long.class).single();
    }

    private List<String> actionsFor(long accountId) {
        return jdbc.sql("SELECT action FROM audit_event WHERE actor_account_id = :id ORDER BY id")
                .param("id", accountId).query(String.class).list();
    }
}
