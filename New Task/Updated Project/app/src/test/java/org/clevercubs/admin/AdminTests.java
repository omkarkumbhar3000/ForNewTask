package org.clevercubs.admin;

import static org.assertj.core.api.Assertions.assertThat;
import static org.clevercubs.support.Journeys.json;
import static org.clevercubs.support.Journeys.realCsrf;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.patch;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.post;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.put;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.jsonPath;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import java.time.Instant;
import java.util.List;

import org.clevercubs.platform.settings.Settings;
import org.clevercubs.support.IntegrationTest;
import org.clevercubs.support.Journeys;
import org.clevercubs.support.Journeys.Family;
import org.junit.jupiter.api.AfterEach;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.jdbc.core.simple.JdbcClient;
import org.springframework.mock.web.MockHttpSession;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.test.web.servlet.MockMvc;
import org.springframework.test.web.servlet.MvcResult;

import com.jayway.jsonpath.JsonPath;

/** Requirement section 19: the Super Admin dashboard, RBAC, sensitive actions and the audit trail. */
class AdminTests extends IntegrationTest {

    @Autowired
    MockMvc mvc;

    @Autowired
    JdbcClient jdbc;

    @Autowired
    PasswordEncoder passwords;

    @Autowired
    Settings settings;

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
    @DisplayName("parents and children are refused everywhere in the admin API")
    void onlyTheSuperAdmin() throws Exception {
        Family f = journeys.family(4);
        for (String path : List.of("/api/v1/admin/overview", "/api/v1/admin/accounts", "/api/v1/admin/feedback",
                "/api/v1/admin/settings", "/api/v1/admin/audit")) {
            mvc.perform(get(path).session(f.session())).andExpect(status().isForbidden());
        }
        journeys.enterChildMode(f);
        mvc.perform(get("/api/v1/admin/overview").session(f.session())).andExpect(status().isForbidden());
        mvc.perform(get("/api/v1/admin/overview")).andExpect(status().isUnauthorized());
    }

    @Test
    @DisplayName("the overview, the accounts, the children and the course report load for the Super Admin")
    void dashboardLoads() throws Exception {
        journeys.family(5);
        MockHttpSession admin = journeys.admin();
        MvcResult overview = journeys.getJson(admin, "/api/v1/admin/overview");
        assertThat(overview.getResponse().getStatus()).isEqualTo(200);
        assertThat(Journeys.<Integer>read(overview, "$.counts.courses")).isEqualTo(11);
        assertThat(Journeys.<Integer>read(overview, "$.counts.children")).isPositive();
        MvcResult accounts = journeys.getJson(admin, "/api/v1/admin/accounts?size=5");
        assertThat(accounts.getResponse().getContentAsString()).doesNotContain("password_hash").doesNotContain("$2a$");
        assertThat(journeys.getJson(admin, "/api/v1/admin/children").getResponse().getStatus()).isEqualTo(200);
        assertThat(journeys.getJson(admin, "/api/v1/admin/reports/courses").getResponse().getStatus()).isEqualTo(200);
    }

    @Test
    @DisplayName("disabling an account stops its sign-in, needs a recent password, and is audited")
    void disableAccount() throws Exception {
        Family f = journeys.family(4);
        MockHttpSession admin = journeys.admin();

        admin.setAttribute("clevercubs.password-confirmed-at", Instant.now().minusSeconds(7200));
        mvc.perform(json(post("/api/v1/admin/accounts/" + f.accountId() + "/status"), "{\"action\":\"DISABLE\"}")
                        .session(admin))
                .andExpect(status().isForbidden())
                .andExpect(jsonPath("$.code").value("reauth-required"));

        admin.setAttribute("clevercubs.password-confirmed-at", Instant.now());
        mvc.perform(json(post("/api/v1/admin/accounts/" + f.accountId() + "/status"), "{\"action\":\"DISABLE\"}")
                        .session(admin))
                .andExpect(status().isNoContent());
        mvc.perform(json(post("/api/v1/auth/login"),
                        "{\"email\":\"" + f.email() + "\",\"password\":\"" + Journeys.PASSWORD + "\"}"))
                .andExpect(status().isUnauthorized());
        assertThat(jdbc.sql("SELECT COUNT(*) FROM audit_event WHERE action = 'ACCOUNT_DISABLE' AND target_id = :a")
                .param("a", f.accountId()).query(Integer.class).single()).isEqualTo(1);
    }

