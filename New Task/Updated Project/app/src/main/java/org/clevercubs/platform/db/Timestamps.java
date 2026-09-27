package org.clevercubs.platform.db;

import java.time.Instant;
import java.time.LocalDateTime;
import java.time.ZoneOffset;
import java.time.temporal.ChronoUnit;

/**
 * Every timestamp column holds UTC wall-clock time without a zone (V1__schema.sql), and is read back as a
 * {@link LocalDateTime} in UTC. Values are written the same way, as a UTC {@link LocalDateTime}, because
 * both the MySQL and the PostgreSQL drivers store that unchanged; the PostgreSQL driver cannot bind an
 * {@link Instant} at all. Microsecond precision matches the columns.
 */
public final class Timestamps {

    private Timestamps() {
    }

    /** Now, as the database stores it. */
    public static LocalDateTime now() {
        return LocalDateTime.now(ZoneOffset.UTC).truncatedTo(ChronoUnit.MICROS);
    }

    public static LocalDateTime of(Instant instant) {
        return instant == null ? null : LocalDateTime.ofInstant(instant, ZoneOffset.UTC).truncatedTo(ChronoUnit.MICROS);
    }
}
