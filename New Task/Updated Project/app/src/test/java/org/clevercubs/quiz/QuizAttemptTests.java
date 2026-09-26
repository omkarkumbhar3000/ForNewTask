package org.clevercubs.quiz;

import static org.assertj.core.api.Assertions.assertThat;
import static org.clevercubs.support.Journeys.json;
import static org.clevercubs.support.Journeys.realCsrf;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.post;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.put;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.jsonPath;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import java.util.ArrayList;
import java.util.List;
import java.util.concurrent.Callable;
import java.util.concurrent.CountDownLatch;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.concurrent.Future;

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

/**
 * Requirement section 11 and 13: scoring by the server, the three-attempt limit enforced by the backend, the
 * lock and the parent's grant (D63), resume (DD-19), the quiz's place in course completion, and the 80% reward
 * rule (D64).
 */
class QuizAttemptTests extends IntegrationTest {

    @Autowired
    MockMvc mvc;

    @Autowired
    JdbcClient jdbc;

    @Autowired
    PasswordEncoder passwords;

    @Autowired
    QuizService quizzes;

    Journeys journeys;

    @BeforeEach
    void setUp() {
        journeys = new Journeys(mvc, jdbc, passwords);
    }

    @AfterEach
    void cleanUp() {
        journeys.cleanUp();
    }

    private Family readyForQuiz(String slug) throws Exception {
        Family f = journeys.family(5);
        journeys.enterChildMode(f);
        journeys.finishLessons(f, slug);
        return f;
    }

    @Test
    @DisplayName("the quiz stays closed until every lesson is done (DD-16)")
    void quizNeedsTheLessons() throws Exception {
        Family f = journeys.family(5);
        journeys.enterChildMode(f);
        mvc.perform(post("/api/v1/learn/quizzes/" + journeys.quizId("animals") + "/attempts").with(realCsrf())
                        .session(f.session()))
                .andExpect(status().is(422))
                .andExpect(jsonPath("$.code").value("quiz-not-ready"));
    }

    @Test
    @DisplayName("the questions are sent without the correct answers")
    void correctAnswersAreNotSentUpFront() throws Exception {
        Family f = readyForQuiz("colours");
        MvcResult r = mvc.perform(post("/api/v1/learn/quizzes/" + journeys.quizId("colours") + "/attempts")
                .with(realCsrf()).session(f.session())).andReturn();
        String body = r.getResponse().getContentAsString();
        assertThat(body).doesNotContain("is_correct").doesNotContain("\"correct\":true");
        List<Object> revealed = Journeys.read(r, "$.questions[*].correctOptionId");
        assertThat(revealed).containsOnlyNulls();
    }

    @Test
    @DisplayName("a perfect quiz takes the course to 100% and earns the star badge (>= 80%)")
    void passingCompletesTheCourse() throws Exception {
        Family f = readyForQuiz("colours");
        long quiz = journeys.quizId("colours");
        String last = journeys.answerAll(f, journeys.startQuiz(f, quiz), quiz, 10);
        assertThat((Integer) com.jayway.jsonpath.JsonPath.read(last, "$.result.scorePercent")).isEqualTo(100);
        assertThat((Boolean) com.jayway.jsonpath.JsonPath.read(last, "$.result.passed")).isTrue();
        assertThat((Integer) com.jayway.jsonpath.JsonPath.read(last, "$.result.coursePercent")).isEqualTo(100);
        List<String> badges = com.jayway.jsonpath.JsonPath.read(last, "$.result.newBadges[*].code");
        assertThat(badges).contains("quiz-star-colours");
    }

    @Test
    @DisplayName("passing at 70% completes the course but earns no badge; 80% is the reward line (D62, D64)")
    void passMarkAndRewardLineAreSeparate() throws Exception {
        Family f = readyForQuiz("flowers");
        long quiz = journeys.quizId("flowers");
        String seventy = journeys.answerAll(f, journeys.startQuiz(f, quiz), quiz, 7);
        assertThat((Boolean) com.jayway.jsonpath.JsonPath.read(seventy, "$.result.passed")).isTrue();
        assertThat((Integer) com.jayway.jsonpath.JsonPath.read(seventy, "$.result.coursePercent")).isEqualTo(100);
        List<String> none = com.jayway.jsonpath.JsonPath.read(seventy, "$.result.newBadges[*].code");
        assertThat(none).doesNotContain("quiz-star-flowers");

        String eighty = journeys.answerAll(f, journeys.startQuiz(f, quiz), quiz, 8);
        List<String> badges = com.jayway.jsonpath.JsonPath.read(eighty, "$.result.newBadges[*].code");
        assertThat(badges).contains("quiz-star-flowers");
    }

