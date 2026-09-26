package org.clevercubs.quiz;

import java.time.Instant;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

import org.clevercubs.child.AgeGroups.AgeGroup;
import org.clevercubs.child.ChildService;
import org.clevercubs.child.ChildService.ChildRow;
import org.clevercubs.learning.Messages;
import org.clevercubs.learning.ProgressService;
import org.clevercubs.learning.ProgressService.CourseProgress;
import org.clevercubs.platform.settings.Settings;
import org.clevercubs.platform.web.ApiException;
import org.clevercubs.reward.RewardService;
import org.clevercubs.reward.RewardService.BadgeView;
import org.clevercubs.reward.RewardService.ProgramOutcome;
import org.springframework.jdbc.core.simple.JdbcClient;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Isolation;
import org.springframework.transaction.annotation.Transactional;

/**
 * Quiz attempts (requirement section 11). The backend is the only judge:
 *
 * <ul>
 *   <li>A quiz opens once its lessons are complete (DD-16).</li>
 *   <li>An attempt is used when it starts (DD-19). The allowance row is locked first, so two simultaneous
 *       starts can neither exceed the limit nor open two attempts. Reopening the quiz resumes the open attempt
 *       without using another one.</li>
 *   <li>Each answer is final and is scored here; which option is correct is never sent before the answer.</li>
 *   <li>After the last answer the attempt is scored, passed at the quiz's pass mark (D62), and rewards and
 *       progress follow. With no attempts left and no pass, the quiz is locked until a parent grants more
 *       (D63).</li>
 * </ul>
 */
@Service
public class QuizService {

    public record OptionView(long id, String label) {
    }

    public record QuestionView(long id, int number, String prompt, List<OptionView> options, Long chosenOptionId,
            Boolean correct, Long correctOptionId) {
    }

    public record AttemptView(long attemptId, long quizId, String quizTitle, String courseSlug, String courseTitle,
            int attemptNumber, int attemptsAllowed, int questionCount, int answeredCount, boolean finished,
            List<QuestionView> questions, String intro, ResultView result) {
    }

    public record ResultView(int scorePercent, int correctCount, int questionCount, boolean passed, int passMark,
            int attemptsRemaining, boolean locked, Integer bestScore, String message, List<BadgeView> newBadges,
            int coursePercent, boolean courseCompleted, boolean programCompleted) {
    }

    public record AnswerResult(boolean correct, long correctOptionId, String message, boolean finished,
            ResultView result) {
    }

    /** What the quiz page shows before anything starts: reading it never uses an attempt. */
    public record QuizOverview(long quizId, String title, String courseSlug, String courseTitle, int questionCount,
            String intro, ProgressService.QuizState state) {
    }

    private record Attempt(long id, long childId, long quizId, int number, String status, int questionCount) {
    }

    private final JdbcClient jdbc;
    private final Settings settings;
    private final ProgressService progress;
    private final RewardService rewards;
    private final ChildService children;
    private final Messages messages;

    public QuizService(JdbcClient jdbc, Settings settings, ProgressService progress, RewardService rewards,
            ChildService children, Messages messages) {
        this.jdbc = jdbc;
        this.settings = settings;
        this.progress = progress;
        this.rewards = rewards;
        this.children = children;
        this.messages = messages;
    }

