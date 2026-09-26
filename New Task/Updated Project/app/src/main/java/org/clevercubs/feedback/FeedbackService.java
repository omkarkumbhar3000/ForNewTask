package org.clevercubs.feedback;

import java.time.Instant;
import java.time.LocalDateTime;
import java.time.ZoneOffset;
import java.util.List;
import java.util.Map;
import java.util.Set;

import org.clevercubs.audit.AuditLog;
import org.clevercubs.platform.security.Role;
import org.clevercubs.platform.web.ApiException;
import org.springframework.jdbc.core.simple.JdbcClient;
import org.springframework.stereotype.Service;

/**
 * Parent feedback (requirement section 15). Stored as plain text with bound parameters and always shown as
 * text, never HTML (fixes SEC-E01, SEC-E18). Readable by its author and by the Super Admin only; a child's
 * session cannot reach it at all.
 */
@Service
public class FeedbackService {

    public record FeedbackView(long id, String category, Long courseId, String courseTitle, Integer rating,
            String message, String status, Instant createdAt, Long parentAccountId, String parentName) {
    }

    public static final Set<String> CATEGORIES = Set.of("GENERAL", "COURSE", "USABILITY", "SUGGESTION", "PROBLEM");
    private static final Set<String> STATUSES = Set.of("NEW", "READ", "RESOLVED");

    private final JdbcClient jdbc;
    private final AuditLog audit;

    public FeedbackService(JdbcClient jdbc, AuditLog audit) {
        this.jdbc = jdbc;
        this.audit = audit;
    }

    public FeedbackView submit(long accountId, String category, Long courseId, Integer rating, String message) {
        if (!CATEGORIES.contains(category)) {
            throw ApiException.field("invalid-input", "category", "Please choose what the feedback is about.");
        }
        if (rating != null && (rating < 1 || rating > 5)) {
            throw ApiException.field("invalid-input", "rating", "Choose between 1 and 5 stars.");
        }
        String text = message == null ? "" : message.strip();
        if (text.length() < 3 || text.length() > 2000) {
            throw ApiException.field("invalid-input", "message", "Please write between 3 and 2000 characters.");
        }
        long parentId = jdbc.sql("SELECT id FROM parent WHERE account_id = :a").param("a", accountId)
                .query(Long.class).optional().orElseThrow(() -> ApiException.notFound("Parent"));
        Long course = courseId == null ? null : jdbc.sql("SELECT id FROM course WHERE id = :c")
                .param("c", courseId).query(Long.class).optional().orElse(null);
        Instant now = Instant.now();
        jdbc.sql("""
                        INSERT INTO feedback (parent_id, category, course_id, rating, message, status, created_at, updated_at)
                        VALUES (:p, :cat, :course, :rating, :msg, 'NEW', :now, :now)""")
                .param("p", parentId).param("cat", category).param("course", course).param("rating", rating)
                .param("msg", text).param("now", now).update();
        long id = jdbc.sql("SELECT MAX(id) FROM feedback WHERE parent_id = :p").param("p", parentId)
                .query(Long.class).single();
        return list("f.id = :id", Map.of("id", id), 1, 0).getFirst();
    }

    public List<FeedbackView> ownFeedback(long accountId) {
        return list("p.account_id = :a", Map.of("a", accountId), 100, 0);
    }

    public List<FeedbackView> forAdmin(String status, int size, int page) {
        if (status != null && !status.isBlank()) {
            if (!STATUSES.contains(status)) {
                throw ApiException.badRequest("invalid-input", "Unknown status.");
            }
            return list("f.status = :s", Map.of("s", status), size, page);
        }
        return list("TRUE", Map.of(), size, page);
    }

    public FeedbackView setStatus(long adminAccountId, long feedbackId, String status) {
        if (!STATUSES.contains(status)) {
            throw ApiException.badRequest("invalid-input", "Unknown status.");
        }
        int changed = jdbc.sql("UPDATE feedback SET status = :s, updated_at = :now WHERE id = :id")
                .param("s", status).param("now", Instant.now()).param("id", feedbackId).update();
        if (changed == 0) {
            throw ApiException.notFound("Feedback");
        }
        audit.record(adminAccountId, Role.SUPER_ADMIN.name(), "FEEDBACK_STATUS_CHANGED", "feedback", feedbackId,
                Map.of("status", status));
        return list("f.id = :id", Map.of("id", feedbackId), 1, 0).getFirst();
    }

    private List<FeedbackView> list(String where, Map<String, ?> params, int size, int page) {
        return jdbc.sql("""
                        SELECT f.id, f.category, f.course_id, c.title, f.rating, f.message, f.status, f.created_at,
                               p.account_id, p.full_name
                        FROM feedback f JOIN parent p ON p.id = f.parent_id LEFT JOIN course c ON c.id = f.course_id
                        WHERE """ + " " + where + " ORDER BY f.created_at DESC LIMIT :size OFFSET :offset")
                .params(params).param("size", size).param("offset", page * size)
                .query((rs, n) -> new FeedbackView(rs.getLong(1), rs.getString(2), rs.getObject(3, Long.class),
                        rs.getString(4), rs.getObject(5, Integer.class), rs.getString(6), rs.getString(7),
                        rs.getObject(8, LocalDateTime.class).toInstant(ZoneOffset.UTC), rs.getLong(9),
                        rs.getString(10)))
                .list();
    }
}
