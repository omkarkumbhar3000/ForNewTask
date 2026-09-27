package org.clevercubs.audit;

import java.util.Map;

import org.clevercubs.platform.db.Timestamps;
import org.springframework.jdbc.core.simple.JdbcClient;
import org.springframework.stereotype.Component;

import tools.jackson.databind.json.JsonMapper;

/**
 * Append-only audit trail (requirement 19, DD-14). The database user cannot update or delete these rows.
 * Details hold identifiers and outcomes only: never passwords, names, email addresses or free text.
 */
@Component
public class AuditLog {

    private final JdbcClient jdbc;
    private final JsonMapper json = JsonMapper.builder().build();

    public AuditLog(JdbcClient jdbc) {
        this.jdbc = jdbc;
    }

    public void record(Long actorAccountId, String actorRole, String action, String targetType, Long targetId,
            Map<String, ?> details) {
        jdbc.sql("""
                        INSERT INTO audit_event (occurred_at, actor_account_id, actor_role, action, target_type,
                                                 target_id, details)
                        VALUES (:at, :actor, :role, :action, :targetType, :targetId, CAST(:details AS JSON))""")
                .param("at", Timestamps.now())
                .param("actor", actorAccountId)
                .param("role", actorRole)
                .param("action", action)
                .param("targetType", targetType)
                .param("targetId", targetId)
                .param("details", details == null || details.isEmpty() ? null : json.writeValueAsString(details))
                .update();
    }

    public void record(Long actorAccountId, String actorRole, String action) {
        record(actorAccountId, actorRole, action, null, null, null);
    }
}
