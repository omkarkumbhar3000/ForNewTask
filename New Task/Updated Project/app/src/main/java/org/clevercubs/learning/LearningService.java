package org.clevercubs.learning;

import java.time.Instant;
import java.util.ArrayList;
import java.util.List;
import java.util.Map;
import java.util.Optional;

import org.clevercubs.child.AgeGroups.AgeGroup;
import org.clevercubs.child.ChildService;
import org.clevercubs.child.ChildService.ChildRow;
import org.clevercubs.child.ChildService.ChildView;
import org.clevercubs.learning.ProgressService.CourseProgress;
import org.clevercubs.platform.web.ApiException;
import org.clevercubs.reward.RewardService;
import org.clevercubs.reward.RewardService.BadgeView;
import org.clevercubs.reward.RewardService.ProgramOutcome;
import org.springframework.jdbc.core.simple.JdbcClient;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

/**
 * What a child sees and does while learning (requirement section 9): the home page with course cards and
 * a resume target, a course with its lessons and quiz state, a lesson with its cards, and "I opened this
 * card". Every call is for the session's active child; the child id is never taken from the request.
 */
@Service
public class LearningService {

    public record Resume(String courseSlug, String courseTitle, Long lessonId, String lessonTitle,
            boolean quizNext) {
    }

    public record Home(ChildView child, String greeting, String encouragement, String programTitle,
            int programPercent, boolean programCompleted, List<CourseProgress> courses, Resume resume,
            int badgesEarned) {
    }

    public record LessonSummary(long id, String title, int sortOrder, int itemsTotal, int itemsViewed,
            boolean done, boolean comingSoon) {
    }

    public record CourseView(CourseProgress course, List<LessonSummary> lessons, String diagram,
            String quizIntro, Long nextLessonId) {
    }

    public record ItemView(long id, int sortOrder, String label, String word, String emoji, String description,
            String image, String audio, String video, String alt, String lyrics, boolean ready, boolean viewed) {
    }

    public record LessonView(long id, String title, int sortOrder, String courseSlug, String courseTitle,
            String courseKind, String diagram, List<ItemView> items, Long previousLessonId, Long nextLessonId,
            boolean done, String startMessage, String doneMessage, int lessonCount) {
    }

    public record ViewResult(boolean lessonDone, boolean lessonJustDone, int coursePercent, boolean courseCompleted,
            boolean quizUnlocked, List<BadgeView> newBadges, boolean programCompleted, String message) {
    }

    private final JdbcClient jdbc;
    private final ChildService children;
    private final ProgressService progress;
    private final RewardService rewards;
    private final Messages messages;

    public LearningService(JdbcClient jdbc, ChildService children, ProgressService progress, RewardService rewards,
            Messages messages) {
        this.jdbc = jdbc;
        this.children = children;
        this.progress = progress;
        this.rewards = rewards;
        this.messages = messages;
    }

    public ChildRow child(long childId) {
        return children.find(childId).orElseThrow(() -> ApiException.notFound("Child"));
    }

    public Home home(long childId) {
        ChildRow child = child(childId);
        AgeGroup group = children.groupOf(child);
        Map<Long, CourseProgress> all = progress.forChild(childId);

        Optional<Map<String, Object>> enrolment = jdbc.sql("""
                        SELECT e.program_id, e.status, p.title FROM program_enrolment e
                        JOIN program p ON p.id = e.program_id
                        WHERE e.child_id = :c ORDER BY e.status = 'ACTIVE' DESC, e.started_at DESC LIMIT 1""")
                .param("c", childId).query().listOfRows().stream().findFirst();

        List<CourseProgress> courses = new ArrayList<>();
        String programTitle = null;
        boolean programCompleted = false;
        if (enrolment.isPresent()) {
            long programId = ((Number) enrolment.get().get("program_id")).longValue();
            programTitle = (String) enrolment.get().get("title");
            programCompleted = "COMPLETED".equals(enrolment.get().get("status"));
            for (Long id : progress.programCourseIds(programId)) {
                if (all.containsKey(id)) {
                    courses.add(all.get(id));
                }
            }
        }
        if (courses.isEmpty()) {
            courses.addAll(all.values());
        }
        int programPercent = ProgressRules.average(courses.stream().mapToInt(CourseProgress::percent).toArray());
        int badges = jdbc.sql("SELECT COUNT(*) FROM child_badge WHERE child_id = :c").param("c", childId)
                .query(Integer.class).single();

        return new Home(children.view(child),
                messages.pick("home.greeting", group.id(), Map.of("name", child.displayName())),
                messages.pick("encourage", group.id()), programTitle, programPercent, programCompleted, courses,
                resume(childId, courses), badges);
    }

