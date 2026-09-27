package org.clevercubs.admin;

import java.security.SecureRandom;
import java.util.ArrayList;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;
import java.util.regex.Pattern;

import org.clevercubs.audit.AuditLog;
import org.clevercubs.child.AgeGroups;
import org.clevercubs.platform.db.Rows;
import org.clevercubs.platform.db.SqlDialect;
import org.clevercubs.platform.db.Timestamps;
import org.clevercubs.platform.security.AccountSessions;
import org.clevercubs.platform.security.PasswordPolicy;
import org.clevercubs.platform.security.Role;
import org.clevercubs.platform.settings.Settings;
import org.clevercubs.platform.web.ApiException;
import org.springframework.jdbc.core.simple.JdbcClient;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

/**
 * The Super Admin's operations (requirement section 19): users, children, content, quizzes, programs, age
 * groups, badges, wording, feedback, settings, reports and the audit trail. Every change is written to the
 * append-only audit trail with the admin's account id (DD-14). Results are plain maps shaped for the admin
 * pages; no password hash ever leaves this class.
 */
@Service
public class AdminService {

    private static final String ADMIN = Role.SUPER_ADMIN.name();
    private static final SecureRandom RANDOM = new SecureRandom();

    /** Allowed range for every admin-editable setting, so a typo cannot break a rule. */
    private static final Map<String, int[]> SETTING_RANGES = Map.of(
            Settings.LESSON_WEIGHT, new int[] {10, 90},
            Settings.MAX_ATTEMPTS, new int[] {1, 10},
            Settings.GRANT_ATTEMPTS, new int[] {1, 10},
            Settings.DEFAULT_PASS_MARK, new int[] {1, 100},
            Settings.REWARD_THRESHOLD, new int[] {1, 100},
            Settings.CHILD_IDLE_MINUTES, new int[] {5, 240},
            Settings.PARENT_REAUTH_MINUTES, new int[] {1, 120});
    private static final Pattern VERSION = Pattern.compile("^[A-Za-z0-9._-]{1,20}$");

    private final JdbcClient jdbc;
    private final AuditLog audit;
    private final Settings settings;
    private final PasswordEncoder passwords;
    private final PasswordPolicy policy;
    private final AgeGroups ageGroups;
    private final SqlDialect dialect;
    private final AccountSessions sessions;

    public AdminService(JdbcClient jdbc, AuditLog audit, Settings settings, PasswordEncoder passwords,
            PasswordPolicy policy, AgeGroups ageGroups, SqlDialect dialect, AccountSessions sessions) {
        this.jdbc = jdbc;
        this.audit = audit;
        this.settings = settings;
        this.passwords = passwords;
        this.policy = policy;
        this.ageGroups = ageGroups;
        this.dialect = dialect;
        this.sessions = sessions;
    }

    // --- overview and reports -------------------------------------------------------------------------

    public Map<String, Object> overview() {
        Map<String, Object> counts = new LinkedHashMap<>();
        counts.put("parents", count("SELECT COUNT(*) FROM user_account WHERE role = 'PARENT'"));
        counts.put("children", count("SELECT COUNT(*) FROM child"));
        counts.put("courses", count("SELECT COUNT(*) FROM course WHERE status = 'PUBLISHED'"));
        counts.put("lessons", count("SELECT COUNT(*) FROM lesson WHERE status = 'PUBLISHED'"));
        counts.put("quizAttempts", count("SELECT COUNT(*) FROM quiz_attempt WHERE status = 'SUBMITTED'"));
        counts.put("badgesAwarded", count("SELECT COUNT(*) FROM child_badge"));
        counts.put("programsCompleted", count("SELECT COUNT(*) FROM program_enrolment WHERE status = 'COMPLETED'"));
        counts.put("newFeedback", count("SELECT COUNT(*) FROM feedback WHERE status = 'NEW'"));
        counts.put("pendingRequests", count("SELECT COUNT(*) FROM parent_request WHERE status = 'PENDING'"));
        counts.put("lockedAccounts", jdbc.sql(
                        "SELECT COUNT(*) FROM user_account WHERE status <> 'ACTIVE' OR locked_until > :now")
                .param("now", Timestamps.now()).query(Integer.class).single());
        return Map.of("counts", counts, "recentAudit", audit(null, 10, 0));
    }