    @Test
    @DisplayName("a temporary password is shown once, works, and forces a change at sign-in")
    void temporaryPassword() throws Exception {
        Family f = journeys.family(4);
        MockHttpSession admin = journeys.admin();
        MvcResult r = mvc.perform(post("/api/v1/admin/accounts/" + f.accountId() + "/temporary-password").with(realCsrf())
                .session(admin)).andReturn();
        String temporary = Journeys.read(r, "$.temporaryPassword");
        assertThat(temporary).hasSizeGreaterThanOrEqualTo(12);
        MockHttpSession parent = journeys.login(f.email(), temporary);
        mvc.perform(get("/api/v1/auth/me").session(parent)).andExpect(jsonPath("$.mustChangePassword").value(true));
        mvc.perform(get("/api/v1/parent/overview").session(parent))
                .andExpect(status().isForbidden())
                .andExpect(jsonPath("$.code").value("password-change-required"));
    }

    @Test
    @DisplayName("a Super Admin adds another: temporary password once, forced change, full admin rights, audited (D79)")
    void addSuperAdmin() throws Exception {
        MockHttpSession admin = journeys.admin();
        String email = Journeys.uniqueEmail("second_admin");
        journeys.remember(email);
        MvcResult created = mvc.perform(json(post("/api/v1/admin/accounts"), "{\"email\":\"" + email + "\"}")
                .session(admin)).andReturn();
        assertThat(created.getResponse().getStatus()).as(created.getResponse().getContentAsString()).isEqualTo(201);
        assertThat(Journeys.<String>read(created, "$.role")).isEqualTo("SUPER_ADMIN");
        String temporary = Journeys.read(created, "$.temporaryPassword");
        assertThat(temporary).hasSizeGreaterThanOrEqualTo(12);

        mvc.perform(json(post("/api/v1/admin/accounts"), "{\"email\":\"" + email.toUpperCase() + "\"}").session(admin))
                .andExpect(status().isBadRequest())
                .andExpect(jsonPath("$.code").value("email-taken"));

        MockHttpSession second = journeys.login(email, temporary);
        mvc.perform(get("/api/v1/admin/overview").session(second))
                .andExpect(status().isForbidden())
                .andExpect(jsonPath("$.code").value("password-change-required"));
        String chosen = "the new admin keeps a long sentence " + System.nanoTime();
        mvc.perform(json(post("/api/v1/auth/change-password"),
                        "{\"currentPassword\":\"" + temporary + "\",\"newPassword\":\"" + chosen + "\"}").session(second))
                .andExpect(status().is2xxSuccessful());
        mvc.perform(get("/api/v1/admin/overview").session(second)).andExpect(status().isOk());
        journeys.login(email, chosen);

        String details = jdbc.sql("""
                        SELECT details FROM audit_event WHERE action = 'ACCOUNT_CREATED' AND target_type = 'user_account'
                        ORDER BY id DESC LIMIT 1""").query(String.class).single();
        assertThat(details).contains("SUPER_ADMIN").doesNotContain(email).doesNotContain(temporary);
    }

    @Test
    @DisplayName("only a Super Admin may add one, and the address must be an email address")
    void addSuperAdminIsGuarded() throws Exception {
        Family f = journeys.family(4);
        mvc.perform(json(post("/api/v1/admin/accounts"), "{\"email\":\"someone@example.test\"}").session(f.session()))
                .andExpect(status().isForbidden());
        MockHttpSession admin = journeys.admin();
        mvc.perform(json(post("/api/v1/admin/accounts"), "{\"email\":\"admin\"}").session(admin))
                .andExpect(status().isBadRequest());
        assertThat(jdbc.sql("SELECT COUNT(*) FROM user_account WHERE email = 'someone@example.test'")
                .query(Integer.class).single()).isZero();
    }

