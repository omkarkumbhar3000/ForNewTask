package org.clevercubs.account;

import static org.assertj.core.api.Assertions.assertThat;
import static org.clevercubs.support.Journeys.PASSWORD;
import static org.clevercubs.support.Journeys.json;
import static org.clevercubs.support.Journeys.registration;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.post;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.jsonPath;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import java.time.LocalDate;
import java.time.ZoneOffset;
import java.util.Map;

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

/** Requirement section 6 and 7: registration of a parent with the first child, consent, and validation. */
class RegistrationTests extends IntegrationTest {

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

    private static LocalDate age(int years) {
        return LocalDate.now(ZoneOffset.UTC).minusYears(years).minusDays(30);
    }

    private MvcResult register(String body) throws Exception {
        return mvc.perform(json(post("/api/v1/auth/register"), body).session(new MockHttpSession())).andReturn();
    }

    @Test
    @DisplayName("registration creates the account, parent, child, three consents and the Year-1 enrolment, and signs in")
    void registrationCreatesTheFamily() throws Exception {
        Family f = journeys.family(4);

        mvc.perform(get("/api/v1/auth/me").session(f.session()))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.role").value("PARENT"))
                .andExpect(jsonPath("$.mode").value("PARENT"));

        Map<String, Object> child = jdbc.sql("SELECT * FROM child WHERE id = :id").param("id", f.childId())
                .query().singleRow();
        assertThat(child.get("first_name")).isEqualTo("Zoe");
        assertThat(child.get("display_name")).as("defaults to the first name").isEqualTo("Zoe");
        assertThat((String) child.get("username")).as("a friendly suggestion").matches("[a-z]+-[a-z]+-\\d{2}");
        assertThat(jdbc.sql("SELECT COUNT(*) FROM consent_record c JOIN parent p ON p.id = c.parent_id WHERE p.account_id = :a")
                .param("a", f.accountId()).query(Integer.class).single()).isEqualTo(3);
        assertThat(jdbc.sql("""
                        SELECT g.code FROM program_enrolment e JOIN program p ON p.id = e.program_id
                        JOIN age_group g ON g.id = p.age_group_id WHERE e.child_id = :c""")
                .param("c", f.childId()).query(String.class).single())
                .as("a four-year-old is enrolled in the 4-5 band's Year 1").isEqualTo("LITTLE");
        String hash = jdbc.sql("SELECT password_hash FROM user_account WHERE id = :a").param("a", f.accountId())
                .query(String.class).single();
        assertThat(hash).startsWith("$2").isNotEqualTo(PASSWORD);
    }

    @Test
    @DisplayName("the answer never contains the password or its hash")
    void noSecretInTheAnswer() throws Exception {
        String email = Journeys.uniqueEmail("parent");
        journeys.remember(email);
        MvcResult r = register(registration(email, PASSWORD, "Ann", age(3), null));
        assertThat(r.getResponse().getStatus()).isEqualTo(201);
        assertThat(r.getResponse().getContentAsString()).doesNotContain(PASSWORD).doesNotContain("$2a$");
    }

    @Test
    @DisplayName("an email that is already registered is refused")
    void duplicateEmailIsRefused() throws Exception {
        Family f = journeys.family(5);
        MvcResult r = register(registration(f.email(), PASSWORD, "Ben", age(5), null));
        assertThat(r.getResponse().getStatus()).isEqualTo(400);
        assertThat(Journeys.<String>read(r, "$.code")).isEqualTo("email-taken");
    }

    @Test
    @DisplayName("a short or common password is refused (DD-01)")
    void weakPasswordsAreRefused() throws Exception {
        String email = Journeys.uniqueEmail("parent");
        journeys.remember(email);
        MvcResult shortOne = register(registration(email, "short", "Cat", age(5), null));
        assertThat(shortOne.getResponse().getStatus()).isEqualTo(400);
        assertThat(Journeys.<String>read(shortOne, "$.code")).isEqualTo("weak-password");

        MvcResult common = register(registration(email, "123456789012", "Cat", age(5), null));
        assertThat(Journeys.<String>read(common, "$.code")).isEqualTo("weak-password");
        assertThat(jdbc.sql("SELECT COUNT(*) FROM user_account WHERE email = :e").param("e", email)
                .query(Integer.class).single()).as("nothing was created").isZero();
    }