    /** Per-course learning statistics, without naming any child. */
    public List<Map<String, Object>> courseReport() {
        return jdbc.sql("""
                        SELECT c.id, c.title, c.icon, c.kind,
                          (SELECT COUNT(DISTINCT v.child_id) FROM lesson_item_view v JOIN lesson_item i ON i.id = v.lesson_item_id
                             JOIN lesson l ON l.id = i.lesson_id WHERE l.course_id = c.id) AS children_started,
                          (SELECT COUNT(*) FROM quiz_attempt a JOIN quiz q ON q.id = a.quiz_id
                             WHERE q.course_id = c.id AND a.status = 'SUBMITTED') AS attempts,
                          (SELECT COUNT(DISTINCT a.child_id) FROM quiz_attempt a JOIN quiz q ON q.id = a.quiz_id
                             WHERE q.course_id = c.id AND a.passed) AS children_passed,
                          (SELECT ROUND(AVG(a.score_percent)) FROM quiz_attempt a JOIN quiz q ON q.id = a.quiz_id
                             WHERE q.course_id = c.id AND a.status = 'SUBMITTED') AS average_score,
                          (SELECT COUNT(*) FROM child_badge cb JOIN badge b ON b.id = cb.badge_id
                             WHERE b.course_id = c.id) AS badges
                        FROM course c ORDER BY c.sort_order""")
                .query(Rows.MAP).list();
    }

    // --- accounts ----------------------------------------------------------------------------------------

    public List<Map<String, Object>> accounts(String search, int size, int page) {
        String q = search == null ? "" : search.trim();
        return jdbc.sql("""
                        SELECT a.id, a.email, a.role, a.status, a.locked_until, a.failed_logins, a.must_change_password,
                               a.last_login_at, a.created_at, p.full_name,
                               (SELECT COUNT(*) FROM child ch WHERE ch.parent_id = p.id) AS children
                        FROM user_account a LEFT JOIN parent p ON p.account_id = a.id
                        WHERE (:q = '' OR LOWER(a.email) LIKE LOWER(CONCAT('%', :q, '%'))
                               OR LOWER(p.full_name) LIKE LOWER(CONCAT('%', :q, '%')))
                        ORDER BY a.created_at DESC LIMIT :size OFFSET :offset""")
                .param("q", q).param("size", size).param("offset", page * size)
                .query(Rows.MAP).list();
    }

    @Transactional
    public void changeAccountStatus(long adminId, long accountId, String action) {
        if (adminId == accountId) {
            throw ApiException.rule("own-account", "You cannot change your own account here.");
        }
        String sql = switch (action == null ? "" : action) {
            case "DISABLE" -> "UPDATE user_account SET status = 'DISABLED', updated_at = :now WHERE id = :id";
            case "ENABLE" -> "UPDATE user_account SET status = 'ACTIVE', updated_at = :now WHERE id = :id";
            case "UNLOCK" -> """
                    UPDATE user_account SET status = CASE WHEN status = 'LOCKED' THEN 'ACTIVE' ELSE status END,
                           locked_until = NULL, failed_logins = 0, updated_at = :now WHERE id = :id""";
            default -> throw ApiException.badRequest("invalid-input", "Unknown action.");
        };
        if (jdbc.sql(sql).param("now", Timestamps.now()).param("id", accountId).update() == 0) {
            throw ApiException.notFound("Account");
        }
        if ("DISABLE".equals(action)) {
            // SEC-R02: the status is checked only at sign-in, so end the sessions the account already holds.
            sessions.endAll(accountId);
        }
        audit.record(adminId, ADMIN, "ACCOUNT_" + action, "user_account", accountId, Map.of());
    }

