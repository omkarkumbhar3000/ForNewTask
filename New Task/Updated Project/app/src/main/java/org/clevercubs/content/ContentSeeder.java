package org.clevercubs.content;

import java.io.IOException;
import java.io.InputStream;
import java.time.Instant;
import java.util.ArrayList;
import java.util.Comparator;
import java.util.List;
import java.util.Map;
import java.util.regex.Pattern;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.boot.ApplicationArguments;
import org.springframework.boot.ApplicationRunner;
import org.springframework.core.annotation.Order;
import org.springframework.core.io.Resource;
import org.springframework.core.io.support.PathMatchingResourcePatternResolver;
import org.springframework.jdbc.core.simple.JdbcClient;
import org.springframework.jdbc.support.GeneratedKeyHolder;
import org.springframework.stereotype.Component;
import org.springframework.transaction.support.TransactionTemplate;

import com.fasterxml.jackson.annotation.JsonIgnoreProperties;

import tools.jackson.databind.ObjectMapper;

/**
 * Loads the course content into an empty database on first start. The content comes from the JSON files in
 * {@code resources/content/}, produced once from the baseline by {@code tools/extract_content.py}; the
 * application never reads the baseline folder itself.
 *
 * <p>It also seeds the rewards (one score badge per quiz course, D64; a completion badge per media course and
 * per program, DD-21) and fills every Year-1 program with the published courses (DD-20). It runs only when
 * the course table is empty, so an administrator's later edits are never overwritten.
 */
@Component
@Order(10)
class ContentSeeder implements ApplicationRunner {

    private static final Logger log = LoggerFactory.getLogger(ContentSeeder.class);
    private static final Pattern MEDIA_PATH = Pattern.compile("^[a-z0-9-]+/[A-Za-z0-9._-]+$");

    @JsonIgnoreProperties(ignoreUnknown = true)
    record CourseJson(String slug, String title, String kind, String icon, String description, String coverImage,
            int sortOrder, List<LessonJson> lessons, QuizJson quiz, List<QuestionJson> reserveQuestions,
            Map<String, Object> diagram) {
    }

    @JsonIgnoreProperties(ignoreUnknown = true)
    record LessonJson(String title, int sortOrder, List<ItemJson> items) {
    }

    @JsonIgnoreProperties(ignoreUnknown = true)
    record ItemJson(int sortOrder, String label, String word, String emoji, String description, String image,
            String audio, String video, String lyrics, String alt, String status) {
    }

    @JsonIgnoreProperties(ignoreUnknown = true)
    record QuizJson(String title, Integer passMarkPercent, List<QuestionJson> questions) {
    }

    @JsonIgnoreProperties(ignoreUnknown = true)
    record QuestionJson(String prompt, List<String> options, int answerIndex) {
    }

    private final JdbcClient jdbc;
    private final ObjectMapper json;
    private final TransactionTemplate tx;

    ContentSeeder(JdbcClient jdbc, ObjectMapper json, TransactionTemplate tx) {
        this.jdbc = jdbc;
        this.json = json;
        this.tx = tx;
    }

    @Override
    public void run(ApplicationArguments args) throws IOException {
        int existing = jdbc.sql("SELECT COUNT(*) FROM course").query(Integer.class).single();
        if (existing > 0) {
            return;
        }
        List<CourseJson> courses = read();
        tx.executeWithoutResult(status -> {
            Instant now = Instant.now();
            for (CourseJson c : courses) {
                insertCourse(c, now);
            }
            seedPrograms();
        });
        log.info("Seeded {} courses from resources/content", courses.size());
    }

    private List<CourseJson> read() throws IOException {
        Resource[] files = new PathMatchingResourcePatternResolver().getResources("classpath*:content/*.json");
        List<CourseJson> courses = new ArrayList<>();
        for (Resource file : files) {
            try (InputStream in = file.getInputStream()) {
                courses.add(json.readValue(in, CourseJson.class));
            }
        }
        courses.sort(Comparator.comparingInt(CourseJson::sortOrder));
        return courses;
    }