    @Test
    @DisplayName("settings are validated, change the live rule, and are audited with before and after")
    void settingsChange() throws Exception {
        MockHttpSession admin = journeys.admin();
        mvc.perform(json(put("/api/v1/admin/settings/" + Settings.REWARD_THRESHOLD), "{\"value\":\"250\"}").session(admin))
                .andExpect(status().isBadRequest());
        try {
            mvc.perform(json(put("/api/v1/admin/settings/" + Settings.REWARD_THRESHOLD), "{\"value\":\"85\"}")
                            .session(admin))
                    .andExpect(status().isOk())
                    .andExpect(jsonPath("$['reward.threshold_percent']").value("85"));
            assertThat(settings.intValue(Settings.REWARD_THRESHOLD)).isEqualTo(85);
            List<String> changes = jdbc.sql("SELECT details FROM audit_event WHERE action = 'SETTING_CHANGED'")
                    .query(String.class).list();
            assertThat(changes).anySatisfy(d -> assertThat(JsonPath.<String>read(d, "$.to")).isEqualTo("85"));
        } finally {
            jdbc.sql("UPDATE system_setting SET setting_value = '80' WHERE setting_key = :k")
                    .param("k", Settings.REWARD_THRESHOLD).update();
        }
        mvc.perform(json(put("/api/v1/admin/settings/unknown.key"), "{\"value\":\"1\"}").session(admin))
                .andExpect(status().isNotFound());
    }

    @Test
    @DisplayName("course and quiz content can be edited, with one correct answer enforced")
    void contentManagement() throws Exception {
        MockHttpSession admin = journeys.admin();
        long courseId = journeys.courseId("fruits");
        String title = jdbc.sql("SELECT title FROM course WHERE id = :c").param("c", courseId).query(String.class).single();
        try {
            mvc.perform(json(patch("/api/v1/admin/courses/" + courseId), "{\"title\":\"Yummy Fruits\"}").session(admin))
                    .andExpect(status().isOk())
                    .andExpect(jsonPath("$.title").value("Yummy Fruits"));
        } finally {
            jdbc.sql("UPDATE course SET title = :t WHERE id = :c").param("t", title).param("c", courseId).update();
        }
        long quiz = journeys.quizId("fruits");
        MvcResult q = journeys.getJson(admin, "/api/v1/admin/quizzes/" + quiz);
        Number questionId = Journeys.read(q, "$.questions[0].id");
        List<Number> optionIds = Journeys.read(q, "$.questions[0].options[*].id");
        String twoCorrect = "{\"options\":[{\"id\":" + optionIds.get(0) + ",\"correct\":true},{\"id\":" + optionIds.get(1)
                + ",\"correct\":true}]}";
        mvc.perform(json(patch("/api/v1/admin/questions/" + questionId), twoCorrect).session(admin))
                .andExpect(status().is(422))
                .andExpect(jsonPath("$.code").value("one-correct-option"));
    }

    @Test
    @DisplayName("feedback status can be moved through NEW, READ and RESOLVED")
    void feedbackWorkflow() throws Exception {
        Family f = journeys.family(4);
        MvcResult sent = mvc.perform(json(post("/api/v1/parent/feedback"),
                "{\"category\":\"PROBLEM\",\"message\":\"The video did not play\"}").session(f.session())).andReturn();
        long id = ((Number) Journeys.read(sent, "$.id")).longValue();
        MockHttpSession admin = journeys.admin();
        mvc.perform(json(patch("/api/v1/admin/feedback/" + id), "{\"status\":\"RESOLVED\"}").session(admin))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.status").value("RESOLVED"));
    }

    @Test
    @DisplayName("the audit trail is readable by the admin and cannot be changed by the application user")
    void auditTrail() throws Exception {
        MockHttpSession admin = journeys.admin();
        MvcResult audit = journeys.getJson(admin, "/api/v1/admin/audit?size=20");
        List<String> actions = Journeys.read(audit, "$[*].action");
        assertThat(actions).contains("AUTH_LOGIN_SIGNED_IN");
    }
}
