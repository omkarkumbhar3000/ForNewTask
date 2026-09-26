package org.clevercubs.learning;

import java.security.SecureRandom;
import java.util.List;
import java.util.Map;

import org.springframework.jdbc.core.simple.JdbcClient;
import org.springframework.stereotype.Component;

/**
 * Age-appropriate wording from {@code ui_message} (requirement sections 5 and 14). A row for the child's age
 * group wins over the rows for every group; several rows under one key rotate. Placeholders such as
 * {@code {name}} are filled here; the pages always render the result as text, never as HTML.
 */
@Component
public class Messages {

    private static final SecureRandom RANDOM = new SecureRandom();

    private final JdbcClient jdbc;

    public Messages(JdbcClient jdbc) {
        this.jdbc = jdbc;
    }

    public String pick(String key, Long ageGroupId, Map<String, String> values) {
        List<String> options = ageGroupId == null ? List.of() : jdbc.sql("""
                        SELECT text FROM ui_message WHERE message_key = :k AND age_group_id = :g AND active""")
                .param("k", key).param("g", ageGroupId).query(String.class).list();
        if (options.isEmpty()) {
            options = jdbc.sql("SELECT text FROM ui_message WHERE message_key = :k AND age_group_id IS NULL AND active")
                    .param("k", key).query(String.class).list();
        }
        if (options.isEmpty()) {
            return "";
        }
        String text = options.get(RANDOM.nextInt(options.size()));
        for (var e : values.entrySet()) {
            text = text.replace("{" + e.getKey() + "}", e.getValue() == null ? "" : e.getValue());
        }
        return text;
    }

    public String pick(String key, Long ageGroupId) {
        return pick(key, ageGroupId, Map.of());
    }
}