    @Test
    @DisplayName("a child outside the supported ages is refused with a clear message")
    void ageOutsideTheBandsIsRefused() throws Exception {
        String email = Journeys.uniqueEmail("parent");
        journeys.remember(email);
        MvcResult tooOld = register(registration(email, PASSWORD, "Dan", age(11), null));
        assertThat(tooOld.getResponse().getStatus()).isEqualTo(400);
        assertThat(Journeys.<String>read(tooOld, "$.code")).isEqualTo("age-not-supported");
        assertThat(Journeys.<String>read(tooOld, "$.detail")).contains("2 to 8");

        MvcResult future = register(registration(email, PASSWORD, "Dan", LocalDate.now().plusDays(3), null));
        assertThat(future.getResponse().getStatus()).isEqualTo(400);
    }

    @Test
    @DisplayName("all three consents are required")
    void consentIsRequired() throws Exception {
        String email = Journeys.uniqueEmail("parent");
        journeys.remember(email);
        String body = registration(email, PASSWORD, "Eve", age(4), null).replace("\"consentChildData\":true",
                "\"consentChildData\":false");
        MvcResult r = register(body);
        assertThat(r.getResponse().getStatus()).isEqualTo(400);
        assertThat(Journeys.<String>read(r, "$.code")).isEqualTo("consent-required");
    }

    @Test
    @DisplayName("usernames follow the safety rules: no real name, no phone-like numbers, no blocked words")
    void usernameRules() throws Exception {
        String email = Journeys.uniqueEmail("parent");
        journeys.remember(email);
        assertThat(Journeys.<String>read(register(registration(email, PASSWORD, "Maya", age(6), "maya-star")), "$.code"))
                .isEqualTo("invalid-username");
        assertThat(Journeys.<String>read(register(registration(email, PASSWORD, "Maya", age(6), "cub9876543")), "$.code"))
                .isEqualTo("invalid-username");
        assertThat(Journeys.<String>read(register(registration(email, PASSWORD, "Maya", age(6), "x")), "$.code"))
                .isEqualTo("invalid-username");
    }

    @Test
    @DisplayName("a username that is taken is refused")
    void takenUsernameIsRefused() throws Exception {
        Family f = journeys.family(5);
        String taken = jdbc.sql("SELECT username FROM child WHERE id = :c").param("c", f.childId())
                .query(String.class).single();
        String email = Journeys.uniqueEmail("parent");
        journeys.remember(email);
        assertThat(Journeys.<String>read(register(registration(email, PASSWORD, "Ola", age(5), taken)), "$.code"))
                .isEqualTo("username-taken");
    }

    @Test
    @DisplayName("a suggested username never contains the child's own name (found by the browser tests)")
    void suggestionsRespectTheChildsName() throws Exception {
        Family f = journeys.family(5);
        for (int i = 0; i < 8; i++) {
            MvcResult r = mvc.perform(json(post("/api/v1/parent/children"),
                    "{\"firstName\":\"Seal\",\"dateOfBirth\":\"" + age(4) + "\"}").session(f.session())).andReturn();
            assertThat(r.getResponse().getStatus()).as(r.getResponse().getContentAsString()).isEqualTo(201);
            assertThat(Journeys.<String>read(r, "$.username")).doesNotContainIgnoringCase("seal");
        }
    }

    @Test
    @DisplayName("SQL and script payloads are stored as plain text, never executed (SEC-E01, SEC-E18)")
    void injectionPayloadsAreJustText() throws Exception {
        String email = Journeys.uniqueEmail("parent");
        journeys.remember(email);
        String body = registration(email, PASSWORD, "Robert'); DROP TABLE child;--", age(5), null)
                .replace("Pat Parent", "<script>alert(1)</script>");
        assertThat(register(body).getResponse().getStatus()).isEqualTo(201);
        assertThat(jdbc.sql("SELECT COUNT(*) FROM child").query(Integer.class).single()).isPositive();
        assertThat(jdbc.sql("SELECT p.full_name FROM parent p JOIN user_account a ON a.id = p.account_id WHERE a.email = :e")
                .param("e", email).query(String.class).single()).isEqualTo("<script>alert(1)</script>");
    }

    @Test
    @DisplayName("a missing body part is a field-level invalid-input answer")
    void incompleteRegistrationIsInvalid() throws Exception {
        mvc.perform(json(post("/api/v1/auth/register"), "{\"parent\":{\"email\":\"x\"}}"))
                .andExpect(status().isBadRequest())
                .andExpect(jsonPath("$.code").value("invalid-input"))
                .andExpect(jsonPath("$.fields").isArray());
    }
}