    /**
     * Admin-assisted password reset while no email provider exists (INF-04): a random temporary password,
     * shown once to the admin, which the owner must replace at the next sign-in.
     */
    @Transactional
    public String issueTemporaryPassword(long adminId, long accountId) {
        if (adminId == accountId) {
            throw ApiException.rule("own-account", "Use the change-password form for your own account.");
        }
        String temporary = newTemporaryPassword();
        int changed = jdbc.sql("""
                        UPDATE user_account SET password_hash = :hash, must_change_password = TRUE,
                               password_changed_at = :now, failed_logins = 0, locked_until = NULL, updated_at = :now
                        WHERE id = :id""")
                .param("hash", passwords.encode(temporary)).param("now", Timestamps.now()).param("id", accountId)
                .update();
        if (changed == 0) {
            throw ApiException.notFound("Account");
        }
        audit.record(adminId, ADMIN, "ACCOUNT_TEMPORARY_PASSWORD", "user_account", accountId, Map.of());
        return temporary;
    }

    /**
     * D79: another Super Admin, created by an existing one. The account starts with a random temporary password,
     * returned once to the creating admin, and must choose its own at the first sign-in
     * ({@code must_change_password}); the audit row names the role, never the address or the password.
     */
    @Transactional
    public Map<String, Object> createSuperAdmin(long adminId, String email) {
        String address = email.trim();
        int taken = jdbc.sql("SELECT COUNT(*) FROM user_account WHERE email = " + dialect.caseInsensitive("e"))
                .param("e", address).query(Integer.class).single();
        if (taken > 0) {
            throw ApiException.field("email-taken", "email", "An account already uses this address.");
        }
        String temporary = newTemporaryPassword();
        jdbc.sql("""
                        INSERT INTO user_account (email, password_hash, role, status, failed_logins, locked_until,
                                                  must_change_password, password_changed_at, created_at, updated_at)
                        VALUES (:e, :hash, 'SUPER_ADMIN', 'ACTIVE', 0, NULL, TRUE, :now, :now, :now)""")
                .param("e", address).param("hash", passwords.encode(temporary)).param("now", Timestamps.now())
                .update();
        long accountId = jdbc.sql("SELECT id FROM user_account WHERE email = " + dialect.caseInsensitive("e"))
                .param("e", address).query(Long.class).single();
        audit.record(adminId, ADMIN, "ACCOUNT_CREATED", "user_account", accountId, Map.of("role", ADMIN));
        return Map.of("accountId", accountId, "email", address, "role", ADMIN, "temporaryPassword", temporary);
    }

    /** 16 random characters in four groups, from an alphabet without look-alikes, that the policy accepts. */
    private String newTemporaryPassword() {
        String alphabet = "ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz23456789";
        String temporary;
        do {
            StringBuilder sb = new StringBuilder();
            for (int i = 0; i < 16; i++) {
                sb.append(alphabet.charAt(RANDOM.nextInt(alphabet.length())));
                if (i == 3 || i == 7 || i == 11) {
                    sb.append('-');
                }
            }
            temporary = sb.toString();
        } while (policy.problem(temporary, null).isPresent());
        return temporary;
    }

    public List<Map<String, Object>> children(String search, int size, int page) {
        String q = search == null ? "" : search.trim();
        List<Map<String, Object>> rows = jdbc.sql("""
                        SELECT ch.id, ch.display_name, ch.username, ch.date_of_birth, ch.avatar_code, ch.created_at,
                               p.full_name AS parent_name, p.account_id AS parent_account_id,
                               (SELECT COUNT(*) FROM child_badge cb WHERE cb.child_id = ch.id) AS badges,
                               (SELECT COUNT(*) FROM lesson_completion lc WHERE lc.child_id = ch.id) AS lessons_done,
                               (SELECT MAX(v.first_viewed_at) FROM lesson_item_view v WHERE v.child_id = ch.id) AS last_active
                        FROM child ch JOIN parent p ON p.id = ch.parent_id
                        WHERE (:q = '' OR LOWER(ch.username) LIKE LOWER(CONCAT('%', :q, '%'))
                               OR LOWER(ch.display_name) LIKE LOWER(CONCAT('%', :q, '%')))
                        ORDER BY ch.created_at DESC LIMIT :size OFFSET :offset""")
                .param("q", q).param("size", size).param("offset", page * size)
                .query(Rows.MAP).list();
        List<Map<String, Object>> out = new ArrayList<>();
        for (Map<String, Object> r : rows) {
            Map<String, Object> m = new LinkedHashMap<>(r);
            // Data minimisation: the admin list shows the age group, not the date of birth.
            java.time.LocalDate dob = r.get("date_of_birth") instanceof java.sql.Date d ? d.toLocalDate()
                    : (java.time.LocalDate) r.get("date_of_birth");
            m.remove("date_of_birth");
            m.put("age_group", ageGroups.forChild(dob, java.time.LocalDate.now(java.time.ZoneOffset.UTC)).name());
            out.add(m);
        }
        return out;
    }

