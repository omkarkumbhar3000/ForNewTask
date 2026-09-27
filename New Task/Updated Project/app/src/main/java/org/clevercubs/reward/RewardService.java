package org.clevercubs.reward;

import java.security.SecureRandom;
import java.time.Instant;
import java.time.LocalDateTime;
import java.util.ArrayList;
import java.util.List;
import java.util.Map;

import org.clevercubs.audit.AuditLog;
import org.clevercubs.learning.ProgressService;
import org.clevercubs.learning.ProgressService.CourseProgress;
import org.clevercubs.platform.db.Rows;
import org.clevercubs.platform.db.SqlDialect;
import org.clevercubs.platform.db.Timestamps;
import org.clevercubs.platform.settings.Settings;
import org.clevercubs.quiz.QuizRules;
import org.springframework.jdbc.core.simple.JdbcClient;
import org.springframework.stereotype.Service;

/**
 * Badges, certificates and program completion (requirement sections 13 and 16). Everything is awarded by
 * the server after the event that earns it; the browser can never ask for a reward.
 *
 * <ul>
 *   <li>Score badge: the best quiz score reaches {@code reward.threshold_percent} (80, compared with >=,
 *       D64).</li>
 *   <li>Completion badge: a course without a quiz reaches 100% (DD-21).</li>
 *   <li>Program: every course of an active Year program at 100% completes it, issues the certificate and
 *       the program badge (D65).</li>
 * </ul>
 * Rewards are private to the family: there are no leaderboards and no comparison between children.
 */
@Service
public class RewardService {

    public record BadgeView(long id, String code, String title, String description, String icon,
            boolean earned, Instant awardedAt) {
    }

    public record CertificateView(long id, long programId, String programTitle, String verificationCode,
            Instant issuedAt) {
    }

    public record ProgramOutcome(boolean completed, String programTitle, List<BadgeView> badges) {
    }

    private static final SecureRandom RANDOM = new SecureRandom();
    private static final String CODE_ALPHABET = "ABCDEFGHJKLMNPQRSTUVWXYZ23456789";

    private final JdbcClient jdbc;
    private final SqlDialect dialect;
    private final Settings settings;
    private final ProgressService progress;
    private final AuditLog audit;

    public RewardService(JdbcClient jdbc, Settings settings, ProgressService progress, AuditLog audit,
            SqlDialect dialect) {
        this.dialect = dialect;
        this.jdbc = jdbc;
        this.settings = settings;
        this.progress = progress;
        this.audit = audit;
    }

    /** After a submitted attempt: the course's score badge, if the best score now reaches the threshold. */
    public List<BadgeView> afterQuiz(long childId, long courseId, long quizId, long attemptId) {
        Integer best = jdbc.sql("""
                        SELECT MAX(score_percent) FROM quiz_attempt
                        WHERE child_id = :c AND quiz_id = :q AND status = 'SUBMITTED'""")
                .param("c", childId).param("q", quizId).query(Integer.class).optional().orElse(null);
        if (!QuizRules.earnsReward(best, settings.intValue(Settings.REWARD_THRESHOLD))) {
            return List.of();
        }
        return award(childId, "criteria = 'QUIZ_BEST_SCORE' AND course_id = :course", Map.of("course", courseId),
                attemptId);
    }

    /** After any progress change: completion badges for finished quiz-less courses, and program completion. */
    public List<BadgeView> afterProgress(long childId, Map<Long, CourseProgress> courses) {
        List<BadgeView> earned = new ArrayList<>();
        for (CourseProgress c : courses.values()) {
            if (c.completed() && (c.quiz() == null || !c.quiz().required())) {
                earned.addAll(award(childId, "criteria = 'COURSE_COMPLETED' AND course_id = :course",
                        Map.of("course", c.courseId()), null));
            }
        }
        return earned;
    }

