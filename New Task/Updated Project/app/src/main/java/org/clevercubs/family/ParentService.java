package org.clevercubs.family;

import java.time.Instant;
import java.time.LocalDateTime;
import java.time.ZoneOffset;
import java.util.ArrayList;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;
import java.util.Optional;

import org.clevercubs.audit.AuditLog;
import org.clevercubs.child.AgeGroups;
import org.clevercubs.child.AgeGroups.AgeGroup;
import org.clevercubs.child.ChildService;
import org.clevercubs.child.ChildService.ChildRow;
import org.clevercubs.child.ChildService.ChildView;
import org.clevercubs.learning.ProgressRules;
import org.clevercubs.learning.ProgressService;
import org.clevercubs.learning.ProgressService.CourseProgress;
import org.clevercubs.platform.security.Role;
import org.clevercubs.platform.web.ApiException;
import org.clevercubs.reward.RewardService;
import org.clevercubs.reward.RewardService.BadgeView;
import org.clevercubs.reward.RewardService.CertificateView;
import org.springframework.jdbc.core.simple.JdbcClient;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

/**
 * The parent area (requirement sections 7, 10, 12, 16): the family dashboard, a child's full progress, the
 * year summary and the next-year decision, and the parent's rights over their data (export and delete, D67).
 * Every method is scoped to the signed-in parent's own children.
 */
@Service
public class ParentService {

    public record ChildCard(ChildView child, String programTitle, int overallPercent, int coursesCompleted,
            int coursesTotal, int badgesEarned, int lockedQuizzes, Instant lastActive) {
    }

    public record Overview(String parentName, List<ChildCard> children, int pendingRequests) {
    }

    public record AttemptRow(int attemptNumber, Integer scorePercent, Boolean passed, String status,
            Instant startedAt, Instant submittedAt) {
    }

    public record CourseReport(CourseProgress progress, List<AttemptRow> attempts) {
    }

    public record ChildReport(ChildView child, String programTitle, String programStatus, int overallPercent,
            List<CourseReport> courses, List<BadgeView> badges, List<CertificateView> certificates) {
    }

    public record NextProgram(long id, String title, String description, List<String> courses) {
    }

    public record YearSummary(ChildView child, String programTitle, int yearNumber, String status,
            Instant startedAt, Instant completedAt, int overallPercent, int coursesCompleted, int coursesTotal,
            int quizzesPassed, int quizzesTotal, Integer averageBestScore, List<CourseReport> courses,
            List<BadgeView> badgesEarned, List<CertificateView> certificates, List<String> needsAttention,
            NextProgram nextProgram, String nextDecision) {
    }

    public record Account(String email, String fullName, String mobile, String city, Instant createdAt) {
    }

    private final JdbcClient jdbc;
    private final ChildService children;
    private final ProgressService progress;
    private final RewardService rewards;
    private final RequestService requests;
    private final AgeGroups ageGroups;
    private final AuditLog audit;

    public ParentService(JdbcClient jdbc, ChildService children, ProgressService progress, RewardService rewards,
            RequestService requests, AgeGroups ageGroups, AuditLog audit) {
        this.jdbc = jdbc;
        this.children = children;
        this.progress = progress;
        this.rewards = rewards;
        this.requests = requests;
        this.ageGroups = ageGroups;
        this.audit = audit;
    }

    public Overview overview(long accountId) {
        String name = jdbc.sql("SELECT full_name FROM parent WHERE account_id = :a").param("a", accountId)
                .query(String.class).optional().orElseThrow(() -> ApiException.notFound("Parent"));
        List<ChildCard> cards = new ArrayList<>();
        for (ChildRow c : children.forAccount(accountId)) {
            Map<Long, CourseProgress> all = progress.forChild(c.id());
            Program program = program(c.id());
            List<CourseProgress> courses = coursesOf(program, all);
            int locked = (int) courses.stream().filter(p -> p.quiz() != null && p.quiz().locked()).count();
            int badges = jdbc.sql("SELECT COUNT(*) FROM child_badge WHERE child_id = :c").param("c", c.id())
                    .query(Integer.class).single();
            Instant last = jdbc.sql("SELECT MAX(first_viewed_at) FROM lesson_item_view WHERE child_id = :c")
                    .param("c", c.id()).query(LocalDateTime.class).optional()
                    .map(t -> t.toInstant(ZoneOffset.UTC)).orElse(null);
            cards.add(new ChildCard(children.view(c), program == null ? null : program.title(),
                    average(courses), (int) courses.stream().filter(CourseProgress::completed).count(),
                    courses.size(), badges, locked, last));
        }
        int pending = requests.forParent(accountId, true).size();
        return new Overview(name, cards, pending);
    }

