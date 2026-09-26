package org.clevercubs.family;

import java.time.Instant;
import java.time.LocalDateTime;
import java.time.ZoneOffset;
import java.util.List;
import java.util.Map;
import java.util.Set;

import org.clevercubs.audit.AuditLog;
import org.clevercubs.child.ChildService;
import org.clevercubs.child.ChildService.ChildRow;
import org.clevercubs.child.UsernameRules;
import org.clevercubs.learning.ProgressService;
import org.clevercubs.learning.ProgressService.CourseProgress;
import org.clevercubs.platform.security.Role;
import org.clevercubs.platform.settings.Settings;
import org.clevercubs.platform.web.ApiException;
import org.springframework.jdbc.core.simple.JdbcClient;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

/**
 * The escalation inbox (requirement section 7, D59): when something needs a grown-up, the child asks, and the
 * request waits for the parent in the parent area. The child sees only the state of their own requests, never
 * any parent data. At most one pending request per child, type and quiz. Email notification is a later
 * configuration (INF-04).
 */
@Service
public class RequestService {

    public record RequestView(long id, long childId, String childName, String type, Long quizId, String quizTitle,
            String requestedValue, String status, Instant createdAt, Instant resolvedAt) {
    }

    private static final Set<String> TYPES = Set.of("QUIZ_ATTEMPTS", "USERNAME_CHANGE", "HELP");

    private final JdbcClient jdbc;
    private final ChildService children;
    private final ProgressService progress;
    private final Settings settings;
    private final AuditLog audit;

    public RequestService(JdbcClient jdbc, ChildService children, ProgressService progress, Settings settings,
            AuditLog audit) {
        this.jdbc = jdbc;
        this.children = children;
        this.progress = progress;
        this.settings = settings;
        this.audit = audit;
    }

    /** "Ask a grown-up", from the child's session. */
    @Transactional
    public RequestView create(long childId, String type, Long quizId, String requestedValue) {
        if (type == null || !TYPES.contains(type)) {
            throw ApiException.badRequest("invalid-input", "Unknown kind of request.");
        }
        ChildRow child = children.find(childId).orElseThrow(() -> ApiException.notFound("Child"));
        String value = null;
        Long quiz = null;
        switch (type) {
            case "QUIZ_ATTEMPTS" -> {
                if (quizId == null) {
                    throw ApiException.badRequest("invalid-input", "Which quiz is this for?");
                }
                boolean locked = progress.forChild(childId).values().stream()
                        .map(CourseProgress::quiz)
                        .anyMatch(q -> q != null && q.quizId() == quizId && q.locked());
                if (!locked) {
                    throw ApiException.rule("not-needed", "You still have tries left for this quiz.");
                }
                quiz = quizId;
            }
            case "USERNAME_CHANGE" -> {
                value = requestedValue == null ? "" : requestedValue.trim();
                String v = value;
                UsernameRules.problem(v, child.firstName()).ifPresent(message -> {
                    throw ApiException.field("invalid-username", "requestedValue", message);
                });
                if (!children.isUsernameFree(v, childId)) {
                    throw ApiException.field("username-taken", "requestedValue", "That username is taken.");
                }
            }
            default -> {
                // HELP carries no free text: a child's message is not collected (privacy by design).
            }
        }

        List<Long> pending = jdbc.sql("""
                        SELECT id FROM parent_request
                        WHERE child_id = :c AND type = :t AND status = 'PENDING' AND (quiz_id <=> :q)""")
                .param("c", childId).param("t", type).param("q", quiz).query(Long.class).list();
        if (!pending.isEmpty()) {
            return get(pending.getFirst());
        }
        jdbc.sql("""
                        INSERT INTO parent_request (child_id, parent_id, type, quiz_id, requested_value, status, created_at)
                        VALUES (:c, :p, :t, :q, :v, 'PENDING', :now)""")
                .param("c", childId).param("p", child.parentId()).param("t", type).param("q", quiz)
                .param("v", value).param("now", Instant.now()).update();
        long id = jdbc.sql("SELECT MAX(id) FROM parent_request WHERE child_id = :c AND type = :t")
                .param("c", childId).param("t", type).query(Long.class).single();
        return get(id);
    }

    public List<RequestView> forChild(long childId) {
        return list("r.child_id = :c", Map.of("c", childId));
    }

