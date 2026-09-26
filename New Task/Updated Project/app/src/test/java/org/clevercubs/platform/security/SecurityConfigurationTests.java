package org.clevercubs.platform.security;

import static org.assertj.core.api.Assertions.assertThat;
import static org.springframework.security.test.web.servlet.request.SecurityMockMvcRequestPostProcessors.authentication;
import static org.clevercubs.support.Journeys.realCsrf;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.post;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.content;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.header;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.jsonPath;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import java.net.URLDecoder;
import java.nio.charset.StandardCharsets;

import org.clevercubs.support.IntegrationTest;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpHeaders;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.test.web.servlet.MockMvc;
import org.springframework.test.web.servlet.MvcResult;

/**
 * The B1 security contract, checked at the HTTP boundary: what an unauthenticated caller sees, what the
 * wrong role sees, and which headers and CSRF rules the chain enforces.
 *
 * <p>Where a request is meant to reach a controller that B1 has not built yet, the assertion is that the
 * security layer let it through (neither 401 nor 403). That is the part this test class owns; the 404 that
 * follows belongs to a later phase and is not asserted here.
 */
class SecurityConfigurationTests extends IntegrationTest {

    private static final String HEALTH = "/api/v1/public/health";

    @Autowired
    MockMvc mvc;

    @Autowired
    PasswordEncoder passwords;

    private static AccountPrincipal account(long id, Role role) {
        return new AccountPrincipal(id, id + "@example.test", null, role, true, null, false);
    }

    private static SessionAuthentication parent() {
        return SessionAuthentication.signedIn(account(1L, Role.PARENT));
    }

    private static SessionAuthentication admin() {
        return SessionAuthentication.signedIn(account(2L, Role.SUPER_ADMIN));
    }

    private static SessionAuthentication childOfParent() {
        return SessionAuthentication.childMode(account(1L, Role.PARENT), 42L);
    }

    /** The request got past the security filters, whatever the controller layer then did with it. */
    private static void assertPassedSecurity(MvcResult result) {
        assertThat(result.getResponse().getStatus())
                .as("security layer should have allowed this request")
                .isNotIn(401, 403);
    }

    // --- what is open ---------------------------------------------------------------

    @Test
    @DisplayName("the health endpoint is public, and proves the database is reachable")
    void healthIsPublic() throws Exception {
        mvc.perform(get(HEALTH))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.status").value("UP"));
    }

    @Test
    @DisplayName("no WWW-Authenticate challenge, so HTTP Basic is not switched on")
    void httpBasicIsNotOffered() throws Exception {
        mvc.perform(get("/api/v1/auth/me"))
                .andExpect(status().isUnauthorized())
                .andExpect(header().doesNotExist(HttpHeaders.WWW_AUTHENTICATE));
    }

    @Test
    @DisplayName("signing in is the one POST a stranger may make")
    void loginEndpointIsReachableWithoutASession() throws Exception {
        MvcResult result = mvc.perform(post("/api/v1/auth/login").with(realCsrf())).andReturn();
        assertPassedSecurity(result);
    }

    // --- what a stranger is refused --------------------------------------------------

    @Test
    @DisplayName("an unauthenticated API call is 401 problem+json, never an HTML redirect")
    void unauthenticatedApiCallIsProblemJson() throws Exception {
        mvc.perform(get("/api/v1/auth/me"))
                .andExpect(status().isUnauthorized())
                .andExpect(content().contentTypeCompatibleWith("application/problem+json"))
                .andExpect(jsonPath("$.status").value(401))
                .andExpect(jsonPath("$.code").value("unauthenticated"))
                .andExpect(jsonPath("$.type").value("urn:clevercubs:problem:unauthenticated"))
                .andExpect(jsonPath("$.detail").isNotEmpty());
    }

    @Test
    @DisplayName("an unauthenticated page call is 302 to /login with the page in next")
    void unauthenticatedPageRedirectsToLogin() throws Exception {
        mvc.perform(get("/parent/dashboard"))
                .andExpect(status().is3xxRedirection())
                .andExpect(header().string(HttpHeaders.LOCATION,
                        org.hamcrest.Matchers.startsWith("/login?next=")));
    }

    @Test
    @DisplayName("next keeps the path and query the caller asked for")
    void nextKeepsPathAndQuery() throws Exception {
        MvcResult result = mvc.perform(get("/learn/lesson/7").queryParam("a", "b"))
                .andExpect(status().is3xxRedirection())
                .andReturn();

        String location = result.getResponse().getHeader(HttpHeaders.LOCATION);
        String encoded = location.substring("/login?next=".length());
        assertThat(URLDecoder.decode(encoded, StandardCharsets.UTF_8)).isEqualTo("/learn/lesson/7?a=b");
    }

