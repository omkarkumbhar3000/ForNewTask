package org.clevercubs.learning;

import static org.assertj.core.api.Assertions.assertThat;
import static org.clevercubs.support.Journeys.json;
import static org.clevercubs.support.Journeys.realCsrf;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.post;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.put;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.jsonPath;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

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
import org.springframework.mock.web.MockHttpSession;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.test.web.servlet.MockMvc;
import org.springframework.test.web.servlet.MvcResult;

/**
 * Child mode (D58) and the learning flow (requirement sections 9 and 10): course cards, lessons, progress
 * calculated by the server, resume, and completion of a course without a quiz.
 */
class LearningFlowTests extends IntegrationTest {

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

    // --- child mode -------------------------------------------------------------------------------------

    @Test
    @DisplayName("a parent enters child mode for their own child; the session then holds only the child role")
    void childModeForOwnChild() throws Exception {
        Family f = journeys.family(4);
        journeys.enterChildMode(f);
        mvc.perform(get("/api/v1/auth/me").session(f.session()))
                .andExpect(jsonPath("$.mode").value("CHILD"))
                .andExpect(jsonPath("$.activeChildId").value(f.childId()));
        mvc.perform(get("/api/v1/parent/overview").session(f.session())).andExpect(status().isForbidden());
        mvc.perform(get("/api/v1/learn/home").session(f.session())).andExpect(status().isOk());
    }

    @Test
    @DisplayName("a parent cannot enter child mode for another family's child (IDOR, SEC-E04)")
    void noChildModeForSomeoneElsesChild() throws Exception {
        Family a = journeys.family(4);
        Family b = journeys.family(5);
        mvc.perform(json(post("/api/v1/session/child"), "{\"childId\":" + b.childId() + "}").session(a.session()))
                .andExpect(status().isNotFound());
    }

    @Test
    @DisplayName("leaving child mode needs the parent's password; a wrong one keeps the child session")
    void returningToParentNeedsThePassword() throws Exception {
        Family f = journeys.family(4);
        journeys.enterChildMode(f);
        mvc.perform(json(post("/api/v1/session/parent"), "{\"password\":\"not-the-password-1\"}").session(f.session()))
                .andExpect(status().isUnauthorized())
                .andExpect(jsonPath("$.code").value("invalid-credentials"));
        mvc.perform(get("/api/v1/auth/me").session(f.session())).andExpect(jsonPath("$.mode").value("CHILD"));
        journeys.backToParent(f);
        mvc.perform(get("/api/v1/auth/me").session(f.session())).andExpect(jsonPath("$.mode").value("PARENT"));
    }

    @Test
    @DisplayName("a parent session cannot use the child API")
    void parentModeCannotLearn() throws Exception {
        Family f = journeys.family(4);
        mvc.perform(get("/api/v1/learn/home").session(f.session())).andExpect(status().isForbidden());
    }

    // --- learning and progress ------------------------------------------------------------------------------

    @Test
    @DisplayName("home lists the program's courses at 0% with a resume target and a greeting")
    void homeStartsAtZero() throws Exception {
        Family f = journeys.family(3);
        journeys.enterChildMode(f);
        MvcResult home = journeys.getJson(f.session(), "/api/v1/learn/home");
        assertThat(home.getResponse().getStatus()).isEqualTo(200);
        List<Integer> percents = Journeys.read(home, "$.courses[*].percent");
        assertThat(percents).hasSize(11).containsOnly(0);
        assertThat(Journeys.<String>read(home, "$.greeting")).contains("Zoe");
        assertThat(Journeys.<String>read(home, "$.resume.courseSlug")).isNotBlank();
        assertThat(Journeys.<String>read(home, "$.child.uiProfile")).isEqualTo("TODDLER");
    }

    @Test
    @DisplayName("opening every card of a lesson completes it and progress follows the 70/30 rule (D61)")
    void lessonCompletionMovesProgress() throws Exception {
        Family f = journeys.family(5);
        journeys.enterChildMode(f);
        List<Long> lessons = journeys.lessonIds("animals");
        journeys.finishLesson(f, lessons.getFirst());

        MvcResult course = journeys.getJson(f.session(), "/api/v1/learn/courses/animals");
        assertThat(Journeys.<Integer>read(course, "$.course.lessonsDone")).isEqualTo(1);
        assertThat(Journeys.<Integer>read(course, "$.course.percent")).isEqualTo(70 * 1 / lessons.size());
        assertThat(Journeys.<Boolean>read(course, "$.course.quiz.unlocked")).isFalse();
        assertThat(Journeys.<Integer>read(course, "$.nextLessonId")).isEqualTo(lessons.get(1).intValue());
    }

