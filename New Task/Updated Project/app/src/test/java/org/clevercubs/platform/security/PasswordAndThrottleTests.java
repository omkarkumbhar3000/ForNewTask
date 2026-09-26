package org.clevercubs.platform.security;

import static org.assertj.core.api.Assertions.assertThat;

import java.time.Clock;
import java.time.Duration;
import java.time.Instant;
import java.time.ZoneOffset;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;

/** DD-01 (password rule) and DD-05 (per-address throttle), without Spring. */
class PasswordAndThrottleTests {

    private final PasswordPolicy policy = new PasswordPolicy();

    @Test
    void acceptsALongPassphrase() {
        assertThat(policy.problem("Sunny-garden-path-42", "pat@example.test")).isEmpty();
    }

    @Test
    @DisplayName("refuses short, common, repetitive and self-referencing passwords")
    void refusesWeakPasswords() {
        assertThat(policy.problem("short", null)).isPresent();
        assertThat(policy.problem("123456789012", null)).isPresent();
        assertThat(policy.problem("aaaaaaaaaaaaaaa", null)).isPresent();
        assertThat(policy.problem("CleverCubs-2026!", null)).isPresent();
        assertThat(policy.problem("patricia-1234567", "patricia@example.test")).isPresent();
        assertThat(policy.problem("x".repeat(201), null)).isPresent();
    }

    @Test
    @DisplayName("an address is blocked after the limit and released when the window passes")
    void throttleWindow() {
        MutableClock clock = new MutableClock();
        LoginThrottle throttle = new LoginThrottle(3, clock);
        for (int i = 0; i < 3; i++) {
            assertThat(throttle.isBlocked("10.0.0.1")).isFalse();
            throttle.recordFailure("10.0.0.1");
        }
        assertThat(throttle.isBlocked("10.0.0.1")).isTrue();
        assertThat(throttle.isBlocked("10.0.0.2")).as("other addresses are unaffected").isFalse();
        clock.advance(Duration.ofMinutes(16));
        assertThat(throttle.isBlocked("10.0.0.1")).isFalse();
    }

    private static final class MutableClock extends Clock {
        private Instant now = Instant.parse("2026-09-26T10:00:00Z");

        void advance(Duration d) {
            now = now.plus(d);
        }

        @Override
        public java.time.ZoneId getZone() {
            return ZoneOffset.UTC;
        }

        @Override
        public Clock withZone(java.time.ZoneId zone) {
            return this;
        }

        @Override
        public Instant instant() {
            return now;
        }
    }
}
