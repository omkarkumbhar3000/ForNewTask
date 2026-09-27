package org.clevercubs.platform.db;

import static org.assertj.core.api.Assertions.assertThat;
import static org.assertj.core.api.Assertions.assertThatThrownBy;

import org.clevercubs.platform.db.SqlDialect.Vendor;
import org.junit.jupiter.api.Test;

/** The two statements MySQL and PostgreSQL write differently (D73). Both forms run in the database suites. */
class SqlDialectTests {

    private static final String INSERT = """
            INSERT INTO child_badge (child_id, badge_id, awarded_at)
            VALUES (:c, :b, :now)""";

    @Test
    void insertIgnoringDuplicatesUsesEachDatabasesOwnForm() {
        assertThat(new SqlDialect(Vendor.MYSQL).insertIgnoringDuplicates(INSERT))
                .startsWith("INSERT IGNORE INTO child_badge (child_id, badge_id, awarded_at)")
                .endsWith("VALUES (:c, :b, :now)");
        assertThat(new SqlDialect(Vendor.POSTGRESQL).insertIgnoringDuplicates(INSERT))
                .startsWith("INSERT INTO child_badge")
                .endsWith("VALUES (:c, :b, :now) ON CONFLICT DO NOTHING");
    }

    @Test
    void insertOrLockExistingNamesTheConflictKeyOnPostgresql() {
        String insert = "INSERT INTO quiz_allowance (child_id, quiz_id, attempts_allowed) VALUES (:c, :q, 3)";
        assertThat(new SqlDialect(Vendor.MYSQL)
                .insertOrLockExisting(insert, "quiz_allowance", "child_id, quiz_id", "attempts_allowed"))
                .endsWith("ON DUPLICATE KEY UPDATE attempts_allowed = attempts_allowed");
        assertThat(new SqlDialect(Vendor.POSTGRESQL)
                .insertOrLockExisting(insert, "quiz_allowance", "child_id, quiz_id", "attempts_allowed"))
                .endsWith("ON CONFLICT (child_id, quiz_id) DO UPDATE SET attempts_allowed = quiz_allowance.attempts_allowed");
    }

    @Test
    void onlyInsertStatementsAreAccepted() {
        assertThatThrownBy(() -> new SqlDialect(Vendor.MYSQL).insertIgnoringDuplicates("UPDATE child SET x = 1"))
                .isInstanceOf(IllegalArgumentException.class);
    }
}