    private void insertCourse(CourseJson c, Instant now) {
        String icon = c.icon() != null ? c.icon() : ("rhymes".equals(c.slug()) ? "🎵" : "📖");
        long courseId = insert("""
                        INSERT INTO course (slug, title, description, icon, cover_image, diagram, kind, status,
                                            sort_order, created_at, updated_at)
                        VALUES (:slug, :title, :description, :icon, :cover, :diagram, :kind, 'PUBLISHED', :sort,
                                :now, :now)""",
                Map.of("slug", c.slug(), "title", c.title(), "description", c.description(), "icon", icon,
                        "kind", c.kind(), "sort", c.sortOrder(), "now", now),
                nullable("cover", media(c.coverImage()),
                        "diagram", c.diagram() == null ? null : json.writeValueAsString(diagram(c.diagram()))));

        for (LessonJson l : c.lessons()) {
            long lessonId = insert("""
                            INSERT INTO lesson (course_id, title, sort_order, status, created_at, updated_at)
                            VALUES (:course, :title, :sort, 'PUBLISHED', :now, :now)""",
                    Map.of("course", courseId, "title", l.title(), "sort", l.sortOrder(), "now", now), Map.of());
            for (ItemJson i : l.items()) {
                String alt = i.alt() != null ? i.alt() : (i.word() != null ? i.word() : i.label());
                jdbc.sql("""
                                INSERT INTO lesson_item (lesson_id, sort_order, label, word, emoji, description,
                                                         image_path, audio_path, video_path, alt_text, lyrics, status)
                                VALUES (:lesson, :sort, :label, :word, :emoji, :description, :image, :audio, :video,
                                        :alt, :lyrics, :status)""")
                        .param("lesson", lessonId)
                        .param("sort", i.sortOrder())
                        .param("label", i.label())
                        .param("word", i.word())
                        .param("emoji", i.emoji())
                        .param("description", i.description())
                        .param("image", media(i.image()))
                        .param("audio", media(i.audio()))
                        .param("video", media(i.video()))
                        .param("alt", alt == null ? "Picture" : alt)
                        .param("lyrics", i.lyrics())
                        .param("status", "MEDIA_MISSING".equals(i.status()) ? "MEDIA_MISSING" : "READY")
                        .update();
            }
        }

        if (c.quiz() != null && !c.quiz().questions().isEmpty()) {
            int passMark = c.quiz().passMarkPercent() == null ? 70 : c.quiz().passMarkPercent();
            long quizId = insert("""
                            INSERT INTO quiz (course_id, title, pass_mark_percent, required, status, created_at,
                                              updated_at)
                            VALUES (:course, :title, :pass, TRUE, 'PUBLISHED', :now, :now)""",
                    Map.of("course", courseId, "title", c.quiz().title(), "pass", passMark, "now", now), Map.of());
            insertQuestions(quizId, "MAIN", c.quiz().questions());
            if (c.reserveQuestions() != null) {
                insertQuestions(quizId, "RESERVE", c.reserveQuestions());
            }
            badge("quiz-star-" + c.slug(), c.title() + " Star", "Earned with a great score in the " + c.title()
                    + " quiz.", "⭐", "QUIZ_BEST_SCORE", courseId, null);
        } else {
            String title = "rhymes".equals(c.slug()) ? "Rhyme Explorer"
                    : "stories".equals(c.slug()) ? "Story Explorer" : c.title() + " Explorer";
            badge("done-" + c.slug(), title, "Finished every lesson in " + c.title() + ".", icon,
                    "COURSE_COMPLETED", courseId, null);
        }
    }

    private void insertQuestions(long quizId, String pool, List<QuestionJson> questions) {
        int order = 1;
        for (QuestionJson q : questions) {
            long questionId = insert("""
                            INSERT INTO quiz_question (quiz_id, pool, sort_order, prompt)
                            VALUES (:quiz, :pool, :sort, :prompt)""",
                    Map.of("quiz", quizId, "pool", pool, "sort", order++, "prompt", q.prompt()), Map.of());
            for (int o = 0; o < q.options().size(); o++) {
                jdbc.sql("""
                                INSERT INTO quiz_option (question_id, sort_order, label, is_correct)
                                VALUES (:question, :sort, :label, :correct)""")
                        .param("question", questionId)
                        .param("sort", o + 1)
                        .param("label", q.options().get(o))
                        .param("correct", o == q.answerIndex())
                        .update();
            }
        }
    }

    /** DD-20: every Year-1 program starts with every published course, in course order. */
    private void seedPrograms() {
        jdbc.sql("""
                        INSERT IGNORE INTO program_course (program_id, course_id, sort_order)
                        SELECT p.id, c.id, c.sort_order FROM program p CROSS JOIN course c
                        WHERE p.year_number = 1 AND c.status = 'PUBLISHED'""")
                .update();
        List<Map<String, Object>> programs = jdbc.sql("""
                        SELECT p.id, g.code, g.name FROM program p JOIN age_group g ON g.id = p.age_group_id""")
                .query().listOfRows();
        for (Map<String, Object> p : programs) {
            badge("program-" + p.get("code").toString().toLowerCase() + "-" + p.get("id"), "Year of Learning",
                    "Completed a whole year of learning in " + p.get("name") + ".", "🎓", "PROGRAM_COMPLETED", null,
                    ((Number) p.get("id")).longValue());
        }
    }

    private void badge(String code, String title, String description, String icon, String criteria,
            Long courseId, Long programId) {
        jdbc.sql("""
                        INSERT IGNORE INTO badge (code, title, description, icon, criteria, course_id, program_id,
                                                  active)
                        VALUES (:code, :title, :description, :icon, :criteria, :course, :program, TRUE)""")
                .param("code", code)
                .param("title", title)
                .param("description", description)
                .param("icon", icon)
                .param("criteria", criteria)
                .param("course", courseId)
                .param("program", programId)
                .update();
    }

    /** Media paths must be relative {@code folder/name}; anything else is refused before it is stored. */
    private static String media(String path) {
        if (path == null) {
            return null;
        }
        if (!MEDIA_PATH.matcher(path).matches() || path.contains("..")) {
            throw new IllegalStateException("Unsafe media path in content: " + path);
        }
        return path;
    }

    private Map<String, Object> diagram(Map<String, Object> d) {
        Object image = d.get("image");
        if (image instanceof String s) {
            media(s);
        }
        return d;
    }

    private static Map<String, Object> nullable(Object... keysAndValues) {
        Map<String, Object> m = new java.util.HashMap<>();
        for (int i = 0; i < keysAndValues.length; i += 2) {
            m.put((String) keysAndValues[i], keysAndValues[i + 1]);
        }
        return m;
    }

    /** Inserts one row and returns its generated id. Nullable values go in {@code nullable}. */
    private long insert(String sql, Map<String, ?> params, Map<String, ?> nullable) {
        var spec = jdbc.sql(sql).params(params);
        for (var e : nullable.entrySet()) {
            spec = spec.param(e.getKey(), e.getValue());
        }
        GeneratedKeyHolder keys = new GeneratedKeyHolder();
        spec.update(keys);
        return keys.getKey().longValue();
    }
}