    /** Where "Continue learning" goes: the course last worked on, else the first unfinished course. */
    Resume resume(long childId, List<CourseProgress> courses) {
        Optional<Long> lastCourse = jdbc.sql("""
                        SELECT l.course_id FROM lesson_item_view v
                        JOIN lesson_item i ON i.id = v.lesson_item_id JOIN lesson l ON l.id = i.lesson_id
                        WHERE v.child_id = :c ORDER BY v.first_viewed_at DESC LIMIT 1""")
                .param("c", childId).query(Long.class).optional();
        List<CourseProgress> order = new ArrayList<>();
        lastCourse.flatMap(id -> courses.stream().filter(c -> c.courseId() == id).findFirst())
                .filter(c -> !c.completed())
                .ifPresent(order::add);
        courses.stream().filter(c -> !c.completed()).forEach(order::add);
        for (CourseProgress c : order) {
            Optional<Map<String, Object>> lesson = nextLesson(childId, c.courseId());
            if (lesson.isPresent()) {
                return new Resume(c.slug(), c.title(), ((Number) lesson.get().get("id")).longValue(),
                        (String) lesson.get().get("title"), false);
            }
            if (c.quiz() != null && !c.quiz().passed()) {
                return new Resume(c.slug(), c.title(), null, null, true);
            }
        }
        return null;
    }

    private Optional<Map<String, Object>> nextLesson(long childId, long courseId) {
        return jdbc.sql("""
                        SELECT l.id, l.title FROM lesson l
                        WHERE l.course_id = :course AND l.status = 'PUBLISHED'
                          AND EXISTS (SELECT 1 FROM lesson_item i WHERE i.lesson_id = l.id AND i.status = 'READY')
                          AND NOT EXISTS (SELECT 1 FROM lesson_completion lc WHERE lc.lesson_id = l.id AND lc.child_id = :c)
                        ORDER BY l.sort_order LIMIT 1""")
                .param("course", courseId).param("c", childId).query().listOfRows().stream().findFirst();
    }

    public CourseView course(long childId, String slug) {
        ChildRow child = child(childId);
        Map<String, Object> course = jdbc.sql("""
                        SELECT id, diagram FROM course WHERE slug = :slug AND status = 'PUBLISHED'""")
                .param("slug", slug).query().listOfRows().stream().findFirst()
                .orElseThrow(() -> ApiException.notFound("Course"));
        long courseId = ((Number) course.get("id")).longValue();
        CourseProgress p = progress.forChild(childId).get(courseId);
        List<LessonSummary> lessons = jdbc.sql("""
                        SELECT l.id, l.title, l.sort_order,
                               (SELECT COUNT(*) FROM lesson_item i WHERE i.lesson_id = l.id AND i.status = 'READY') AS total,
                               (SELECT COUNT(*) FROM lesson_item i JOIN lesson_item_view v ON v.lesson_item_id = i.id
                                 WHERE i.lesson_id = l.id AND i.status = 'READY' AND v.child_id = :c) AS viewed,
                               EXISTS (SELECT 1 FROM lesson_completion lc WHERE lc.lesson_id = l.id AND lc.child_id = :c) AS done
                        FROM lesson l WHERE l.course_id = :course AND l.status = 'PUBLISHED' ORDER BY l.sort_order""")
                .param("c", childId).param("course", courseId)
                .query((rs, n) -> new LessonSummary(rs.getLong("id"), rs.getString("title"), rs.getInt("sort_order"),
                        rs.getInt("total"), rs.getInt("viewed"), rs.getBoolean("done"), rs.getInt("total") == 0))
                .list();
        Long next = nextLesson(childId, courseId).map(m -> ((Number) m.get("id")).longValue()).orElse(null);
        AgeGroup group = children.groupOf(child);
        return new CourseView(p, lessons, diagramOf(course.get("diagram")), messages.pick("quiz.intro", group.id()),
                next);
    }