    /**
     * Starts a new attempt, or resumes the open one.
     *
     * <p>READ COMMITTED on purpose: a start that waited for the allowance lock must then see the attempt the
     * start before it committed, which MySQL's default REPEATABLE READ snapshot would hide. The upsert takes
     * an exclusive lock straight away (INSERT IGNORE would take a shared one and deadlock on the upgrade).
     */
    @Transactional(isolation = Isolation.READ_COMMITTED)
    public AttemptView start(long childId, long quizId) {
        Map<String, Object> quiz = quiz(quizId);
        long courseId = ((Number) quiz.get("course_id")).longValue();

        // Serialise every start for this child and quiz on the allowance row.
        jdbc.sql("""
                        INSERT INTO quiz_allowance (child_id, quiz_id, attempts_allowed, attempts_used, updated_at)
                        VALUES (:c, :q, :allowed, 0, :now)
                        ON DUPLICATE KEY UPDATE attempts_allowed = attempts_allowed""")
                .param("c", childId).param("q", quizId).param("allowed", settings.intValue(Settings.MAX_ATTEMPTS))
                .param("now", Instant.now()).update();
        int[] allowance = jdbc.sql("""
                        SELECT attempts_allowed, attempts_used FROM quiz_allowance
                        WHERE child_id = :c AND quiz_id = :q FOR UPDATE""")
                .param("c", childId).param("q", quizId)
                .query((rs, n) -> new int[] {rs.getInt(1), rs.getInt(2)}).single();

        Long open = jdbc.sql("""
                        SELECT id FROM quiz_attempt WHERE child_id = :c AND quiz_id = :q AND status = 'IN_PROGRESS'""")
                .param("c", childId).param("q", quizId).query(Long.class).optional().orElse(null);
        if (open != null) {
            return view(childId, open);
        }

        CourseProgress course = progress.forChild(childId).get(courseId);
        if (course == null || course.quiz() == null || !course.quiz().unlocked()) {
            throw ApiException.rule("quiz-not-ready", "Finish all the lessons first, then the quiz opens.");
        }
        if (allowance[1] >= allowance[0]) {
            throw ApiException.rule("quiz-locked",
                    "All tries are used for now. A grown-up can give you more tries.");
        }
        jdbc.sql("""
                        UPDATE quiz_allowance SET attempts_used = attempts_used + 1, updated_at = :now
                        WHERE child_id = :c AND quiz_id = :q AND attempts_used < attempts_allowed""")
                .param("now", Instant.now()).param("c", childId).param("q", quizId).update();

        int questions = jdbc.sql("SELECT COUNT(*) FROM quiz_question WHERE quiz_id = :q AND pool = 'MAIN'")
                .param("q", quizId).query(Integer.class).single();
        int number = jdbc.sql("SELECT COALESCE(MAX(attempt_number), 0) + 1 FROM quiz_attempt WHERE child_id = :c AND quiz_id = :q")
                .param("c", childId).param("q", quizId).query(Integer.class).single();
        jdbc.sql("""
                        INSERT INTO quiz_attempt (child_id, quiz_id, attempt_number, status, started_at, question_count)
                        VALUES (:c, :q, :n, 'IN_PROGRESS', :now, :questions)""")
                .param("c", childId).param("q", quizId).param("n", number).param("now", Instant.now())
                .param("questions", questions).update();
        long attemptId = jdbc.sql("SELECT id FROM quiz_attempt WHERE child_id = :c AND quiz_id = :q AND attempt_number = :n")
                .param("c", childId).param("q", quizId).param("n", number).query(Long.class).single();
        return view(childId, attemptId);
    }

    public QuizOverview overview(long childId, long quizId) {
        CourseProgress course = progress.forChild(childId).values().stream()
                .filter(c -> c.quiz() != null && c.quiz().quizId() == quizId)
                .findFirst()
                .orElseThrow(() -> ApiException.notFound("Quiz"));
        int questions = jdbc.sql("SELECT COUNT(*) FROM quiz_question WHERE quiz_id = :q AND pool = 'MAIN'")
                .param("q", quizId).query(Integer.class).single();
        ChildRow child = children.find(childId).orElseThrow(() -> ApiException.notFound("Child"));
        return new QuizOverview(quizId, course.quiz().title(), course.slug(), course.title(), questions,
                messages.pick("quiz.intro", children.groupOf(child).id()), course.quiz());
    }

    /** The attempt with its questions and the answers given so far (never the unanswered correct options). */
    public AttemptView view(long childId, long attemptId) {
        Attempt attempt = attempt(childId, attemptId, false);
        Map<String, Object> quiz = quiz(attempt.quizId());
        ChildRow child = children.find(childId).orElseThrow(() -> ApiException.notFound("Child"));
        AgeGroup group = children.groupOf(child);

        Map<Long, long[]> answers = new HashMap<>(); // question -> {option, correct(0/1)}
        jdbc.sql("SELECT question_id, option_id, is_correct FROM quiz_attempt_answer WHERE attempt_id = :a")
                .param("a", attemptId)
                .query((rs, n) -> Map.entry(rs.getLong(1), new long[] {rs.getLong(2), rs.getBoolean(3) ? 1 : 0}))
                .list().forEach(e -> answers.put(e.getKey(), e.getValue()));

        List<Map<String, Object>> rows = jdbc.sql("""
                        SELECT q.id AS qid, q.sort_order, q.prompt, o.id AS oid, o.label, o.is_correct
                        FROM quiz_question q JOIN quiz_option o ON o.question_id = q.id
                        WHERE q.quiz_id = :quiz AND q.pool = 'MAIN' ORDER BY q.sort_order, o.sort_order""")
                .param("quiz", attempt.quizId()).query().listOfRows();
        List<QuestionView> questions = new ArrayList<>();
        Map<Long, List<OptionView>> options = new java.util.LinkedHashMap<>();
        Map<Long, String> prompts = new HashMap<>();
        Map<Long, Long> correctOption = new HashMap<>();
        for (Map<String, Object> r : rows) {
            long qid = ((Number) r.get("qid")).longValue();
            prompts.put(qid, (String) r.get("prompt"));
            options.computeIfAbsent(qid, k -> new ArrayList<>())
                    .add(new OptionView(((Number) r.get("oid")).longValue(), (String) r.get("label")));
            if (truthy(r.get("is_correct"))) {
                correctOption.put(qid, ((Number) r.get("oid")).longValue());
            }
        }
        int number = 1;
        for (var e : options.entrySet()) {
            long[] a = answers.get(e.getKey());
            questions.add(new QuestionView(e.getKey(), number++, prompts.get(e.getKey()), e.getValue(),
                    a == null ? null : a[0], a == null ? null : a[1] == 1,
                    a == null ? null : correctOption.get(e.getKey())));
        }
        boolean finished = "SUBMITTED".equals(attempt.status());
        ResultView result = finished ? result(childId, attempt, List.of(), false) : null;
        return new AttemptView(attempt.id(), attempt.quizId(), (String) quiz.get("title"), (String) quiz.get("slug"),
                (String) quiz.get("course_title"), attempt.number(),
                allowance(childId, attempt.quizId())[0], attempt.questionCount(), answers.size(), finished,
                questions, messages.pick("quiz.intro", group.id()), result);
    }