    @Test
    @DisplayName("three failed attempts lock the quiz, the course stays below 100%, and a fourth start is refused")
    void threeAttemptsThenLocked() throws Exception {
        Family f = readyForQuiz("colours");
        long quiz = journeys.quizId("colours");
        for (int i = 0; i < 3; i++) {
            String last = journeys.answerAll(f, journeys.startQuiz(f, quiz), quiz, 2);
            assertThat((Boolean) com.jayway.jsonpath.JsonPath.read(last, "$.result.passed")).isFalse();
            assertThat((Integer) com.jayway.jsonpath.JsonPath.read(last, "$.result.attemptsRemaining")).isEqualTo(2 - i);
        }
        mvc.perform(post("/api/v1/learn/quizzes/" + quiz + "/attempts").with(realCsrf()).session(f.session()))
                .andExpect(status().is(422))
                .andExpect(jsonPath("$.code").value("quiz-locked"));
        MvcResult course = journeys.getJson(f.session(), "/api/v1/learn/courses/colours");
        assertThat(Journeys.<Integer>read(course, "$.course.percent")).isEqualTo(70);
        assertThat(Journeys.<Boolean>read(course, "$.course.quiz.locked")).isTrue();
        assertThat(jdbc.sql("SELECT COUNT(*) FROM quiz_attempt WHERE child_id = :c").param("c", f.childId())
                .query(Integer.class).single()).isEqualTo(3);
    }

    @Test
    @DisplayName("a locked child asks a grown-up; the parent approves and three more tries open, audited")
    void parentGrantsMoreAttempts() throws Exception {
        Family f = readyForQuiz("colours");
        long quiz = journeys.quizId("colours");
        for (int i = 0; i < 3; i++) {
            journeys.answerAll(f, journeys.startQuiz(f, quiz), quiz, 0);
        }
        MvcResult ask = mvc.perform(json(post("/api/v1/learn/requests"),
                "{\"type\":\"QUIZ_ATTEMPTS\",\"quizId\":" + quiz + "}").session(f.session())).andReturn();
        assertThat(ask.getResponse().getStatus()).isEqualTo(201);
        long requestId = ((Number) Journeys.read(ask, "$.id")).longValue();
        assertThat(ask.getResponse().getContentAsString()).doesNotContain(f.email());

        journeys.backToParent(f);
        mvc.perform(post("/api/v1/parent/requests/" + requestId + "/approve").with(realCsrf()).session(f.session()))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.status").value("APPROVED"));
        assertThat(jdbc.sql("SELECT attempts_allowed FROM quiz_allowance WHERE child_id = :c AND quiz_id = :q")
                .param("c", f.childId()).param("q", quiz).query(Integer.class).single()).isEqualTo(6);
        assertThat(jdbc.sql("SELECT COUNT(*) FROM audit_event WHERE action = 'QUIZ_ATTEMPTS_GRANTED' AND target_id = :c")
                .param("c", f.childId()).query(Integer.class).single()).isEqualTo(1);

        journeys.enterChildMode(f);
        String passed = journeys.answerAll(f, journeys.startQuiz(f, quiz), quiz, 10);
        assertThat((Integer) com.jayway.jsonpath.JsonPath.read(passed, "$.result.coursePercent")).isEqualTo(100);
    }

    @Test
    @DisplayName("opening the quiz page (its overview) never uses a try")
    void overviewUsesNoAttempt() throws Exception {
        Family f = readyForQuiz("colours");
        long quiz = journeys.quizId("colours");
        MvcResult r = journeys.getJson(f.session(), "/api/v1/learn/quizzes/" + quiz);
        assertThat(r.getResponse().getStatus()).isEqualTo(200);
        assertThat(Journeys.<Integer>read(r, "$.state.attemptsRemaining")).isEqualTo(3);
        assertThat(Journeys.<Integer>read(r, "$.questionCount")).isEqualTo(10);
        assertThat(jdbc.sql("SELECT COUNT(*) FROM quiz_attempt WHERE child_id = :c").param("c", f.childId())
                .query(Integer.class).single()).isZero();
    }

