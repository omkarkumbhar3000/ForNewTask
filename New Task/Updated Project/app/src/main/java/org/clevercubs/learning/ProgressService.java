package org.clevercubs.learning;

import java.util.HashMap;
import java.util.HashSet;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;
import java.util.Set;

import org.clevercubs.platform.settings.Settings;
import org.clevercubs.quiz.QuizRules;
import org.springframework.jdbc.core.simple.JdbcClient;
import org.springframework.stereotype.Service;

/**
 * Computes a child's progress in every published course from the stored records only: lesson completions,
 * submitted quiz attempts and the attempt allowance (requirement section 10, DD-07). The browser never sends
 * a progress value. A handful of grouped queries per call, whatever the number of courses.
 */
@Service
public class ProgressService {

    public record QuizState(long quizId, String title, boolean required, int passMark, boolean unlocked,
            int attemptsAllowed, int attemptsUsed, int attemptsRemaining, Integer bestScore, boolean passed,
            boolean locked, Long inProgressAttemptId, boolean requestPending, int attemptsSubmitted) {
    }

    public record CourseProgress(long courseId, String slug, String title, String description, String icon,
            String coverImage, String kind, int sortOrder, int lessonsTotal, int lessonsDone, int percent,
            boolean started, boolean completed, QuizState quiz) {
    }

    private record Quiz(long id, long courseId, String title, boolean required, int passMark) {
    }

    private final JdbcClient jdbc;
    private final Settings settings;

    public ProgressService(JdbcClient jdbc, Settings settings) {
        this.jdbc = jdbc;
        this.settings = settings;
    }

