package org.clevercubs.platform;

import static org.assertj.core.api.Assertions.assertThat;
import static org.assertj.core.api.Assertions.assertThatThrownBy;

import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.SQLException;
import java.sql.Statement;
import java.util.List;

import org.clevercubs.platform.settings.Settings;
import org.clevercubs.support.IntegrationTest;
import org.clevercubs.support.TestDatabase;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.jdbc.core.simple.JdbcClient;

/**
 * B0 checks: the schema migrates, the reference data matches the owner's decisions, and the application's
 * database user has least privilege (docs/05-data-model.md section 7; fixes SEC-E05).
 */
class DatabaseSetupTests extends IntegrationTest {

    @Autowired
    JdbcClient jdbc;

    @Autowired
    Settings settings;

    @Test
    void everyTableOfTheDataModelExists() {
        List<String> tables = jdbc.sql("""
                        SELECT table_name FROM information_schema.tables
                        WHERE table_schema = 'clevercubs' AND table_name <> 'flyway_schema_history'""")
                .query(String.class).list();
        assertThat(tables).containsExactlyInAnyOrder(
                "user_account", "parent", "child", "consent_record", "age_group", "course", "lesson",
                "lesson_item", "program", "program_course", "ui_message", "program_enrolment",
                "lesson_item_view", "lesson_completion", "quiz", "quiz_question", "quiz_option",
                "quiz_allowance", "quiz_attempt", "quiz_attempt_answer", "badge", "child_badge",
                "certificate", "parent_request", "feedback", "audit_event", "system_setting");
    }

    @Test
    void ageGroupsAreTheOwnersBands() { // D66
        record Band(String code, int min, int max) {
        }
        List<Band> bands = jdbc.sql("SELECT code, min_age, max_age FROM age_group ORDER BY sort_order")
                .query((rs, n) -> new Band(rs.getString(1), rs.getInt(2), rs.getInt(3))).list();
        assertThat(bands).containsExactly(new Band("TINY", 2, 3), new Band("LITTLE", 4, 5), new Band("BIG", 6, 8));
    }

    @Test
    void ruleSettingsMatchTheOwnersDecisions() { // D61, D62, D63, D64
        assertThat(settings.intValue(Settings.LESSON_WEIGHT)).isEqualTo(70);
        assertThat(settings.intValue(Settings.DEFAULT_PASS_MARK)).isEqualTo(70);
        assertThat(settings.intValue(Settings.MAX_ATTEMPTS)).isEqualTo(3);
        assertThat(settings.intValue(Settings.GRANT_ATTEMPTS)).isEqualTo(3);
        assertThat(settings.intValue(Settings.REWARD_THRESHOLD)).isEqualTo(80);
    }

    @Test
    void theApplicationUserIsNotASuperuser() throws SQLException {
        try (Connection app = appConnection(); Statement st = app.createStatement()) {
            assertThatThrownBy(() -> st.execute("CREATE TABLE intruder (id INT)"))
                    .isInstanceOf(SQLException.class).hasMessageContaining("denied");
            assertThatThrownBy(() -> st.execute("DROP TABLE child"))
                    .isInstanceOf(SQLException.class).hasMessageContaining("denied");
            assertThatThrownBy(() -> st.executeQuery("SELECT user FROM mysql.user"))
                    .isInstanceOf(SQLException.class).hasMessageContaining("denied");
        }
    }

    @Test
    void theAuditTrailIsAppendOnlyForTheApplication() throws SQLException {
        try (Connection app = appConnection(); Statement st = app.createStatement()) {
            st.executeUpdate("""
                    INSERT INTO audit_event (occurred_at, actor_role, action)
                    VALUES (UTC_TIMESTAMP(6), 'SYSTEM', 'TEST_APPEND_ONLY')""");
            assertThatThrownBy(() -> st.executeUpdate("UPDATE audit_event SET action = 'TAMPERED'"))
                    .isInstanceOf(SQLException.class).hasMessageContaining("denied");
            assertThatThrownBy(() -> st.executeUpdate("DELETE FROM audit_event"))
                    .isInstanceOf(SQLException.class).hasMessageContaining("denied");
        }
    }

    private static Connection appConnection() throws SQLException {
        return DriverManager.getConnection(TestDatabase.jdbcUrl(), "cc_app", TestDatabase.APP_PASSWORD);
    }
}