    public ChildReport report(long accountId, long childId) {
        return reportOf(children.requireOwned(accountId, childId));
    }

    /** The full progress report of a child; also used by the Super Admin's progress view. */
    public ChildReport reportOf(ChildRow c) {
        Map<Long, CourseProgress> all = progress.forChild(c.id());
        Program program = program(c.id());
        List<CourseReport> courses = coursesOf(program, all).stream()
                .map(p -> new CourseReport(p, attempts(c.id(), p))).toList();
        return new ChildReport(children.view(c), program == null ? null : program.title(),
                program == null ? null : program.status(), average(coursesOf(program, all)), courses,
                rewards.badgesOf(c.id()).stream().filter(BadgeView::earned).toList(),
                rewards.certificatesOf(c.id()));
    }

    public YearSummary yearSummary(long accountId, long childId) {
        ChildRow c = children.requireOwned(accountId, childId);
        Program program = program(c.id());
        if (program == null) {
            throw ApiException.notFound("Program");
        }
        Map<Long, CourseProgress> all = progress.forChild(c.id());
        List<CourseProgress> courses = coursesOf(program, all);
        List<CourseReport> reports = courses.stream().map(p -> new CourseReport(p, attempts(c.id(), p))).toList();
        List<CourseProgress> withQuiz = courses.stream().filter(p -> p.quiz() != null).toList();
        List<Integer> bests = withQuiz.stream().map(p -> p.quiz().bestScore()).filter(s -> s != null).toList();
        Integer averageBest = bests.isEmpty() ? null
                : (int) Math.round(bests.stream().mapToInt(Integer::intValue).average().orElse(0));

        // Plain facts only, never a judgement about the child (requirement section 16).
        List<String> attention = new ArrayList<>();
        for (CourseProgress p : courses) {
            if (p.quiz() != null && p.quiz().locked()) {
                attention.add(p.title() + ": the quiz is waiting for more tries from you.");
            } else if (p.quiz() != null && p.quiz().unlocked() && !p.quiz().passed()) {
                attention.add(p.title() + ": the lessons are done and the quiz is ready.");
            } else if (!p.started()) {
                attention.add(p.title() + ": not started yet.");
            } else if (!p.completed()) {
                attention.add(p.title() + ": " + p.lessonsDone() + " of " + p.lessonsTotal() + " lessons done.");
            }
        }
        return new YearSummary(children.view(c), program.title(), program.yearNumber(), program.status(),
                program.startedAt(), program.completedAt(), average(courses),
                (int) courses.stream().filter(CourseProgress::completed).count(), courses.size(),
                (int) withQuiz.stream().filter(p -> p.quiz().passed()).count(), withQuiz.size(), averageBest, reports,
                rewards.badgesOf(c.id()).stream().filter(BadgeView::earned).toList(), rewards.certificatesOf(c.id()),
                attention, nextProgram(c, program, all).orElse(null), program.nextDecision());
    }

