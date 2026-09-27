package org.clevercubs.support;

import static org.assertj.core.api.Assertions.assertThat;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.post;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.put;

import java.time.LocalDate;
import java.time.ZoneOffset;
import java.util.ArrayList;
import java.util.List;
import java.util.Map;
import java.util.UUID;

import org.clevercubs.platform.db.Rows;
import org.clevercubs.platform.db.Timestamps;
import org.springframework.http.MediaType;
import org.springframework.jdbc.core.simple.JdbcClient;
import org.springframework.mock.web.MockHttpSession;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.test.web.servlet.MockMvc;
import org.springframework.test.web.servlet.MvcResult;
import org.springframework.test.web.servlet.request.MockHttpServletRequestBuilder;
import org.springframework.test.web.servlet.request.RequestPostProcessor;

import jakarta.servlet.http.Cookie;

import com.jayway.jsonpath.JsonPath;

/**
 * The journeys the integration tests repeat, driven through the real HTTP API exactly as the pages drive it:
 * register a family, sign in, enter child mode, finish lessons, answer a quiz. Every account it creates is
 * remembered by email and removed by {@link #cleanUp()} (deleting by email, per the AGENTS.md lesson that
 * ids read before an insert are not reliable).
 */
public final class Journeys {

    public static final String PASSWORD = "Sunny-garden-path-42";

    public record Family(String email, long accountId, long childId, MockHttpSession session) {
    }

    private final MockMvc mvc;
    private final JdbcClient jdbc;
    private final PasswordEncoder passwords;
    private final List<String> emails = new ArrayList<>();

    public Journeys(MockMvc mvc, JdbcClient jdbc, PasswordEncoder passwords) {
        this.mvc = mvc;
        this.jdbc = jdbc;
        this.passwords = passwords;
    }

    public static String uniqueEmail(String prefix) {
        return prefix + "-" + UUID.randomUUID() + "@example.test";
    }

    public static String registration(String email, String password, String childName, LocalDate dob,
            String username) {
        return """
                {"parent":{"fullName":"Pat Parent","email":"%s","password":"%s","mobile":"","city":"Pune"},
                 "child":{"firstName":"%s","displayName":"","dateOfBirth":"%s","username":%s,"avatarCode":"owl"},
                 "acceptTerms":true,"acceptPrivacy":true,"consentChildData":true}"""
                .formatted(email, password, childName, dob, username == null ? "null" : "\"" + username + "\"");
    }

    /** Registers a parent with one child aged about {@code years}, signed in, in parent mode. */
    public Family family(int years) throws Exception {
        String email = uniqueEmail("parent");
        emails.add(email);
        LocalDate dob = LocalDate.now(ZoneOffset.UTC).minusYears(years).minusDays(40);
        MockHttpSession session = new MockHttpSession();
        MvcResult result = mvc.perform(json(post("/api/v1/auth/register"), registration(email, PASSWORD, "Zoe", dob,
                        null)).session(session))
                .andReturn();
        assertThat(result.getResponse().getStatus()).as(result.getResponse().getContentAsString()).isEqualTo(201);
        long accountId = ((Number) JsonPath.read(result.getResponse().getContentAsString(), "$.accountId")).longValue();
        long childId = jdbc.sql("""
                        SELECT c.id FROM child c JOIN parent p ON p.id = c.parent_id WHERE p.account_id = :a""")
                .param("a", accountId).query(Long.class).single();
        return new Family(email, accountId, childId, (MockHttpSession) result.getRequest().getSession(false));
    }

    /** Creates a Super Admin directly in the database (no public route creates one) and signs it in. */
    public MockHttpSession admin() throws Exception {
        String email = uniqueEmail("super_admin");
        emails.add(email);
        jdbc.sql("""
                        INSERT INTO user_account (email, password_hash, role, status, failed_logins, must_change_password,
                                                  password_changed_at, created_at, updated_at)
                        VALUES (:e, :h, 'SUPER_ADMIN', 'ACTIVE', 0, FALSE, :now, :now, :now)""")
                .param("now", Timestamps.now())
                .param("e", email).param("h", passwords.encode(PASSWORD)).update();
        return login(email, PASSWORD);
    }

    public MockHttpSession login(String email, String password) throws Exception {
        MockHttpSession session = new MockHttpSession();
        MvcResult result = mvc.perform(json(post("/api/v1/auth/login"),
                        "{\"email\":\"" + email + "\",\"password\":\"" + password + "\"}").session(session))
                .andReturn();
        assertThat(result.getResponse().getStatus()).as(result.getResponse().getContentAsString()).isEqualTo(200);
        return (MockHttpSession) result.getRequest().getSession(false);
    }

    public void enterChildMode(Family f) throws Exception {
        MvcResult r = mvc.perform(json(post("/api/v1/session/child"), "{\"childId\":" + f.childId() + "}")
                .session(f.session())).andReturn();
        assertThat(r.getResponse().getStatus()).as(r.getResponse().getContentAsString()).isEqualTo(200);
    }

    public void backToParent(Family f) throws Exception {
        MvcResult r = mvc.perform(json(post("/api/v1/session/parent"), "{\"password\":\"" + PASSWORD + "\"}")
                .session(f.session())).andReturn();
        assertThat(r.getResponse().getStatus()).as(r.getResponse().getContentAsString()).isEqualTo(200);
    }

