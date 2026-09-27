package org.clevercubs.platform;

import static org.assertj.core.api.Assertions.assertThat;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.header;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.jsonPath;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import org.clevercubs.support.IntegrationTest;
import org.clevercubs.support.Journeys;
import org.clevercubs.support.Journeys.Family;
import org.junit.jupiter.api.AfterEach;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.ValueSource;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpHeaders;
import org.springframework.jdbc.core.simple.JdbcClient;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.test.web.servlet.MockMvc;
import org.springframework.test.web.servlet.MvcResult;

/** The page routes, static assets and the media library (requirement sections 8, 20 and 25). */
class PagesAndMediaTests extends IntegrationTest {

    @Autowired
    MockMvc mvc;

    @Autowired
    JdbcClient jdbc;

    @Autowired
    PasswordEncoder passwords;

    Journeys journeys;

    @BeforeEach
    void setUp() {
        journeys = new Journeys(mvc, jdbc, passwords);
    }

    @AfterEach
    void cleanUp() {
        journeys.cleanUp();
    }

    @ParameterizedTest
    @ValueSource(strings = {"/", "/login", "/register", "/terms", "/privacy", "/contact"})
    @DisplayName("the public pages open without signing in")
    void publicPages(String path) throws Exception {
        mvc.perform(get(path)).andExpect(status().isOk());
    }

    @ParameterizedTest
    @ValueSource(strings = {"/css/app.css", "/js/api.js", "/js/pages/welcome.js", "/img/logo-96.png",
        "/fonts/fredoka.woff2", "/index.html", "/404.html"})
    @DisplayName("styles, scripts, images and fonts are public, with the security headers")
    void staticAssets(String path) throws Exception {
        mvc.perform(get(path))
                .andExpect(status().isOk())
                .andExpect(header().string("X-Content-Type-Options", "nosniff"));
    }

    @ParameterizedTest
    @ValueSource(strings = {"/parent/", "/parent/child.html", "/learn/", "/learn/quiz.html", "/admin/",
        "/media/alphabets/apple.png"})
    @DisplayName("a protected page or media file without a session redirects to login (section 8)")
    void protectedPagesRedirect(String path) throws Exception {
        MvcResult r = mvc.perform(get(path)).andExpect(status().is3xxRedirection()).andReturn();
        assertThat(r.getResponse().getHeader(HttpHeaders.LOCATION)).startsWith("/login?next=");
    }

    @Test
    @DisplayName("a signed-in session can stream media; traversal outside the media folder is refused")
    void mediaForSignedInUsers() throws Exception {
        Family f = journeys.family(4);
        mvc.perform(get("/media/alphabets/apple.png").session(f.session()))
                .andExpect(status().isOk())
                .andExpect(header().string("Content-Type", "image/png"));
        mvc.perform(get("/media/rhymes/twinkal-v.mp4").header(HttpHeaders.RANGE, "bytes=0-99").session(f.session()))
                .andExpect(status().isPartialContent());
        int traversal = mvc.perform(get("/media/..%2F..%2Fapp%2Fpom.xml").session(f.session())).andReturn()
                .getResponse().getStatus();
        assertThat(traversal).isIn(400, 404);
    }

    @Test
    @DisplayName("the public session check answers without a 401 and never shows the parent's email to a child")
    void sessionCheck() throws Exception {
        mvc.perform(get("/api/v1/public/session")).andExpect(status().isOk())
                .andExpect(jsonPath("$.signedIn").value(false));
        Family f = journeys.family(4);
        mvc.perform(get("/api/v1/public/session").session(f.session()))
                .andExpect(jsonPath("$.signedIn").value(true))
                .andExpect(jsonPath("$.email").value(f.email()));
        journeys.enterChildMode(f);
        mvc.perform(get("/api/v1/public/session").session(f.session()))
                .andExpect(jsonPath("$.mode").value("CHILD"))
                .andExpect(jsonPath("$.email").doesNotExist());
    }

    @Test
    @DisplayName("a page of the wrong area is refused with 403, not shown")
    void wrongAreaPage() throws Exception {
        Family f = journeys.family(4);
        mvc.perform(get("/admin/").session(f.session())).andExpect(status().isForbidden());
        journeys.enterChildMode(f);
        mvc.perform(get("/parent/").session(f.session())).andExpect(status().isForbidden());
    }

    @Test
    @DisplayName("the catalogue and the supported ages are public and carry no personal data")
    void publicCatalogue() throws Exception {
        mvc.perform(get("/api/v1/public/courses"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.length()").value(11))
                .andExpect(jsonPath("$[0].title").isNotEmpty());
        mvc.perform(get("/api/v1/public/ages"))
                .andExpect(jsonPath("$.minAge").value(2))
                .andExpect(jsonPath("$.maxAge").value(8));
    }

    @Test
    @DisplayName("the contact endpoint lists the configured addresses (D80)")
    void contactAddresses() throws Exception {
        mvc.perform(get("/api/v1/public/contact"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.configured").value(true))
                .andExpect(jsonPath("$.emails.length()").value(1))
                .andExpect(jsonPath("$.emails[0]").value("hello@clevercubs.test"))
                .andExpect(jsonPath("$.email").value("hello@clevercubs.test"));
    }
}