    // --- content -----------------------------------------------------------------------------------------

    public List<Map<String, Object>> courses() {
        return jdbc.sql("""
                        SELECT c.id, c.slug, c.title, c.description, c.icon, c.kind, c.status, c.sort_order,
                               (SELECT COUNT(*) FROM lesson l WHERE l.course_id = c.id) AS lessons,
                               (SELECT COUNT(*) FROM lesson_item i JOIN lesson l ON l.id = i.lesson_id
                                 WHERE l.course_id = c.id) AS items,
                               q.id AS quiz_id, q.pass_mark_percent, q.status AS quiz_status
                        FROM course c LEFT JOIN quiz q ON q.course_id = c.id ORDER BY c.sort_order""")
                .query(Rows.MAP).list();
    }

    public Map<String, Object> course(long courseId) {
        Map<String, Object> course = jdbc.sql("SELECT id, slug, title, description, icon, kind, status, sort_order FROM course WHERE id = :id")
                .param("id", courseId).query(Rows.MAP).list().stream().findFirst()
                .orElseThrow(() -> ApiException.notFound("Course"));
        List<Map<String, Object>> lessons = jdbc.sql(
                        "SELECT id, title, sort_order, status FROM lesson WHERE course_id = :c ORDER BY sort_order")
                .param("c", courseId).query(Rows.MAP).list();
        List<Map<String, Object>> withItems = new ArrayList<>();
        for (Map<String, Object> l : lessons) {
            Map<String, Object> m = new LinkedHashMap<>(l);
            m.put("items", jdbc.sql("""
                            SELECT id, sort_order, label, word, emoji, description, alt_text, image_path, audio_path,
                                   video_path, status
                            FROM lesson_item WHERE lesson_id = :l ORDER BY sort_order""")
                    .param("l", l.get("id")).query(Rows.MAP).list());
            withItems.add(m);
        }
        Map<String, Object> out = new LinkedHashMap<>(course);
        out.put("lessons", withItems);
        out.put("quizId", jdbc.sql("SELECT id FROM quiz WHERE course_id = :c").param("c", courseId)
                .query(Long.class).optional().orElse(null));
        return out;
    }

    @Transactional
    public void updateCourse(long adminId, long id, String title, String description, String icon, String status,
            Integer sortOrder) {
        checkStatus(status);
        int changed = jdbc.sql("""
                        UPDATE course SET title = COALESCE(:title, title), description = COALESCE(:description, description),
                               icon = COALESCE(:icon, icon), status = COALESCE(:status, status),
                               sort_order = COALESCE(:sort, sort_order), updated_at = :now
                        WHERE id = :id""")
                .param("title", trimToNull(title, 60)).param("description", trimToNull(description, 500))
                .param("icon", trimToNull(icon, 16)).param("status", status).param("sort", sortOrder)
                .param("now", Timestamps.now()).param("id", id).update();
        found(changed, "Course");
        audit.record(adminId, ADMIN, "COURSE_UPDATED", "course", id, Map.of());
    }

    @Transactional
    public void updateLesson(long adminId, long id, String title, String status) {
        checkStatus(status);
        found(jdbc.sql("""
                        UPDATE lesson SET title = COALESCE(:title, title), status = COALESCE(:status, status),
                               updated_at = :now WHERE id = :id""")
                .param("title", trimToNull(title, 80)).param("status", status).param("now", Timestamps.now())
                .param("id", id).update(), "Lesson");
        audit.record(adminId, ADMIN, "LESSON_UPDATED", "lesson", id, Map.of());
    }

