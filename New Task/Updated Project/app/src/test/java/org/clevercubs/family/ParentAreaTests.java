package org.clevercubs.family;

import static org.assertj.core.api.Assertions.assertThat;
import static org.clevercubs.support.Journeys.json;
import static org.clevercubs.support.Journeys.realCsrf;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.delete;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.patch;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.post;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.jsonPath;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import java.time.Instant;
import java.time.LocalDate;
import java.util.List;

import org.clevercubs.support.IntegrationTest;
import org.clevercubs.support.Journeys;
import org.clevercubs.support.Journeys.Family;
import org.junit.jupiter.api.AfterEach;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.jdbc.core.simple.JdbcClient;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.test.web.servlet.MockMvc;
import org.springframework.test.web.servlet.MvcResult;

/** Requirement sections 7, 12, 15 and 16, and the privacy rights of D67. */
class ParentAreaTests extends IntegrationTest {

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

    @Test
    @DisplayName("the overview lists the parent's own children with progress at a glance")
    void overview() throws Exception {
        Family f = journeys.family(4);
        MvcResult r = journeys.getJson(f.session(), "/api/v1/parent/overview");
        assertThat(r.getResponse().getStatus()).isEqualTo(200);
        assertThat(Journeys.<String>read(r, "$.parentName")).isEqualTo("Pat Parent");
        assertThat(Journeys.<List<Object>>read(r, "$.children")).hasSize(1);
        assertThat(Journeys.<Integer>read(r, "$.children[0].overallPercent")).isZero();
    }

    @Test
    @DisplayName("a parent can add a second child and edit a child's profile and preferences")
    void addAndEditChild() throws Exception {
        Family f = journeys.family(4);
        MvcResult added = mvc.perform(json(post("/api/v1/parent/children"),
                "{\"firstName\":\"Leo\",\"dateOfBirth\":\"" + LocalDate.now().minusYears(7) + "\",\"avatarCode\":\"lion\"}")
                .session(f.session())).andReturn();
        assertThat(added.getResponse().getStatus()).isEqualTo(201);
        assertThat(Journeys.<String>read(added, "$.ageGroupCode")).isEqualTo("BIG");

        mvc.perform(json(patch("/api/v1/parent/children/" + f.childId()),
                        "{\"displayName\":\"Zo\",\"soundEffects\":false,\"avatarCode\":\"panda\"}").session(f.session()))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.displayName").value("Zo"))
                .andExpect(jsonPath("$.soundEffects").value(false))
                .andExpect(jsonPath("$.avatar").value("🐼"));
    }

    @Test
    @DisplayName("another family's child is not found: read, edit, delete, export and grant (IDOR, SEC-E04)")
    void otherFamiliesAreInvisible() throws Exception {
        Family a = journeys.family(4);
        Family b = journeys.family(5);
        String other = "/api/v1/parent/children/" + b.childId();
        mvc.perform(get(other).session(a.session())).andExpect(status().isNotFound());
        mvc.perform(json(patch(other), "{\"displayName\":\"x\"}").session(a.session())).andExpect(status().isNotFound());
        mvc.perform(delete(other).with(realCsrf()).session(a.session())).andExpect(status().isNotFound());
        mvc.perform(get(other + "/export").session(a.session())).andExpect(status().isNotFound());
        mvc.perform(get(other + "/year-summary").session(a.session())).andExpect(status().isNotFound());
        assertThat(jdbc.sql("SELECT display_name FROM child WHERE id = :c").param("c", b.childId())
                .query(String.class).single()).isEqualTo("Zoe");
    }

    @Test
    @DisplayName("feedback is stored as text and only the author and the Super Admin can read it")
    void feedbackVisibility() throws Exception {
        Family f = journeys.family(4);
        mvc.perform(json(post("/api/v1/parent/feedback"),
                        "{\"category\":\"USABILITY\",\"rating\":5,\"message\":\"<b>Lovely</b> app\"}").session(f.session()))
                .andExpect(status().isCreated())
                .andExpect(jsonPath("$.message").value("<b>Lovely</b> app"));
        mvc.perform(get("/api/v1/parent/feedback").session(f.session()))
                .andExpect(jsonPath("$[0].category").value("USABILITY"));

        journeys.enterChildMode(f);
        mvc.perform(get("/api/v1/parent/feedback").session(f.session())).andExpect(status().isForbidden());

        MvcResult admin = journeys.getJson(journeys.admin(), "/api/v1/admin/feedback");
        List<String> messages = Journeys.read(admin, "$[*].message");
        assertThat(messages).contains("<b>Lovely</b> app");
    }

    @Test
    @DisplayName("export and delete need a recent password; after re-authentication they work (DD-02)")
    void sensitiveActionsNeedARecentPassword() throws Exception {
        Family f = journeys.family(4);
        f.session().setAttribute("clevercubs.password-confirmed-at", Instant.now().minusSeconds(3600));
        mvc.perform(get("/api/v1/parent/children/" + f.childId() + "/export").session(f.session()))
                .andExpect(status().isForbidden())
                .andExpect(jsonPath("$.code").value("reauth-required"));

        mvc.perform(json(post("/api/v1/auth/reauth"), "{\"password\":\"" + Journeys.PASSWORD + "\"}").session(f.session()))
                .andExpect(status().isNoContent());
        MvcResult export = mvc.perform(get("/api/v1/parent/children/" + f.childId() + "/export").session(f.session()))
                .andReturn();
        assertThat(export.getResponse().getStatus()).isEqualTo(200);
        assertThat(export.getResponse().getHeader("Content-Disposition")).contains("attachment");
        assertThat(Journeys.<String>read(export, "$.child.firstName")).isEqualTo("Zoe");

        mvc.perform(delete("/api/v1/parent/children/" + f.childId()).with(realCsrf()).session(f.session()))
                .andExpect(status().isNoContent());
        assertThat(jdbc.sql("SELECT COUNT(*) FROM child WHERE id = :c").param("c", f.childId())
                .query(Integer.class).single()).isZero();
        assertThat(jdbc.sql("SELECT COUNT(*) FROM audit_event WHERE action = 'CHILD_DELETED' AND target_id = :c")
                .param("c", f.childId()).query(Integer.class).single()).isEqualTo(1);
    }