    @Test
    @DisplayName("reopening the quiz resumes the same attempt without using another (DD-19)")
    void resumeDoesNotUseAnAttempt() throws Exception {
        Family f = readyForQuiz("colours");
        long quiz = journeys.quizId("colours");
        long first = journeys.startQuiz(f, quiz);
        long again = journeys.startQuiz(f, quiz);
        assertThat(again).isEqualTo(first);
        assertThat(jdbc.sql("SELECT attempts_used FROM quiz_allowance WHERE child_id = :c AND quiz_id = :q")
                .param("c", f.childId()).param("q", quiz).query(Integer.class).single()).isEqualTo(1);
    }

    @Test
    @DisplayName("an answer is final: answering the same question again does not change the score")
    void answersAreFinal() throws Exception {
        Family f = readyForQuiz("colours");
        long quiz = journeys.quizId("colours");
        long attempt = journeys.startQuiz(f, quiz);
        long question = jdbc.sql("SELECT id FROM quiz_question WHERE quiz_id = :q AND pool = 'MAIN' ORDER BY sort_order LIMIT 1")
                .param("q", quiz).query(Long.class).single();
        mvc.perform(json(put("/api/v1/learn/attempts/" + attempt + "/answers/" + question),
                        "{\"optionId\":" + journeys.option(question, false) + "}").session(f.session()))
                .andExpect(jsonPath("$.correct").value(false));
        mvc.perform(json(put("/api/v1/learn/attempts/" + attempt + "/answers/" + question),
                        "{\"optionId\":" + journeys.option(question, true) + "}").session(f.session()))
                .andExpect(jsonPath("$.correct").value(false));
        assertThat(jdbc.sql("SELECT correct_count FROM quiz_attempt WHERE id = :a").param("a", attempt)
                .query(Integer.class).single()).isZero();
    }

    @Test
    @DisplayName("an option from another question is refused")
    void optionMustBelongToTheQuestion() throws Exception {
        Family f = readyForQuiz("colours");
        long quiz = journeys.quizId("colours");
        long attempt = journeys.startQuiz(f, quiz);
        List<Long> questions = jdbc.sql("SELECT id FROM quiz_question WHERE quiz_id = :q AND pool = 'MAIN' ORDER BY sort_order")
                .param("q", quiz).query(Long.class).list();
        mvc.perform(json(put("/api/v1/learn/attempts/" + attempt + "/answers/" + questions.get(0)),
                        "{\"optionId\":" + journeys.option(questions.get(1), true) + "}").session(f.session()))
                .andExpect(status().isBadRequest());
    }

    @Test
    @DisplayName("another child's attempt cannot be read or answered (IDOR)")
    void attemptsArePrivate() throws Exception {
        Family a = readyForQuiz("colours");
        long quiz = journeys.quizId("colours");
        long attempt = journeys.startQuiz(a, quiz);
        Family b = journeys.family(5);
        journeys.enterChildMode(b);
        mvc.perform(org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get(
                        "/api/v1/learn/attempts/" + attempt).session(b.session()))
                .andExpect(status().isNotFound());
    }

    @Test
    @DisplayName("two simultaneous starts open exactly one attempt and use one allowance")
    void simultaneousStartsOpenOneAttempt() throws Exception {
        Family f = readyForQuiz("colours");
        long quiz = journeys.quizId("colours");
        ExecutorService pool = Executors.newFixedThreadPool(4);
        CountDownLatch go = new CountDownLatch(1);
        List<Future<Long>> results = new ArrayList<>();
        for (int i = 0; i < 4; i++) {
            Callable<Long> start = () -> {
                go.await();
                return quizzes.start(f.childId(), quiz).attemptId();
            };
            results.add(pool.submit(start));
        }
        go.countDown();
        List<Long> ids = new ArrayList<>();
        for (Future<Long> r : results) {
            ids.add(r.get());
        }
        pool.shutdown();
        assertThat(ids).as("every caller resumed the same attempt").containsOnly(ids.getFirst());
        assertThat(jdbc.sql("SELECT attempts_used FROM quiz_allowance WHERE child_id = :c AND quiz_id = :q")
                .param("c", f.childId()).param("q", quiz).query(Integer.class).single()).isEqualTo(1);
    }
}