    /** Completes every active program whose courses are all at 100%, once. */
    public ProgramOutcome checkPrograms(long childId, Map<Long, CourseProgress> courses) {
        List<Map<String, Object>> enrolments = jdbc.sql("""
                        SELECT e.id, e.program_id, p.title FROM program_enrolment e JOIN program p ON p.id = e.program_id
                        WHERE e.child_id = :c AND e.status = 'ACTIVE'""")
                .param("c", childId).query(Rows.MAP).list();
        for (Map<String, Object> e : enrolments) {
            long programId = ((Number) e.get("program_id")).longValue();
            List<Long> ids = progress.programCourseIds(programId);
            boolean allDone = !ids.isEmpty()
                    && ids.stream().allMatch(id -> courses.containsKey(id) && courses.get(id).completed());
            if (!allDone) {
                continue;
            }
            int changed = jdbc.sql("""
                            UPDATE program_enrolment SET status = 'COMPLETED', completed_at = :now
                            WHERE id = :id AND status = 'ACTIVE'""")
                    .param("now", Timestamps.now()).param("id", ((Number) e.get("id")).longValue()).update();
            if (changed == 1) {
                jdbc.sql(dialect.insertIgnoringDuplicates("""
                                INSERT INTO certificate (child_id, program_id, issued_at, verification_code)
                                VALUES (:c, :p, :now, :code)"""))
                        .param("c", childId).param("p", programId).param("now", Timestamps.now())
                        .param("code", verificationCode()).update();
                audit.record(null, "SYSTEM", "PROGRAM_COMPLETED", "child", childId, Map.of("programId", programId));
                List<BadgeView> badges = award(childId, "criteria = 'PROGRAM_COMPLETED' AND program_id = :p",
                        Map.of("p", programId), null);
                return new ProgramOutcome(true, (String) e.get("title"), badges);
            }
        }
        return new ProgramOutcome(false, null, List.of());
    }

    /** Every active badge, earned or not yet, so the profile can show goals as well as achievements. */
    public List<BadgeView> badgesOf(long childId) {
        return jdbc.sql("""
                        SELECT b.id, b.code, b.title, b.description, b.icon, cb.awarded_at
                        FROM badge b
                        LEFT JOIN child_badge cb ON cb.badge_id = b.id AND cb.child_id = :c
                        LEFT JOIN course co ON co.id = b.course_id
                        WHERE b.active AND (co.id IS NULL OR co.status = 'PUBLISHED')
                        ORDER BY cb.awarded_at IS NULL, cb.awarded_at DESC, co.sort_order, b.id""")
                .param("c", childId)
                .query((rs, n) -> {
                    LocalDateTime at = rs.getObject("awarded_at", LocalDateTime.class);
                    return new BadgeView(rs.getLong("id"), rs.getString("code"), rs.getString("title"),
                            rs.getString("description"), rs.getString("icon"), at != null,
                            at == null ? null : at.toInstant(java.time.ZoneOffset.UTC));
                })
                .list();
    }

    public List<CertificateView> certificatesOf(long childId) {
        return jdbc.sql("""
                        SELECT c.id, c.program_id, p.title, c.verification_code, c.issued_at
                        FROM certificate c JOIN program p ON p.id = c.program_id
                        WHERE c.child_id = :c ORDER BY c.issued_at""")
                .param("c", childId)
                .query((rs, n) -> new CertificateView(rs.getLong(1), rs.getLong(2), rs.getString(3), rs.getString(4),
                        rs.getObject(5, LocalDateTime.class).toInstant(java.time.ZoneOffset.UTC)))
                .list();
    }

    private List<BadgeView> award(long childId, String where, Map<String, ?> params, Long attemptId) {
        List<BadgeView> earned = new ArrayList<>();
        List<Map<String, Object>> badges = jdbc.sql(
                        "SELECT id, code, title, description, icon FROM badge WHERE active AND " + where)
                .params(params).query(Rows.MAP).list();
        for (Map<String, Object> b : badges) {
            long badgeId = ((Number) b.get("id")).longValue();
            int inserted = jdbc.sql(dialect.insertIgnoringDuplicates("""
                            INSERT INTO child_badge (child_id, badge_id, awarded_at, source_attempt_id)
                            VALUES (:c, :b, :now, :attempt)"""))
                    .param("c", childId).param("b", badgeId).param("now", Timestamps.now()).param("attempt", attemptId)
                    .update();
            if (inserted == 1) {
                earned.add(new BadgeView(badgeId, (String) b.get("code"), (String) b.get("title"),
                        (String) b.get("description"), (String) b.get("icon"), true, Instant.now()));
            }
        }
        return earned;
    }

    private static String verificationCode() {
        StringBuilder sb = new StringBuilder(16);
        for (int i = 0; i < 16; i++) {
            sb.append(CODE_ALPHABET.charAt(RANDOM.nextInt(CODE_ALPHABET.length())));
        }
        return sb.toString();
    }
}