    /**
     * The parent's decision about the next year (section 16): recorded on the completed enrolment. Continuing
     * enrols the child in the next program when one with new content is published; otherwise the decision is
     * kept and the page says the program is being prepared (INF-01).
     */
    @Transactional
    public YearSummary decideNextYear(long accountId, long childId, String decision) {
        if (!"CONTINUE".equals(decision) && !"NOT_NOW".equals(decision)) {
            throw ApiException.badRequest("invalid-input", "Choose to continue, or not now.");
        }
        ChildRow c = children.requireOwned(accountId, childId);
        Program program = program(c.id());
        if (program == null || !"COMPLETED".equals(program.status())) {
            throw ApiException.rule("program-not-complete", "The decision opens when this year is complete.");
        }
        jdbc.sql("UPDATE program_enrolment SET next_decision = :d, decided_at = :now WHERE id = :id")
                .param("d", decision).param("now", Instant.now()).param("id", program.enrolmentId()).update();
        if ("CONTINUE".equals(decision)) {
            nextProgram(c, program, progress.forChild(c.id())).ifPresent(next -> jdbc.sql("""
                            INSERT IGNORE INTO program_enrolment (child_id, program_id, status, started_at)
                            VALUES (:c, :p, 'ACTIVE', :now)""")
                    .param("c", c.id()).param("p", next.id()).param("now", Instant.now()).update());
        }
        audit.record(accountId, Role.PARENT.name(), "NEXT_YEAR_DECIDED", "child", childId,
                Map.of("decision", decision));
        return yearSummary(accountId, childId);
    }

    /** Everything stored about one child, as JSON the parent can keep (D67). */
    public Map<String, Object> export(long accountId, long childId) {
        ChildRow c = children.requireOwned(accountId, childId);
        Map<String, Object> out = new LinkedHashMap<>();
        out.put("exportedAt", Instant.now().toString());
        out.put("child", children.view(c));
        out.put("report", reportOf(c));
        out.put("lessonCompletions", jdbc.sql("""
                        SELECT l.title AS lesson, co.title AS course, lc.completed_at
                        FROM lesson_completion lc JOIN lesson l ON l.id = lc.lesson_id JOIN course co ON co.id = l.course_id
                        WHERE lc.child_id = :c ORDER BY lc.completed_at""")
                .param("c", c.id()).query().listOfRows());
        out.put("requests", requests.forChild(c.id()));
        audit.record(accountId, Role.PARENT.name(), "CHILD_DATA_EXPORTED", "child", childId, Map.of());
        return out;
    }

    @Transactional
    public void deleteChild(long accountId, long childId) {
        children.requireOwned(accountId, childId);
        jdbc.sql("DELETE FROM child WHERE id = :id").param("id", childId).update();
        audit.record(accountId, Role.PARENT.name(), "CHILD_DELETED", "child", childId, Map.of());
    }

    public Account account(long accountId) {
        return jdbc.sql("""
                        SELECT a.email, p.full_name, p.mobile, p.city, a.created_at
                        FROM user_account a JOIN parent p ON p.account_id = a.id WHERE a.id = :a""")
                .param("a", accountId)
                .query((rs, n) -> new Account(rs.getString(1), rs.getString(2), rs.getString(3), rs.getString(4),
                        rs.getObject(5, LocalDateTime.class).toInstant(ZoneOffset.UTC)))
                .optional().orElseThrow(() -> ApiException.notFound("Account"));
    }

    @Transactional
    public Account updateAccount(long accountId, String fullName, String mobile, String city) {
        jdbc.sql("""
                        UPDATE parent SET full_name = :name, mobile = :mobile, city = :city, updated_at = :now
                        WHERE account_id = :a""")
                .param("name", fullName.trim()).param("mobile", blankToNull(mobile)).param("city", blankToNull(city))
                .param("now", Instant.now()).param("a", accountId).update();
        return account(accountId);
    }

    /** Deletes the parent's account and, through the foreign keys, their children and all their data. */
    @Transactional
    public void deleteAccount(long accountId) {
        jdbc.sql("DELETE FROM user_account WHERE id = :a AND role = 'PARENT'").param("a", accountId).update();
        audit.record(accountId, Role.PARENT.name(), "ACCOUNT_DELETED", "user_account", accountId, Map.of());
    }

    // --- helpers -------------------------------------------------------------------------------------------

    private record Program(long enrolmentId, long id, String title, int yearNumber, long ageGroupId,
            String status, Instant startedAt, Instant completedAt, String nextDecision) {
    }