    @Transactional
    public void updateItem(long adminId, long id, String word, String description, String altText) {
        found(jdbc.sql("""
                        UPDATE lesson_item SET word = COALESCE(:word, word), description = COALESCE(:description, description),
                               alt_text = COALESCE(:alt, alt_text) WHERE id = :id""")
                .param("word", trimToNull(word, 80)).param("description", trimToNull(description, 300))
                .param("alt", trimToNull(altText, 150)).param("id", id).update(), "Card");
        audit.record(adminId, ADMIN, "LESSON_ITEM_UPDATED", "lesson_item", id, Map.of());
    }

    public Map<String, Object> quiz(long quizId) {
        Map<String, Object> quiz = jdbc.sql("""
                        SELECT q.id, q.title, q.pass_mark_percent, q.required, q.status, c.title AS course_title
                        FROM quiz q JOIN course c ON c.id = q.course_id WHERE q.id = :id""")
                .param("id", quizId).query(Rows.MAP).list().stream().findFirst()
                .orElseThrow(() -> ApiException.notFound("Quiz"));
        List<Map<String, Object>> questions = jdbc.sql(
                        "SELECT id, pool, sort_order, prompt FROM quiz_question WHERE quiz_id = :q ORDER BY pool, sort_order")
                .param("q", quizId).query(Rows.MAP).list();
        List<Map<String, Object>> full = new ArrayList<>();
        for (Map<String, Object> q : questions) {
            Map<String, Object> m = new LinkedHashMap<>(q);
            m.put("options", jdbc.sql(
                            "SELECT id, sort_order, label, is_correct FROM quiz_option WHERE question_id = :q ORDER BY sort_order")
                    .param("q", q.get("id")).query(Rows.MAP).list());
            full.add(m);
        }
        Map<String, Object> out = new LinkedHashMap<>(quiz);
        out.put("questions", full);
        return out;
    }

    @Transactional
    public void updateQuiz(long adminId, long id, Integer passMark, Boolean required, String status) {
        checkStatus(status);
        if (passMark != null && (passMark < 1 || passMark > 100)) {
            throw ApiException.field("invalid-input", "passMarkPercent", "The pass mark is between 1 and 100.");
        }
        found(jdbc.sql("""
                        UPDATE quiz SET pass_mark_percent = COALESCE(:pass, pass_mark_percent),
                               required = COALESCE(:required, required), status = COALESCE(:status, status),
                               updated_at = :now WHERE id = :id""")
                .param("pass", passMark).param("required", required).param("status", status)
                .param("now", Timestamps.now()).param("id", id).update(), "Quiz");
        audit.record(adminId, ADMIN, "QUIZ_UPDATED", "quiz", id, passMark == null ? Map.of() : Map.of("passMark", passMark));
    }

    /** Edits a question's wording and options; exactly one option must be correct (docs/05 section 3.3). */
    @Transactional
    public void updateQuestion(long adminId, long questionId, String prompt, String pool,
            List<Map<String, Object>> options) {
        if (pool != null && !pool.equals("MAIN") && !pool.equals("RESERVE")) {
            throw ApiException.badRequest("invalid-input", "Unknown question pool.");
        }
        found(jdbc.sql("UPDATE quiz_question SET prompt = COALESCE(:p, prompt), pool = COALESCE(:pool, pool) WHERE id = :id")
                .param("p", trimToNull(prompt, 200)).param("pool", pool).param("id", questionId).update(), "Question");
        if (options != null && !options.isEmpty()) {
            long correct = options.stream().filter(o -> Boolean.TRUE.equals(o.get("correct"))).count();
            if (correct != 1) {
                throw ApiException.rule("one-correct-option", "Exactly one answer must be marked correct.");
            }
            for (Map<String, Object> o : options) {
                long optionId = ((Number) o.get("id")).longValue();
                found(jdbc.sql("""
                                UPDATE quiz_option SET label = COALESCE(:label, label), is_correct = :correct
                                WHERE id = :id AND question_id = :q""")
                        .param("label", trimToNull((String) o.get("label"), 80))
                        .param("correct", Boolean.TRUE.equals(o.get("correct")))
                        .param("id", optionId).param("q", questionId).update(), "Answer option");
            }
        }
        audit.record(adminId, ADMIN, "QUESTION_UPDATED", "quiz_question", questionId, Map.of());
    }