    /** Progress in every published course, in course order, keyed by course id. */
    public Map<Long, CourseProgress> forChild(long childId) {
        int lessonWeight = settings.intValue(Settings.LESSON_WEIGHT);
        int defaultAllowed = settings.intValue(Settings.MAX_ATTEMPTS);

        Map<Long, Integer> totals = counts("""
                SELECT l.course_id, COUNT(*) FROM lesson l
                WHERE l.status = 'PUBLISHED'
                  AND EXISTS (SELECT 1 FROM lesson_item i WHERE i.lesson_id = l.id AND i.status = 'READY')
                GROUP BY l.course_id""", Map.of());
        Map<Long, Integer> done = counts("""
                SELECT l.course_id, COUNT(*) FROM lesson_completion lc JOIN lesson l ON l.id = lc.lesson_id
                WHERE lc.child_id = :child AND l.status = 'PUBLISHED'
                  AND EXISTS (SELECT 1 FROM lesson_item i WHERE i.lesson_id = l.id AND i.status = 'READY')
                GROUP BY l.course_id""", Map.of("child", childId));
        Map<Long, Integer> views = counts("""
                SELECT l.course_id, COUNT(*) FROM lesson_item_view v
                JOIN lesson_item i ON i.id = v.lesson_item_id JOIN lesson l ON l.id = i.lesson_id
                WHERE v.child_id = :child GROUP BY l.course_id""", Map.of("child", childId));

        Map<Long, Quiz> quizByCourse = new HashMap<>();
        jdbc.sql("SELECT id, course_id, title, required, pass_mark_percent FROM quiz WHERE status = 'PUBLISHED'")
                .query((rs, n) -> new Quiz(rs.getLong(1), rs.getLong(2), rs.getString(3), rs.getBoolean(4),
                        rs.getInt(5)))
                .list()
                .forEach(q -> quizByCourse.put(q.courseId(), q));

        Map<Long, int[]> submitted = new HashMap<>(); // quiz -> {best, passed(0/1), count}
        jdbc.sql("""
                        SELECT quiz_id, MAX(score_percent), MAX(CASE WHEN passed THEN 1 ELSE 0 END), COUNT(*)
                        FROM quiz_attempt WHERE child_id = :child AND status = 'SUBMITTED' GROUP BY quiz_id""")
                .param("child", childId)
                .query((rs, n) -> Map.entry(rs.getLong(1), new int[] {rs.getInt(2), rs.getInt(3), rs.getInt(4)}))
                .list()
                .forEach(e -> submitted.put(e.getKey(), e.getValue()));

        Map<Long, int[]> allowance = new HashMap<>(); // quiz -> {allowed, used}
        jdbc.sql("SELECT quiz_id, attempts_allowed, attempts_used FROM quiz_allowance WHERE child_id = :child")
                .param("child", childId)
                .query((rs, n) -> Map.entry(rs.getLong(1), new int[] {rs.getInt(2), rs.getInt(3)}))
                .list()
                .forEach(e -> allowance.put(e.getKey(), e.getValue()));

        Map<Long, Long> open = new HashMap<>();
        jdbc.sql("SELECT quiz_id, id FROM quiz_attempt WHERE child_id = :child AND status = 'IN_PROGRESS'")
                .param("child", childId)
                .query((rs, n) -> Map.entry(rs.getLong(1), rs.getLong(2)))
                .list()
                .forEach(e -> open.put(e.getKey(), e.getValue()));

        Set<Long> pending = new HashSet<>(jdbc.sql("""
                        SELECT quiz_id FROM parent_request
                        WHERE child_id = :child AND type = 'QUIZ_ATTEMPTS' AND status = 'PENDING'""")
                .param("child", childId).query(Long.class).list());

        Map<Long, CourseProgress> result = new LinkedHashMap<>();
        jdbc.sql("""
                        SELECT id, slug, title, description, icon, cover_image, kind, sort_order FROM course
                        WHERE status = 'PUBLISHED' ORDER BY sort_order, id""")
                .query((rs, n) -> {
                    long courseId = rs.getLong("id");
                    int total = totals.getOrDefault(courseId, 0);
                    int completed = Math.min(done.getOrDefault(courseId, 0), total);
                    Quiz q = quizByCourse.get(courseId);
                    QuizState state = null;
                    boolean requiredQuiz = false;
                    boolean passed = false;
                    if (q != null) {
                        int[] s = submitted.getOrDefault(q.id(), new int[] {-1, 0, 0});
                        int[] a = allowance.getOrDefault(q.id(), new int[] {defaultAllowed, 0});
                        passed = s[1] == 1;
                        Long openAttempt = open.get(q.id());
                        boolean unlocked = openAttempt != null || (total > 0 && completed >= total);
                        state = new QuizState(q.id(), q.title(), q.required(), q.passMark(), unlocked, a[0], a[1],
                                Math.max(0, a[0] - a[1]), s[0] < 0 ? null : s[0], passed,
                                QuizRules.locked(a[1], a[0], passed, openAttempt != null), openAttempt,
                                pending.contains(q.id()), s[2]);
                        requiredQuiz = q.required();
                    }
                    int percent = ProgressRules.coursePercent(requiredQuiz, completed, total, passed, lessonWeight);
                    boolean started = views.getOrDefault(courseId, 0) > 0 || (state != null && state.attemptsUsed() > 0);
                    return new CourseProgress(courseId, rs.getString("slug"), rs.getString("title"),
                            rs.getString("description"), rs.getString("icon"), media(rs.getString("cover_image")),
                            rs.getString("kind"), rs.getInt("sort_order"), total, completed, percent, started,
                            percent >= 100, state);
                })
                .list()
                .forEach(c -> result.put(c.courseId(), c));
        return result;
    }

    /** The course ids of a program, in program order. */
    public List<Long> programCourseIds(long programId) {
        return jdbc.sql("""
                        SELECT pc.course_id FROM program_course pc JOIN course c ON c.id = pc.course_id
                        WHERE pc.program_id = :p AND c.status = 'PUBLISHED' ORDER BY pc.sort_order, c.sort_order""")
                .param("p", programId).query(Long.class).list();
    }

    static String media(String path) {
        return path == null ? null : "/media/" + path;
    }

    private Map<Long, Integer> counts(String sql, Map<String, ?> params) {
        Map<Long, Integer> m = new HashMap<>();
        jdbc.sql(sql).params(params)
                .query((rs, n) -> Map.entry(rs.getLong(1), rs.getInt(2)))
                .list()
                .forEach(e -> m.put(e.getKey(), e.getValue()));
        return m;
    }
}