    @Test
    @DisplayName("an unmapped path is closed by default, not open")
    void unmappedPathStillRequiresASession() throws Exception {
        mvc.perform(get("/nothing/here"))
                .andExpect(status().is3xxRedirection())
                .andExpect(header().string(HttpHeaders.LOCATION,
                        org.hamcrest.Matchers.startsWith("/login?next=")));
    }

    // --- roles -----------------------------------------------------------------------

    @Test
    @DisplayName("a parent passes its own area")
    void parentReachesParentArea() throws Exception {
        assertPassedSecurity(mvc.perform(get("/api/v1/parent/children")
                .with(authentication(parent()))).andReturn());
    }

    @Test
    @DisplayName("a parent is 403 in the child area, with problem+json")
    void parentIsRefusedInChildArea() throws Exception {
        mvc.perform(get("/api/v1/learn/session").with(authentication(parent())))
                .andExpect(status().isForbidden())
                .andExpect(content().contentTypeCompatibleWith("application/problem+json"))
                .andExpect(jsonPath("$.code").value("forbidden"));
    }

    @Test
    @DisplayName("a child session drops the parent authority, so child mode cannot reach the parent area")
    void childModeCannotReachParentArea() throws Exception {
        mvc.perform(get("/api/v1/parent/children").with(authentication(childOfParent())))
                .andExpect(status().isForbidden())
                .andExpect(jsonPath("$.code").value("forbidden"));
    }

    @Test
    @DisplayName("a child session reaches the child area")
    void childModeReachesChildArea() throws Exception {
        assertPassedSecurity(mvc.perform(get("/api/v1/learn/session")
                .with(authentication(childOfParent()))).andReturn());
    }

    @Test
    @DisplayName("a parent is 403 in the admin area")
    void parentIsRefusedInAdminArea() throws Exception {
        mvc.perform(get("/api/v1/admin/settings").with(authentication(parent())))
                .andExpect(status().isForbidden());
    }

    @Test
    @DisplayName("a Super Admin passes the admin area")
    void adminReachesAdminArea() throws Exception {
        assertPassedSecurity(mvc.perform(get("/api/v1/admin/settings")
                .with(authentication(admin()))).andReturn());
    }

    // --- CSRF ------------------------------------------------------------------------

    @Test
    @DisplayName("a state-changing POST without the CSRF token is 403")
    void postWithoutCsrfTokenIsRefused() throws Exception {
        mvc.perform(post("/api/v1/parent/children").with(authentication(parent())))
                .andExpect(status().isForbidden())
                .andExpect(content().contentTypeCompatibleWith("application/problem+json"))
                .andExpect(jsonPath("$.code").value("forbidden"));
    }

    @Test
    @DisplayName("the same POST with the CSRF token passes the security layer")
    void postWithCsrfTokenIsAccepted() throws Exception {
        assertPassedSecurity(mvc.perform(post("/api/v1/parent/children")
                .with(authentication(parent()))
                .with(realCsrf())).andReturn());
    }

    // --- headers ---------------------------------------------------------------------

    @Test
    @DisplayName("responses carry the hardened header set")
    void securityHeadersArePresent() throws Exception {
        mvc.perform(get(HEALTH))
                .andExpect(header().string("Content-Security-Policy",
                        org.hamcrest.Matchers.containsString("default-src 'self'")))
                .andExpect(header().string("Content-Security-Policy",
                        org.hamcrest.Matchers.not(org.hamcrest.Matchers.containsString("unsafe-inline"))))
                .andExpect(header().string("X-Content-Type-Options", "nosniff"))
                .andExpect(header().string("X-Frame-Options", "DENY"))
                .andExpect(header().string("Referrer-Policy", "same-origin"));
    }

    // --- password storage -------------------------------------------------------------

    @Test
    @DisplayName("the password encoder is BCrypt, so the stored value is neither plain nor reversible")
    void passwordEncoderIsBcrypt() {
        String hash = passwords.encode("correct horse battery staple");

        assertThat(passwords).isInstanceOf(
                org.springframework.security.crypto.bcrypt.BCryptPasswordEncoder.class);
        assertThat(hash).isNotEqualTo("correct horse battery staple").startsWith("$2");
        assertThat(passwords.matches("correct horse battery staple", hash)).isTrue();
        assertThat(passwords.matches("wrong password", hash)).isFalse();
    }
}