    @Test
    @DisplayName("every lesson done is 70%: never 100% before the quiz is passed (section 10)")
    void lessonsAloneStopAtSeventy() throws Exception {
        Family f = journeys.family(5);
        journeys.enterChildMode(f);
        journeys.finishLessons(f, "colours");
        MvcResult course = journeys.getJson(f.session(), "/api/v1/learn/courses/colours");
        assertThat(Journeys.<Integer>read(course, "$.course.percent")).isEqualTo(70);
        assertThat(Journeys.<Boolean>read(course, "$.course.completed")).isFalse();
        assertThat(Journeys.<Boolean>read(course, "$.course.quiz.unlocked")).isTrue();
    }

    @Test
    @DisplayName("viewing a card twice changes nothing, and resume points to the next unfinished lesson")
    void viewsAreIdempotentAndResumeFollows() throws Exception {
        Family f = journeys.family(6);
        journeys.enterChildMode(f);
        List<Long> lessons = journeys.lessonIds("birds");
        journeys.finishLesson(f, lessons.getFirst());
        journeys.finishLesson(f, lessons.getFirst());
        assertThat(jdbc.sql("SELECT COUNT(*) FROM lesson_completion WHERE child_id = :c").param("c", f.childId())
                .query(Integer.class).single()).isEqualTo(1);
        MvcResult home = journeys.getJson(f.session(), "/api/v1/learn/home");
        assertThat(Journeys.<String>read(home, "$.resume.courseSlug")).isEqualTo("birds");
        assertThat(Journeys.<Integer>read(home, "$.resume.lessonId")).isEqualTo(lessons.get(1).intValue());
    }

    @Test
    @DisplayName("a course without a quiz reaches 100% through its lessons and earns its completion badge")
    void mediaCourseCompletes() throws Exception {
        Family f = journeys.family(4);
        journeys.enterChildMode(f);
        journeys.finishLessons(f, "stories");
        MvcResult course = journeys.getJson(f.session(), "/api/v1/learn/courses/stories");
        assertThat(Journeys.<Integer>read(course, "$.course.percent")).isEqualTo(100);
        List<Boolean> comingSoon = Journeys.read(course, "$.lessons[*].comingSoon");
        assertThat(comingSoon).as("the story with no video is marked, not counted (INF-09)").contains(true);
        assertThat(jdbc.sql("""
                        SELECT COUNT(*) FROM child_badge cb JOIN badge b ON b.id = cb.badge_id
                        WHERE cb.child_id = :c AND b.code = 'done-stories'""")
                .param("c", f.childId()).query(Integer.class).single()).isEqualTo(1);
    }

    @Test
    @DisplayName("a card that is coming soon cannot be marked as viewed")
    void missingMediaCannotBeViewed() throws Exception {
        Family f = journeys.family(4);
        journeys.enterChildMode(f);
        long missing = jdbc.sql("SELECT id FROM lesson_item WHERE status = 'MEDIA_MISSING' LIMIT 1")
                .query(Long.class).single();
        mvc.perform(put("/api/v1/learn/items/" + missing + "/view").with(realCsrf()).session(f.session()))
                .andExpect(status().is(422))
                .andExpect(jsonPath("$.code").value("media-missing"));
    }

    @Test
    @DisplayName("a lesson shows its cards with media paths under /media and a friendly start message")
    void lessonView() throws Exception {
        Family f = journeys.family(4);
        journeys.enterChildMode(f);
        MvcResult lesson = journeys.getJson(f.session(), "/api/v1/learn/lessons/" + journeys.lessonIds("alphabets").getFirst());
        assertThat(Journeys.<String>read(lesson, "$.items[0].label")).isEqualTo("A");
        assertThat(Journeys.<String>read(lesson, "$.items[0].image")).startsWith("/media/alphabets/");
        assertThat(Journeys.<String>read(lesson, "$.startMessage")).isNotBlank();
    }

    @Test
    @DisplayName("an unknown course is a 404, not a 500")
    void unknownCourse() throws Exception {
        Family f = journeys.family(4);
        journeys.enterChildMode(f);
        mvc.perform(get("/api/v1/learn/courses/does-not-exist").session(f.session()))
                .andExpect(status().isNotFound());
    }

    @Test
    @DisplayName("the profile shows badges as goals and achievements, never other children")
    void profileShowsBadges() throws Exception {
        Family f = journeys.family(7);
        journeys.enterChildMode(f);
        MvcResult profile = journeys.getJson(f.session(), "/api/v1/learn/profile");
        List<Boolean> earned = Journeys.read(profile, "$.badges[*].earned");
        assertThat(earned).isNotEmpty().containsOnly(false);
        assertThat(Journeys.<String>read(profile, "$.child.uiProfile")).isEqualTo("EARLY_PRIMARY");
    }

    @Test
    @DisplayName("without a session the child API is 401 and a learning page redirects to login")
    void strangersAreRefused() throws Exception {
        mvc.perform(get("/api/v1/learn/home")).andExpect(status().isUnauthorized());
        mvc.perform(get("/learn/").session(new MockHttpSession())).andExpect(status().is3xxRedirection());
    }
}
