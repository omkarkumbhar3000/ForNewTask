package org.clevercubs.learning;

import static org.assertj.core.api.Assertions.assertThat;
import static org.clevercubs.support.Journeys.realCsrf;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.post;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.put;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import java.util.HashSet;
import java.util.List;
import java.util.Map;
import java.util.Set;

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
 * Each club has its own course set, and a child reaches only the courses of their own program (D78,
 * programs/year-1.json). Tiny Cubs 2-3, Little Cubs 4-5, Big Cubs 6-8.
 */
class ClubProgramsTests extends IntegrationTest {

    static final List<String> TINY = List.of("colours", "animals", "fruits", "rhymes");
    static final List<String> LITTLE = List.of("alphabets", "numbers", "body-parts", "vegetables");
    static final List<String> BIG = List.of("birds", "flowers", "stories");

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

    List<String> programSlugs(String club) {
        return jdbc.sql("""
                        SELECT c.slug FROM program_course pc
                        JOIN program p ON p.id = pc.program_id JOIN age_group g ON g.id = p.age_group_id
                        JOIN course c ON c.id = pc.course_id
                        WHERE g.code = :club AND p.year_number = 1 ORDER BY pc.sort_order""")
                .param("club", club).query(String.class).list();
    }

    @Test
    @DisplayName("each club's Year 1 holds its own courses: distinct sets that together cover every course")
    void eachClubHasItsOwnCourses() {
        assertThat(programSlugs("TINY")).containsExactlyElementsOf(TINY);
        assertThat(programSlugs("LITTLE")).containsExactlyElementsOf(LITTLE);
        assertThat(programSlugs("BIG")).containsExactlyElementsOf(BIG);

        Set<String> all = new HashSet<>();
        all.addAll(TINY);
        all.addAll(LITTLE);
        all.addAll(BIG);
        assertThat(all).as("no course is in two clubs").hasSize(TINY.size() + LITTLE.size() + BIG.size());
        List<String> published = jdbc.sql("SELECT slug FROM course WHERE status = 'PUBLISHED'")
                .query(String.class).list();
        assertThat(all).as("no published course is left out").containsExactlyInAnyOrderElementsOf(published);
    }

    @Test
    @DisplayName("a child's home lists exactly their own club's courses")
    void homeShowsOnlyTheChildsClub() throws Exception {
        for (Map.Entry<Integer, List<String>> club : Map.of(3, TINY, 5, LITTLE, 7, BIG).entrySet()) {
            Family f = journeys.family(club.getKey());
            journeys.enterChildMode(f);
            MvcResult home = journeys.getJson(f.session(), "/api/v1/learn/home");
            List<String> slugs = Journeys.read(home, "$.courses[*].slug");
            assertThat(slugs).as("age %d", club.getKey()).containsExactlyElementsOf(club.getValue());
        }
    }

    @Test
    @DisplayName("a Tiny Cub cannot open a Little or Big course, lesson, card or quiz; each answer is a 404")
    void tinyCannotReachOtherClubs() throws Exception {
        Family f = journeys.family(3);
        journeys.enterChildMode(f);

        mvc.perform(get("/api/v1/learn/courses/stories").session(f.session())).andExpect(status().isNotFound());
        mvc.perform(get("/api/v1/learn/courses/alphabets").session(f.session())).andExpect(status().isNotFound());
        mvc.perform(get("/api/v1/learn/lessons/" + journeys.lessonIds("birds").getFirst()).session(f.session()))
                .andExpect(status().isNotFound());
        long numbersCard = jdbc.sql("""
                        SELECT i.id FROM lesson_item i JOIN lesson l ON l.id = i.lesson_id JOIN course c ON c.id = l.course_id
                        WHERE c.slug = 'numbers' AND i.status = 'READY' ORDER BY l.sort_order, i.sort_order LIMIT 1""")
                .query(Long.class).single();
        mvc.perform(put("/api/v1/learn/items/" + numbersCard + "/view").with(realCsrf()).session(f.session()))
                .andExpect(status().isNotFound());
        long flowersQuiz = journeys.quizId("flowers");
        mvc.perform(get("/api/v1/learn/quizzes/" + flowersQuiz).session(f.session())).andExpect(status().isNotFound());
        mvc.perform(post("/api/v1/learn/quizzes/" + flowersQuiz + "/attempts").with(realCsrf()).session(f.session()))
                .andExpect(status().isNotFound());

        int views = jdbc.sql("SELECT COUNT(*) FROM lesson_item_view WHERE child_id = :c").param("c", f.childId())
                .query(Integer.class).single();
        assertThat(views).as("nothing was recorded for another club's card").isZero();
    }

    @Test
    @DisplayName("a Little Cub opens Little courses but not Tiny or Big ones; a Big Cub opens Big courses")
    void littleAndBigGetTheirOwnSets() throws Exception {
        Family little = journeys.family(5);
        journeys.enterChildMode(little);
        mvc.perform(get("/api/v1/learn/courses/numbers").session(little.session())).andExpect(status().isOk());
        mvc.perform(get("/api/v1/learn/lessons/" + journeys.lessonIds("alphabets").getFirst())
                .session(little.session())).andExpect(status().isOk());
        mvc.perform(get("/api/v1/learn/courses/colours").session(little.session())).andExpect(status().isNotFound());
        mvc.perform(get("/api/v1/learn/courses/stories").session(little.session())).andExpect(status().isNotFound());

        Family big = journeys.family(7);
        journeys.enterChildMode(big);
        mvc.perform(get("/api/v1/learn/courses/stories").session(big.session())).andExpect(status().isOk());
        mvc.perform(get("/api/v1/learn/quizzes/" + journeys.quizId("birds")).session(big.session()))
                .andExpect(status().isOk());
        mvc.perform(get("/api/v1/learn/courses/rhymes").session(big.session())).andExpect(status().isNotFound());
    }
}
