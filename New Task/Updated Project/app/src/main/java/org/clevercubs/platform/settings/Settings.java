package org.clevercubs.platform.settings;

import java.util.Map;
import java.util.TreeMap;

import org.clevercubs.platform.db.Timestamps;
import org.springframework.jdbc.core.simple.JdbcClient;
import org.springframework.stereotype.Component;
import org.springframework.transaction.annotation.Transactional;

/**
 * The business rules the Super Admin may change (docs/05-data-model.md section 3.6). Every rule reads its
 * value from here, so one number drives the whole application (for example the reward threshold, D64).
 * Values are read on each call; the table is tiny and this keeps admin changes effective immediately.
 */
@Component
public class Settings {

    public static final String LESSON_WEIGHT = "progress.lesson_weight_percent";
    public static final String MAX_ATTEMPTS = "quiz.max_attempts";
    public static final String GRANT_ATTEMPTS = "quiz.grant_attempts";
    public static final String DEFAULT_PASS_MARK = "quiz.default_pass_mark_percent";
    public static final String REWARD_THRESHOLD = "reward.threshold_percent";
    public static final String CHILD_IDLE_MINUTES = "session.child_idle_minutes";
    public static final String PARENT_REAUTH_MINUTES = "parent.reauth_minutes";
    public static final String CONSENT_VERSION = "consent.document_version";

    private final JdbcClient jdbc;

    public Settings(JdbcClient jdbc) {
        this.jdbc = jdbc;
    }

    public int intValue(String key) {
        return Integer.parseInt(stringValue(key));
    }

    public String stringValue(String key) {
        return jdbc.sql("SELECT setting_value FROM system_setting WHERE setting_key = :key")
                .param("key", key)
                .query(String.class)
                .optional()
                .orElseThrow(() -> new IllegalStateException("Missing system setting: " + key));
    }

    public Map<String, String> all() {
        Map<String, String> values = new TreeMap<>();
        jdbc.sql("SELECT setting_key, setting_value FROM system_setting")
                .query((rs, n) -> Map.entry(rs.getString(1), rs.getString(2)))
                .list()
                .forEach(entry -> values.put(entry.getKey(), entry.getValue()));
        return values;
    }

    /** Updates an existing setting. Unknown keys are rejected, so no new rule can be invented at runtime. */
    @Transactional
    public void update(String key, String value, long actorAccountId) {
        int rows = jdbc.sql("""
                        UPDATE system_setting SET setting_value = :value, updated_at = :now, updated_by = :actor
                        WHERE setting_key = :key""")
                .param("value", value)
                .param("now", Timestamps.now())
                .param("actor", actorAccountId)
                .param("key", key)
                .update();
        if (rows != 1) {
            throw new IllegalArgumentException("Unknown setting: " + key);
        }
    }
}