    public long courseId(String slug) {
        return jdbc.sql("SELECT id FROM course WHERE slug = :s").param("s", slug).query(Long.class).single();
    }

    public long quizId(String slug) {
        return jdbc.sql("SELECT q.id FROM quiz q JOIN course c ON c.id = q.course_id WHERE c.slug = :s")
                .param("s", slug).query(Long.class).single();
    }

    /** Opens every ready card of every lesson of the course, through the API, in child mode. */
    public void finishLessons(Family f, String slug) throws Exception {
        for (Long lessonId : lessonIds(slug)) {
            finishLesson(f, lessonId);
        }
    }

    public void finishLesson(Family f, long lessonId) throws Exception {
        List<Long> items = jdbc.sql("SELECT id FROM lesson_item WHERE lesson_id = :l AND status = 'READY'")
                .param("l", lessonId).query(Long.class).list();
        for (Long item : items) {
            MvcResult r = mvc.perform(put("/api/v1/learn/items/" + item + "/view").with(realCsrf()).session(f.session()))
                    .andReturn();
            assertThat(r.getResponse().getStatus()).as(r.getResponse().getContentAsString()).isEqualTo(200);
        }
    }

    public List<Long> lessonIds(String slug) {
        return jdbc.sql("""
                        SELECT l.id FROM lesson l JOIN course c ON c.id = l.course_id
                        WHERE c.slug = :s AND l.status = 'PUBLISHED' ORDER BY l.sort_order""")
                .param("s", slug).query(Long.class).list();
    }

    /** Starts (or resumes) the quiz and returns the attempt id. */
    public long startQuiz(Family f, long quizId) throws Exception {
        MvcResult r = mvc.perform(post("/api/v1/learn/quizzes/" + quizId + "/attempts").with(realCsrf())
                .session(f.session())).andReturn();
        assertThat(r.getResponse().getStatus()).as(r.getResponse().getContentAsString()).isEqualTo(200);
        return ((Number) JsonPath.read(r.getResponse().getContentAsString(), "$.attemptId")).longValue();
    }

    /**
     * Answers every question of the attempt: the first {@code correct} questions right, the rest wrong.
     * Returns the body of the last answer, which carries the result.
     */
    public String answerAll(Family f, long attemptId, long quizId, int correct) throws Exception {
        List<Long> questions = jdbc.sql("SELECT id FROM quiz_question WHERE quiz_id = :q AND pool = 'MAIN' ORDER BY sort_order")
                .param("q", quizId).query(Long.class).list();
        String last = null;
        for (int i = 0; i < questions.size(); i++) {
            long option = option(questions.get(i), i < correct);
            MvcResult r = mvc.perform(json(put("/api/v1/learn/attempts/" + attemptId + "/answers/" + questions.get(i)),
                    "{\"optionId\":" + option + "}").session(f.session())).andReturn();
            assertThat(r.getResponse().getStatus()).as(r.getResponse().getContentAsString()).isEqualTo(200);
            last = r.getResponse().getContentAsString();
        }
        return last;
    }

    public long option(long questionId, boolean correct) {
        return jdbc.sql("SELECT id FROM quiz_option WHERE question_id = :q AND is_correct = :c ORDER BY sort_order LIMIT 1")
                .param("q", questionId).param("c", correct).query(Long.class).single();
    }

    /** A POST/PUT/PATCH with a JSON body and a valid CSRF token. */
    public static MockHttpServletRequestBuilder json(MockHttpServletRequestBuilder request, String body) {
        return request.with(realCsrf()).contentType(MediaType.APPLICATION_JSON).content(body);
    }

    /**
     * The real double-submit exchange the pages use: the same random value in the XSRF-TOKEN cookie and the
     * X-XSRF-TOKEN header. Deliberately not spring-security-test's csrf(), which swaps the shared CsrfFilter's
     * token repository for a session-based one and so changes CSRF for every later test in the context.
     */
    public static RequestPostProcessor realCsrf() {
        return request -> {
            String token = UUID.randomUUID().toString();
            Cookie[] existing = request.getCookies();
            Cookie[] cookies = existing == null ? new Cookie[1] : java.util.Arrays.copyOf(existing, existing.length + 1);
            cookies[cookies.length - 1] = new Cookie("XSRF-TOKEN", token);
            request.setCookies(cookies);
            request.addHeader("X-XSRF-TOKEN", token);
            return request;
        };
    }

    public MvcResult getJson(MockHttpSession session, String path) throws Exception {
        return mvc.perform(get(path).session(session)).andReturn();
    }

    public static <T> T read(MvcResult result, String path) throws Exception {
        return JsonPath.read(result.getResponse().getContentAsString(), path);
    }

    public Map<String, Object> row(String sql, Map<String, ?> params) {
        return jdbc.sql(sql).params(params).query(Rows.MAP).single();
    }

    /** Removes every account this helper created; children and their data follow by cascade. */
    public void cleanUp() {
        for (String email : emails) {
            jdbc.sql("DELETE FROM user_account WHERE email = :e").param("e", email).update();
        }
        emails.clear();
    }

    public void remember(String email) {
        emails.add(email);
    }
}