    /** The child's current program: the active one, else the most recently completed one. */
    private Program program(long childId) {
        return jdbc.sql("""
                        SELECT e.id, p.id, p.title, p.year_number, p.age_group_id, e.status, e.started_at,
                               e.completed_at, e.next_decision
                        FROM program_enrolment e JOIN program p ON p.id = e.program_id
                        WHERE e.child_id = :c
                        ORDER BY e.status = 'ACTIVE' DESC, e.started_at DESC LIMIT 1""")
                .param("c", childId)
                .query((rs, n) -> {
                    LocalDateTime done = rs.getObject(8, LocalDateTime.class);
                    return new Program(rs.getLong(1), rs.getLong(2), rs.getString(3), rs.getInt(4), rs.getLong(5),
                            rs.getString(6), rs.getObject(7, LocalDateTime.class).toInstant(ZoneOffset.UTC),
                            done == null ? null : done.toInstant(ZoneOffset.UTC), rs.getString(9));
                })
                .optional().orElse(null);
    }

    private List<CourseProgress> coursesOf(Program program, Map<Long, CourseProgress> all) {
        if (program == null) {
            return new ArrayList<>(all.values());
        }
        List<CourseProgress> list = new ArrayList<>();
        for (Long id : progress.programCourseIds(program.id())) {
            if (all.containsKey(id)) {
                list.add(all.get(id));
            }
        }
        return list;
    }

    /**
     * The next program: the same age group's next year, else the next age group's first year, provided it
     * contains a course the child has not completed. Without new content there is no next program yet.
     */
    private Optional<NextProgram> nextProgram(ChildRow c, Program current, Map<Long, CourseProgress> all) {
        List<AgeGroup> groups = ageGroups.all();
        List<long[]> candidates = new ArrayList<>(); // {ageGroupId, year}
        candidates.add(new long[] {current.ageGroupId(), current.yearNumber() + 1});
        for (int i = 0; i < groups.size() - 1; i++) {
            if (groups.get(i).id() == current.ageGroupId()) {
                candidates.add(new long[] {groups.get(i + 1).id(), 1});
            }
        }
        for (long[] cand : candidates) {
            Optional<Map<String, Object>> p = jdbc.sql("""
                            SELECT id, title, description FROM program
                            WHERE age_group_id = :g AND year_number = :y AND status = 'PUBLISHED'""")
                    .param("g", cand[0]).param("y", cand[1]).query().listOfRows().stream().findFirst();
            if (p.isEmpty()) {
                continue;
            }
            long id = ((Number) p.get().get("id")).longValue();
            List<Long> ids = progress.programCourseIds(id);
            boolean hasNew = ids.stream().anyMatch(cid -> !all.containsKey(cid) || !all.get(cid).completed());
            if (hasNew) {
                List<String> titles = ids.stream().filter(all::containsKey).map(cid -> all.get(cid).title()).toList();
                return Optional.of(new NextProgram(id, (String) p.get().get("title"),
                        (String) p.get().get("description"), titles));
            }
        }
        return Optional.empty();
    }

    private List<AttemptRow> attempts(long childId, CourseProgress p) {
        if (p.quiz() == null) {
            return List.of();
        }
        return jdbc.sql("""
                        SELECT attempt_number, score_percent, passed, status, started_at, submitted_at
                        FROM quiz_attempt WHERE child_id = :c AND quiz_id = :q ORDER BY attempt_number""")
                .param("c", childId).param("q", p.quiz().quizId())
                .query((rs, n) -> {
                    LocalDateTime submitted = rs.getObject(6, LocalDateTime.class);
                    return new AttemptRow(rs.getInt(1), rs.getObject(2, Integer.class),
                            rs.getObject(3, Boolean.class), rs.getString(4),
                            rs.getObject(5, LocalDateTime.class).toInstant(ZoneOffset.UTC),
                            submitted == null ? null : submitted.toInstant(ZoneOffset.UTC));
                })
                .list();
    }

    private static int average(List<CourseProgress> courses) {
        return ProgressRules.average(courses.stream().mapToInt(CourseProgress::percent).toArray());
    }

    private static String blankToNull(String s) {
        return s == null || s.isBlank() ? null : s.trim();
    }
}