    @Test
    @DisplayName("the year summary reports plain facts and the next-year decision waits for completion")
    void yearSummary() throws Exception {
        Family f = journeys.family(4);
        MvcResult r = journeys.getJson(f.session(), "/api/v1/parent/children/" + f.childId() + "/year-summary");
        assertThat(r.getResponse().getStatus()).isEqualTo(200);
        assertThat(Journeys.<Integer>read(r, "$.coursesTotal")).isEqualTo(11);
        assertThat(Journeys.<String>read(r, "$.status")).isEqualTo("ACTIVE");
        assertThat(Journeys.<List<String>>read(r, "$.needsAttention")).isNotEmpty();
        mvc.perform(json(post("/api/v1/parent/children/" + f.childId() + "/next-year"), "{\"decision\":\"CONTINUE\"}")
                        .session(f.session()))
                .andExpect(status().is(422))
                .andExpect(jsonPath("$.code").value("program-not-complete"));
    }

    @Test
    @DisplayName("completing every course completes the year, issues a certificate and opens the decision")
    void completingTheYear() throws Exception {
        Family f = journeys.family(4);
        journeys.enterChildMode(f);
        List<String> slugs = jdbc.sql("SELECT slug FROM course WHERE status = 'PUBLISHED' ORDER BY sort_order")
                .query(String.class).list();
        for (String slug : slugs) {
            journeys.finishLessons(f, slug);
            List<Long> quiz = jdbc.sql("SELECT q.id FROM quiz q JOIN course c ON c.id = q.course_id WHERE c.slug = :s")
                    .param("s", slug).query(Long.class).list();
            if (!quiz.isEmpty()) {
                journeys.answerAll(f, journeys.startQuiz(f, quiz.getFirst()), quiz.getFirst(), 10);
            }
        }
        MvcResult home = journeys.getJson(f.session(), "/api/v1/learn/home");
        assertThat(Journeys.<Boolean>read(home, "$.programCompleted")).isTrue();
        assertThat(Journeys.<Integer>read(home, "$.programPercent")).isEqualTo(100);

        journeys.backToParent(f);
        MvcResult summary = journeys.getJson(f.session(), "/api/v1/parent/children/" + f.childId() + "/year-summary");
        assertThat(Journeys.<String>read(summary, "$.status")).isEqualTo("COMPLETED");
        assertThat(Journeys.<List<Object>>read(summary, "$.certificates")).hasSize(1);
        assertThat(Journeys.<String>read(summary, "$.certificates[0].verificationCode")).hasSize(16);
        mvc.perform(json(post("/api/v1/parent/children/" + f.childId() + "/next-year"), "{\"decision\":\"CONTINUE\"}")
                        .session(f.session()))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.nextDecision").value("CONTINUE"));
    }

    @Test
    @DisplayName("a child can ask for a new username; the parent approves it and the username changes")
    void usernameRequest() throws Exception {
        Family f = journeys.family(6);
        journeys.enterChildMode(f);
        String wanted = "brave-otter-" + (int) (Math.random() * 90 + 10);
        MvcResult ask = mvc.perform(json(post("/api/v1/learn/requests"),
                "{\"type\":\"USERNAME_CHANGE\",\"requestedValue\":\"" + wanted + "\"}").session(f.session())).andReturn();
        assertThat(ask.getResponse().getStatus()).isEqualTo(201);
        long id = ((Number) Journeys.read(ask, "$.id")).longValue();
        journeys.backToParent(f);
        mvc.perform(post("/api/v1/parent/requests/" + id + "/approve").with(realCsrf()).session(f.session()))
                .andExpect(status().isOk());
        assertThat(jdbc.sql("SELECT username FROM child WHERE id = :c").param("c", f.childId()).query(String.class)
                .single()).isEqualTo(wanted);
    }

    @Test
    @DisplayName("a parent can update their contact details and delete the whole account")
    void accountManagement() throws Exception {
        Family f = journeys.family(4);
        mvc.perform(json(patch("/api/v1/parent/account"), "{\"fullName\":\"Pat P.\",\"mobile\":\"+91 98765 43210\",\"city\":\"\"}")
                        .session(f.session()))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.fullName").value("Pat P."))
                .andExpect(jsonPath("$.city", org.hamcrest.Matchers.nullValue()));
        mvc.perform(delete("/api/v1/parent/account").with(realCsrf()).session(f.session()))
                .andExpect(status().isNoContent());
        assertThat(jdbc.sql("SELECT COUNT(*) FROM child WHERE id = :c").param("c", f.childId())
                .query(Integer.class).single()).as("the children go with the account").isZero();
    }
}