    public LessonView lesson(long childId, long lessonId) {
        ChildRow child = child(childId);
        Map<String, Object> lesson = jdbc.sql("""
                        SELECT l.id, l.title, l.sort_order, l.course_id, c.slug, c.title AS course_title, c.kind, c.diagram
                        FROM lesson l JOIN course c ON c.id = l.course_id
                        WHERE l.id = :id AND l.status = 'PUBLISHED' AND c.status = 'PUBLISHED'""")
                .param("id", lessonId).query().listOfRows().stream().findFirst()
                .orElseThrow(() -> ApiException.notFound("Lesson"));
        long courseId = ((Number) lesson.get("course_id")).longValue();
        int sort = ((Number) lesson.get("sort_order")).intValue();

        List<ItemView> items = jdbc.sql("""
                        SELECT i.*, EXISTS (SELECT 1 FROM lesson_item_view v
                                            WHERE v.lesson_item_id = i.id AND v.child_id = :c) AS viewed
                        FROM lesson_item i WHERE i.lesson_id = :l ORDER BY i.sort_order""")
                .param("c", childId).param("l", lessonId)
                .query((rs, n) -> new ItemView(rs.getLong("id"), rs.getInt("sort_order"), rs.getString("label"),
                        rs.getString("word"), rs.getString("emoji"), rs.getString("description"),
                        ProgressService.media(rs.getString("image_path")),
                        ProgressService.media(rs.getString("audio_path")),
                        ProgressService.media(rs.getString("video_path")), rs.getString("alt_text"),
                        rs.getString("lyrics"), "READY".equals(rs.getString("status")), rs.getBoolean("viewed")))
                .list();

        Long previous = neighbour(courseId, sort, "<", "DESC");
        Long next = neighbour(courseId, sort, ">", "ASC");
        boolean done = jdbc.sql("SELECT COUNT(*) FROM lesson_completion WHERE child_id = :c AND lesson_id = :l")
                .param("c", childId).param("l", lessonId).query(Integer.class).single() > 0;
        int count = jdbc.sql("SELECT COUNT(*) FROM lesson WHERE course_id = :course AND status = 'PUBLISHED'")
                .param("course", courseId).query(Integer.class).single();
        AgeGroup group = children.groupOf(child);
        return new LessonView(lessonId, (String) lesson.get("title"), sort, (String) lesson.get("slug"),
                (String) lesson.get("course_title"), (String) lesson.get("kind"), diagramOf(lesson.get("diagram")),
                items, previous, next, done, messages.pick("lesson.start", group.id()),
                messages.pick("lesson.done", group.id()), count);
    }

    private Long neighbour(long courseId, int sort, String op, String dir) {
        return jdbc.sql("SELECT id FROM lesson WHERE course_id = :course AND status = 'PUBLISHED' AND sort_order "
                        + op + " :sort ORDER BY sort_order " + dir + " LIMIT 1")
                .param("course", courseId).param("sort", sort).query(Long.class).optional().orElse(null);
    }

    /**
     * "I opened this card" (a picture or sound) or "I watched this video to the end" (DD-17). Idempotent. The
     * server then decides whether the lesson is complete, the course progress, and any reward.
     */
    @Transactional
    public ViewResult viewItem(long childId, long itemId) {
        ChildRow child = child(childId);
        Map<String, Object> item = jdbc.sql("""
                        SELECT i.id, i.lesson_id, i.status, l.course_id FROM lesson_item i
                        JOIN lesson l ON l.id = i.lesson_id JOIN course c ON c.id = l.course_id
                        WHERE i.id = :id AND l.status = 'PUBLISHED' AND c.status = 'PUBLISHED'""")
                .param("id", itemId).query().listOfRows().stream().findFirst()
                .orElseThrow(() -> ApiException.notFound("Card"));
        if (!"READY".equals(item.get("status"))) {
            throw ApiException.rule("media-missing", "This one is coming soon.");
        }
        long lessonId = ((Number) item.get("lesson_id")).longValue();
        long courseId = ((Number) item.get("course_id")).longValue();

        jdbc.sql("""
                        INSERT IGNORE INTO lesson_item_view (child_id, lesson_item_id, first_viewed_at)
                        VALUES (:c, :i, :now)""")
                .param("c", childId).param("i", itemId).param("now", Instant.now()).update();

        int remaining = jdbc.sql("""
                        SELECT COUNT(*) FROM lesson_item i
                        WHERE i.lesson_id = :l AND i.status = 'READY'
                          AND NOT EXISTS (SELECT 1 FROM lesson_item_view v WHERE v.lesson_item_id = i.id AND v.child_id = :c)""")
                .param("l", lessonId).param("c", childId).query(Integer.class).single();
        boolean justDone = false;
        if (remaining == 0) {
            justDone = jdbc.sql("""
                            INSERT IGNORE INTO lesson_completion (child_id, lesson_id, completed_at)
                            VALUES (:c, :l, :now)""")
                    .param("c", childId).param("l", lessonId).param("now", Instant.now()).update() == 1;
        }

        Map<Long, CourseProgress> all = progress.forChild(childId);
        CourseProgress course = all.get(courseId);
        List<BadgeView> badges = new ArrayList<>();
        boolean programDone = false;
        if (justDone) {
            badges.addAll(rewards.afterProgress(childId, Map.of(courseId, course)));
            ProgramOutcome outcome = rewards.checkPrograms(childId, all);
            badges.addAll(outcome.badges());
            programDone = outcome.completed();
        }
        AgeGroup group = children.groupOf(child);
        return new ViewResult(remaining == 0, justDone, course.percent(), course.completed(),
                course.quiz() != null && course.quiz().unlocked(), badges, programDone,
                justDone ? messages.pick("lesson.done", group.id()) : null);
    }

    private static String diagramOf(Object value) {
        return value == null ? null : value.toString();
    }
}