    /** Scores one answer. Answering the same question again returns the first answer's result unchanged. */
    @Transactional(isolation = Isolation.READ_COMMITTED)
    public AnswerResult answer(long childId, long attemptId, long questionId, long optionId) {
        Attempt attempt = attempt(childId, attemptId, true);
        ChildRow child = children.find(childId).orElseThrow(() -> ApiException.notFound("Child"));
        AgeGroup group = children.groupOf(child);

        Map<String, Object> question = jdbc.sql("""
                        SELECT id FROM quiz_question WHERE id = :q AND quiz_id = :quiz AND pool = 'MAIN'""")
                .param("q", questionId).param("quiz", attempt.quizId()).query().listOfRows().stream().findFirst()
                .orElseThrow(() -> ApiException.notFound("Question"));
        List<Map<String, Object>> options = jdbc.sql(
                        "SELECT id, label, is_correct FROM quiz_option WHERE question_id = :q ORDER BY sort_order")
                .param("q", question.get("id")).query().listOfRows();
        Map<String, Object> correct = options.stream().filter(o -> truthy(o.get("is_correct"))).findFirst()
                .orElseThrow(() -> new IllegalStateException("Question " + questionId + " has no correct option"));
        long correctId = ((Number) correct.get("id")).longValue();

        List<long[]> existing = jdbc.sql("""
                        SELECT option_id, is_correct FROM quiz_attempt_answer WHERE attempt_id = :a AND question_id = :q""")
                .param("a", attemptId).param("q", questionId)
                .query((rs, n) -> new long[] {rs.getLong(1), rs.getBoolean(2) ? 1 : 0}).list();
        if (!existing.isEmpty()) {
            boolean wasCorrect = existing.getFirst()[1] == 1;
            return new AnswerResult(wasCorrect, correctId, "", "SUBMITTED".equals(attempt.status()),
                    "SUBMITTED".equals(attempt.status()) ? result(childId, attempt, List.of(), false) : null);
        }
        if (!"IN_PROGRESS".equals(attempt.status())) {
            throw ApiException.conflict("attempt-finished", "This quiz try is already finished.");
        }
        boolean isOption = options.stream().anyMatch(o -> ((Number) o.get("id")).longValue() == optionId);
        if (!isOption) {
            throw ApiException.badRequest("invalid-input", "Please pick one of the answers.");
        }
        boolean isCorrect = optionId == correctId;
        jdbc.sql("""
                        INSERT INTO quiz_attempt_answer (attempt_id, question_id, option_id, is_correct, answered_at)
                        VALUES (:a, :q, :o, :correct, :now)""")
                .param("a", attemptId).param("q", questionId).param("o", optionId).param("correct", isCorrect)
                .param("now", Instant.now()).update();
        if (isCorrect) {
            jdbc.sql("UPDATE quiz_attempt SET correct_count = correct_count + 1 WHERE id = :a")
                    .param("a", attemptId).update();
        }
        String message = isCorrect ? messages.pick("quiz.correct", group.id())
                : messages.pick("quiz.incorrect", group.id(), Map.of("answer", (String) correct.get("label")));

        int answered = jdbc.sql("SELECT COUNT(*) FROM quiz_attempt_answer WHERE attempt_id = :a")
                .param("a", attemptId).query(Integer.class).single();
        if (answered < attempt.questionCount()) {
            return new AnswerResult(isCorrect, correctId, message, false, null);
        }
        return new AnswerResult(isCorrect, correctId, message, true, submit(childId, attempt));
    }

