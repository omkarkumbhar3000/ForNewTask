package org.clevercubs.platform.db;

import java.sql.ResultSet;
import java.sql.SQLException;
import java.sql.Timestamp;
import java.util.Map;

import org.springframework.jdbc.core.ColumnMapRowMapper;
import org.springframework.jdbc.core.RowMapper;

/**
 * Reads a row as a column-name map with the same value types on MySQL and PostgreSQL, so an API that
 * returns such a map answers identically on both: timestamps as a UTC {@link java.time.LocalDateTime}
 * (sent as an ISO time without a zone, which the pages read as UTC) and JSON columns as their text.
 * Use {@code .query(Rows.MAP).list()} instead of {@code .query().listOfRows()}.
 */
public final class Rows {

    public static final RowMapper<Map<String, Object>> MAP = new PortableColumnMapRowMapper();

    private Rows() {
    }

    private static final class PortableColumnMapRowMapper extends ColumnMapRowMapper {

        @Override
        protected Object getColumnValue(ResultSet rs, int index) throws SQLException {
            Object value = super.getColumnValue(rs, index);
            if (value instanceof Timestamp timestamp) {
                // PostgreSQL returns a Timestamp for a zone-less column; MySQL returns a LocalDateTime.
                return timestamp.toLocalDateTime();
            }
            if (value != null && value.getClass().getName().equals("org.postgresql.util.PGobject")) {
                // A PostgreSQL JSON value; MySQL returns JSON as a String.
                return rs.getString(index);
            }
            return value;
        }
    }
}
