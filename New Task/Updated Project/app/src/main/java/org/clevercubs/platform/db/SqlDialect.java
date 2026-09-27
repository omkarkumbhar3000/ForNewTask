package org.clevercubs.platform.db;

import java.sql.Connection;
import java.sql.SQLException;
import java.util.Locale;

import javax.sql.DataSource;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;

/**
 * The only SQL that MySQL and PostgreSQL write differently, kept in one place (D73). Everything else the
 * application sends is standard SQL that both run unchanged. MySQL is the development and default test
 * database; PostgreSQL is used where the host offers no MySQL (docs/07-deployment.md).
 */
@Component
public class SqlDialect {

    public enum Vendor { MYSQL, POSTGRESQL }

    private static final String INSERT_INTO = "INSERT INTO";

    private final Vendor vendor;

    @Autowired
    public SqlDialect(DataSource dataSource) {
        this.vendor = detect(dataSource);
    }

    /** For tests of the SQL text alone. */
    SqlDialect(Vendor vendor) {
        this.vendor = vendor;
    }

    public Vendor vendor() {
        return vendor;
    }

    /**
     * Turns {@code INSERT INTO ...} into an insert that silently skips a row which would break a unique key
     * or primary key, instead of failing. Used where "already there" is a normal outcome (a card viewed
     * twice, a badge already earned); callers read the update count to know whether a row was added.
     */
    public String insertIgnoringDuplicates(String insert) {
        String sql = requireInsert(insert);
        return vendor == Vendor.MYSQL
                ? "INSERT IGNORE INTO" + sql.substring(INSERT_INTO.length())
                : sql + " ON CONFLICT DO NOTHING";
    }

    /**
     * Turns {@code INSERT INTO table ...} into an insert that, when the row already exists, leaves it
     * unchanged but locks it exclusively, as an update would. {@code keyColumns} is the unique key the
     * insert can collide on; {@code column} is any column of the table (it is set to itself).
     */
    public String insertOrLockExisting(String insert, String table, String keyColumns, String column) {
        String sql = requireInsert(insert);
        return vendor == Vendor.MYSQL
                ? sql + " ON DUPLICATE KEY UPDATE " + column + " = " + column
                : sql + " ON CONFLICT (" + keyColumns + ") DO UPDATE SET " + column + " = " + table + "." + column;
    }

    /**
     * A named parameter to compare with a column that ignores letter case: {@code user_account.email} and
     * {@code child.username}. MySQL's collation ignores case for any comparison. PostgreSQL's CITEXT columns
     * do so only against another CITEXT value; against the text parameter the driver sends, the comparison
     * would be case-sensitive, so the parameter is cast. Both forms still use the column's unique index.
     */
    public String caseInsensitive(String parameterName) {
        return vendor == Vendor.MYSQL ? ":" + parameterName : "CAST(:" + parameterName + " AS citext)";
    }

    private static String requireInsert(String insert) {
        String sql = insert.strip();
        if (!sql.regionMatches(true, 0, INSERT_INTO, 0, INSERT_INTO.length())) {
            throw new IllegalArgumentException("Expected an INSERT INTO statement");
        }
        return sql;
    }

    private static Vendor detect(DataSource dataSource) {
        try (Connection connection = dataSource.getConnection()) {
            String product = connection.getMetaData().getDatabaseProductName().toLowerCase(Locale.ROOT);
            return product.contains("postgres") ? Vendor.POSTGRESQL : Vendor.MYSQL;
        } catch (SQLException e) {
            throw new IllegalStateException("Could not read the database type", e);
        }
    }
}