    public List<Map<String, Object>> programs() {
        List<Map<String, Object>> programs = jdbc.sql("""
                        SELECT p.id, p.title, p.description, p.year_number, p.status, g.name AS age_group
                        FROM program p JOIN age_group g ON g.id = p.age_group_id ORDER BY g.sort_order, p.year_number""")
                .query(Rows.MAP).list();
        List<Map<String, Object>> out = new ArrayList<>();
        for (Map<String, Object> p : programs) {
            Map<String, Object> m = new LinkedHashMap<>(p);
            m.put("courseIds", jdbc.sql("SELECT course_id FROM program_course WHERE program_id = :p ORDER BY sort_order")
                    .param("p", p.get("id")).query(Long.class).list());
            out.add(m);
        }
        return out;
    }

    @Transactional
    public void setProgramCourses(long adminId, long programId, List<Long> courseIds) {
        found(jdbc.sql("SELECT COUNT(*) FROM program WHERE id = :p").param("p", programId).query(Integer.class)
                .single(), "Program");
        jdbc.sql("DELETE FROM program_course WHERE program_id = :p").param("p", programId).update();
        int order = 1;
        for (Long courseId : courseIds) {
            jdbc.sql(dialect.insertIgnoringDuplicates(
                            "INSERT INTO program_course (program_id, course_id, sort_order) VALUES (:p, :c, :o)"))
                    .param("p", programId).param("c", courseId).param("o", order++).update();
        }
        audit.record(adminId, ADMIN, "PROGRAM_COURSES_SET", "program", programId, Map.of("courses", courseIds.size()));
    }

    public List<Map<String, Object>> ageGroups() {
        return jdbc.sql("SELECT id, code, name, min_age, max_age, ui_profile, sort_order FROM age_group ORDER BY sort_order")
                .query(Rows.MAP).list();
    }

    /** Edits a band; bands may not overlap, so every age still maps to exactly one group (docs/05 3.2). */
    @Transactional
    public void updateAgeGroup(long adminId, long id, String name, Integer minAge, Integer maxAge) {
        Map<String, Object> current = jdbc.sql("SELECT min_age, max_age FROM age_group WHERE id = :id")
                .param("id", id).query(Rows.MAP).list().stream().findFirst()
                .orElseThrow(() -> ApiException.notFound("Age group"));
        int min = minAge != null ? minAge : ((Number) current.get("min_age")).intValue();
        int max = maxAge != null ? maxAge : ((Number) current.get("max_age")).intValue();
        if (min < 0 || min > max || max > 18) {
            throw ApiException.rule("invalid-range", "The youngest age must be at most the oldest (0 to 18).");
        }
        int overlaps = jdbc.sql("SELECT COUNT(*) FROM age_group WHERE id <> :id AND min_age <= :max AND max_age >= :min")
                .param("id", id).param("min", min).param("max", max).query(Integer.class).single();
        if (overlaps > 0) {
            throw ApiException.rule("overlapping-bands", "Age groups may not overlap.");
        }
        jdbc.sql("UPDATE age_group SET name = COALESCE(:name, name), min_age = :min, max_age = :max WHERE id = :id")
                .param("name", trimToNull(name, 40)).param("min", min).param("max", max).param("id", id).update();
        audit.record(adminId, ADMIN, "AGE_GROUP_UPDATED", "age_group", id, Map.of("min", min, "max", max));
    }

    public List<Map<String, Object>> badges() {
        return jdbc.sql("""
                        SELECT b.id, b.code, b.title, b.description, b.icon, b.criteria, b.active, c.title AS course,
                               (SELECT COUNT(*) FROM child_badge cb WHERE cb.badge_id = b.id) AS awarded
                        FROM badge b LEFT JOIN course c ON c.id = b.course_id ORDER BY b.criteria, c.sort_order, b.id""")
                .query(Rows.MAP).list();
    }

    @Transactional
    public void updateBadge(long adminId, long id, String title, String description, String icon, Boolean active) {
        found(jdbc.sql("""
                        UPDATE badge SET title = COALESCE(:t, title), description = COALESCE(:d, description),
                               icon = COALESCE(:i, icon), active = COALESCE(:a, active) WHERE id = :id""")
                .param("t", trimToNull(title, 60)).param("d", trimToNull(description, 200))
                .param("i", trimToNull(icon, 16)).param("a", active).param("id", id).update(), "Badge");
        audit.record(adminId, ADMIN, "BADGE_UPDATED", "badge", id, Map.of());
    }