    private ResultView submit(long childId, Attempt attempt) {
        Map<String, Object> quiz = quiz(attempt.quizId());
        int correct = jdbc.sql("SELECT correct_count FROM quiz_attempt WHERE id = :a").param("a", attempt.id())
                .query(Integer.class).single();
        int score = QuizRules.scorePercent(correct, attempt.questionCount());
        boolean passed = QuizRules.passed(score, ((Number) quiz.get("pass_mark_percent")).intValue());
        jdbc.sql("""
                        UPDATE quiz_attempt SET status = 'SUBMITTED', submitted_at = :now, score_percent = :score,
                               passed = :passed
                        WHERE id = :a AND status = 'IN_PROGRESS'""")
                .param("now", Instant.now()).param("score", score).param("passed", passed).param("a", attempt.id())
                .update();

        long courseId = ((Number) quiz.get("course_id")).longValue();
        List<BadgeView> badges = new ArrayList<>(rewards.afterQuiz(childId, courseId, attempt.quizId(), attempt.id()));
        Map<Long, CourseProgress> all = progress.forChild(childId);
        badges.addAll(rewards.afterProgress(childId, Map.of(courseId, all.get(courseId))));
        ProgramOutcome program = rewards.checkPrograms(childId, all);
        badges.addAll(program.badges());
        Attempt submitted = new Attempt(attempt.id(), attempt.childId(), attempt.quizId(), attempt.number(),
                "SUBMITTED", attempt.questionCount());
        return result(childId, submitted, badges, program.completed());
    }

    private ResultView result(long childId, Attempt attempt, List<BadgeView> badges, boolean programCompleted) {
        Map<String, Object> row = jdbc.sql("""
                        SELECT a.correct_count, a.score_percent, a.passed, q.pass_mark_percent, q.course_id
                        FROM quiz_attempt a JOIN quiz q ON q.id = a.quiz_id WHERE a.id = :a""")
                .param("a", attempt.id()).query().listOfRows().getFirst();
        CourseProgress course = progress.forChild(childId).get(((Number) row.get("course_id")).longValue());
        var state = course.quiz();
        boolean passed = truthy(row.get("passed"));
        ChildRow child = children.find(childId).orElseThrow(() -> ApiException.notFound("Child"));
        Long group = children.groupOf(child).id();
        String message = passed ? messages.pick("quiz.passed", group)
                : state.locked() ? messages.pick("quiz.locked", group) : messages.pick("quiz.not_passed", group);
        return new ResultView(((Number) row.get("score_percent")).intValue(),
                ((Number) row.get("correct_count")).intValue(), attempt.questionCount(), passed,
                ((Number) row.get("pass_mark_percent")).intValue(), state.attemptsRemaining(), state.locked(),
                state.bestScore(), message, badges, course.percent(), course.completed(), programCompleted);
    }

    private Attempt attempt(long childId, long attemptId, boolean forUpdate) {
        return jdbc.sql("""
                        SELECT id, child_id, quiz_id, attempt_number, status, question_count FROM quiz_attempt
                        WHERE id = :a AND child_id = :c""" + (forUpdate ? " FOR UPDATE" : ""))
                .param("a", attemptId).param("c", childId)
                .query((rs, n) -> new Attempt(rs.getLong(1), rs.getLong(2), rs.getLong(3), rs.getInt(4),
                        rs.getString(5), rs.getInt(6)))
                .optional()
                .orElseThrow(() -> ApiException.notFound("Quiz try"));
    }

    private Map<String, Object> quiz(long quizId) {
        return jdbc.sql("""
                        SELECT q.id, q.title, q.course_id, q.pass_mark_percent, c.slug, c.title AS course_title
                        FROM quiz q JOIN course c ON c.id = q.course_id
                        WHERE q.id = :q AND q.status = 'PUBLISHED' AND c.status = 'PUBLISHED'""")
                .param("q", quizId).query().listOfRows().stream().findFirst()
                .orElseThrow(() -> ApiException.notFound("Quiz"));
    }

    private int[] allowance(long childId, long quizId) {
        return jdbc.sql("SELECT attempts_allowed, attempts_used FROM quiz_allowance WHERE child_id = :c AND quiz_id = :q")
                .param("c", childId).param("q", quizId)
                .query((rs, n) -> new int[] {rs.getInt(1), rs.getInt(2)})
                .optional().orElse(new int[] {settings.intValue(Settings.MAX_ATTEMPTS), 0});
    }

    static boolean truthy(Object value) {
        return value instanceof Boolean b ? b : value instanceof Number n && n.intValue() != 0;
    }
}