    public List<RequestView> forParent(long accountId, boolean pendingOnly) {
        return list("r.parent_id = (SELECT id FROM parent WHERE account_id = :a)"
                + (pendingOnly ? " AND r.status = 'PENDING'" : ""), Map.of("a", accountId));
    }

    @Transactional
    public RequestView approve(long accountId, long requestId) {
        RequestView r = owned(accountId, requestId);
        switch (r.type()) {
            case "QUIZ_ATTEMPTS" -> grant(accountId, r.childId(), r.quizId());
            case "USERNAME_CHANGE" -> {
                children.changeUsername(r.childId(), r.requestedValue());
                audit.record(accountId, Role.PARENT.name(), "CHILD_USERNAME_CHANGED", "child", r.childId(), Map.of());
            }
            default -> {
            }
        }
        resolve(requestId, "APPROVED");
        return get(requestId);
    }

    @Transactional
    public RequestView decline(long accountId, long requestId) {
        owned(accountId, requestId);
        resolve(requestId, "DECLINED");
        return get(requestId);
    }

    /**
     * Gives a locked quiz {@code quiz.grant_attempts} more tries (D63), from a request or directly from the
     * child's page. Audited every time.
     */
    @Transactional
    public void grant(long accountId, long childId, Long quizId) {
        children.requireOwned(accountId, childId);
        if (quizId == null) {
            throw ApiException.badRequest("invalid-input", "Which quiz is this for?");
        }
        int more = settings.intValue(Settings.GRANT_ATTEMPTS);
        int changed = jdbc.sql("""
                        UPDATE quiz_allowance SET attempts_allowed = attempts_allowed + :more, updated_at = :now
                        WHERE child_id = :c AND quiz_id = :q""")
                .param("more", more).param("now", Instant.now()).param("c", childId).param("q", quizId).update();
        if (changed == 0) {
            throw ApiException.rule("not-needed", "This quiz still has tries left.");
        }
        jdbc.sql("""
                        UPDATE parent_request SET status = 'APPROVED', resolved_at = :now
                        WHERE child_id = :c AND quiz_id = :q AND type = 'QUIZ_ATTEMPTS' AND status = 'PENDING'""")
                .param("now", Instant.now()).param("c", childId).param("q", quizId).update();
        audit.record(accountId, Role.PARENT.name(), "QUIZ_ATTEMPTS_GRANTED", "child", childId,
                Map.of("quizId", quizId, "attempts", more));
    }

    private RequestView owned(long accountId, long requestId) {
        RequestView r = list("r.id = :id AND r.parent_id = (SELECT id FROM parent WHERE account_id = :a)",
                Map.of("id", requestId, "a", accountId)).stream().findFirst()
                .orElseThrow(() -> ApiException.notFound("Request"));
        if (!"PENDING".equals(r.status())) {
            throw ApiException.conflict("already-resolved", "This request was already answered.");
        }
        return r;
    }

    private void resolve(long requestId, String status) {
        jdbc.sql("UPDATE parent_request SET status = :s, resolved_at = :now WHERE id = :id AND status = 'PENDING'")
                .param("s", status).param("now", Instant.now()).param("id", requestId).update();
    }

    private RequestView get(long id) {
        return list("r.id = :id", Map.of("id", id)).getFirst();
    }

    private List<RequestView> list(String where, Map<String, ?> params) {
        return jdbc.sql("""
                        SELECT r.id, r.child_id, ch.display_name, r.type, r.quiz_id, q.title, r.requested_value,
                               r.status, r.created_at, r.resolved_at
                        FROM parent_request r JOIN child ch ON ch.id = r.child_id
                        LEFT JOIN quiz q ON q.id = r.quiz_id
                        WHERE """ + " " + where + " ORDER BY r.status = 'PENDING' DESC, r.created_at DESC LIMIT 200")
                .params(params)
                .query((rs, n) -> {
                    LocalDateTime resolved = rs.getObject(10, LocalDateTime.class);
                    Long quiz = rs.getObject(5, Long.class);
                    return new RequestView(rs.getLong(1), rs.getLong(2), rs.getString(3), rs.getString(4),
                            quiz, rs.getString(6), rs.getString(7), rs.getString(8),
                            rs.getObject(9, LocalDateTime.class).toInstant(ZoneOffset.UTC),
                            resolved == null ? null : resolved.toInstant(ZoneOffset.UTC));
                })
                .list();
    }
}