    public List<Map<String, Object>> messages() {
        return jdbc.sql("""
                        SELECT m.id, m.message_key, m.text, m.active, g.name AS age_group, m.age_group_id
                        FROM ui_message m LEFT JOIN age_group g ON g.id = m.age_group_id ORDER BY m.message_key, m.id""")
                .query(Rows.MAP).list();
    }

    @Transactional
    public void updateMessage(long adminId, long id, String text, Boolean active) {
        found(jdbc.sql("UPDATE ui_message SET text = COALESCE(:t, text), active = COALESCE(:a, active) WHERE id = :id")
                .param("t", trimToNull(text, 300)).param("a", active).param("id", id).update(), "Message");
        audit.record(adminId, ADMIN, "MESSAGE_UPDATED", "ui_message", id, Map.of());
    }

    @Transactional
    public void createMessage(long adminId, String key, Long ageGroupId, String text) {
        String k = trimToNull(key, 60);
        String t = trimToNull(text, 300);
        if (k == null || t == null) {
            throw ApiException.badRequest("invalid-input", "A key and a text are required.");
        }
        jdbc.sql("INSERT INTO ui_message (message_key, age_group_id, text, active) VALUES (:k, :g, :t, TRUE)")
                .param("k", k).param("g", ageGroupId).param("t", t).update();
        audit.record(adminId, ADMIN, "MESSAGE_CREATED", "ui_message", null, Map.of("key", k));
    }

    // --- settings and audit --------------------------------------------------------------------------------

    public Map<String, String> settings() {
        return settings.all();
    }

    public void updateSetting(long adminId, String key, String value) {
        String v = value == null ? "" : value.trim();
        int[] range = SETTING_RANGES.get(key);
        if (range != null) {
            int n;
            try {
                n = Integer.parseInt(v);
            } catch (NumberFormatException e) {
                throw ApiException.field("invalid-input", "value", "Enter a whole number.");
            }
            if (n < range[0] || n > range[1]) {
                throw ApiException.field("invalid-input", "value",
                        "Enter a number from " + range[0] + " to " + range[1] + ".");
            }
        } else if (Settings.CONSENT_VERSION.equals(key)) {
            if (!VERSION.matcher(v).matches()) {
                throw ApiException.field("invalid-input", "value", "Use letters, numbers, dots or dashes.");
            }
        } else {
            throw ApiException.notFound("Setting");
        }
        String before = settings.stringValue(key);
        settings.update(key, v, adminId);
        audit.record(adminId, ADMIN, "SETTING_CHANGED", "system_setting", null,
                Map.of("key", key, "from", before, "to", v));
    }

    public List<Map<String, Object>> audit(String action, int size, int page) {
        String a = action == null ? "" : action.trim();
        return jdbc.sql("""
                        SELECT id, occurred_at, actor_account_id, actor_role, action, target_type, target_id,
                               details
                        FROM audit_event WHERE (:a = '' OR action = :a)
                        ORDER BY occurred_at DESC, id DESC LIMIT :size OFFSET :offset""")
                .param("a", a).param("size", size).param("offset", page * size)
                .query(Rows.MAP).list();
    }

    public List<String> auditActions() {
        return jdbc.sql("SELECT DISTINCT action FROM audit_event ORDER BY action").query(String.class).list();
    }

    // --- helpers --------------------------------------------------------------------------------------------

    private int count(String sql) {
        return jdbc.sql(sql).query(Integer.class).single();
    }

    private static void found(int rows, String what) {
        if (rows == 0) {
            throw ApiException.notFound(what);
        }
    }

    private static void checkStatus(String status) {
        if (status != null && !List.of("DRAFT", "PUBLISHED", "ARCHIVED").contains(status)) {
            throw ApiException.badRequest("invalid-input", "Unknown status.");
        }
    }

    private static String trimToNull(String s, int max) {
        if (s == null || s.isBlank()) {
            return null;
        }
        String t = s.trim();
        if (t.length() > max) {
            throw ApiException.badRequest("invalid-input", "Please use at most " + max + " characters.");
        }
        return t;
    }
}
