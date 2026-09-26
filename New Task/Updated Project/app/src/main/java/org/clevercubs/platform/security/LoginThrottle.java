package org.clevercubs.platform.security;

import java.time.Clock;
import java.time.Duration;
import java.util.ArrayDeque;
import java.util.Deque;
import java.util.Map;
import java.util.concurrent.ConcurrentHashMap;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Component;

/**
 * Per-address throttle for password guesses (DD-05). The per-account lock lives in
 * {@link AccountAuthenticationProvider}; this stops one address from walking through many accounts.
 *
 * <p>In memory on purpose: it protects one running instance, needs no table and forgets everything on a
 * restart. A multi-instance deployment would move it to shared storage (docs/04 section 12).
 */
@Component
public class LoginThrottle {

    private static final Duration WINDOW = Duration.ofMinutes(15);

    private final int maxFailures;
    private final Clock clock;
    private final Map<String, Deque<Long>> failures = new ConcurrentHashMap<>();

    @Autowired
    public LoginThrottle(@Value("${clevercubs.security.max-failures-per-address:30}") int maxFailures) {
        this(maxFailures, Clock.systemUTC());
    }

    LoginThrottle(int maxFailures, Clock clock) {
        this.maxFailures = maxFailures;
        this.clock = clock;
    }

    /** True while the address has used up its failures for the current window. */
    public boolean isBlocked(String address) {
        Deque<Long> recent = failures.get(address);
        if (recent == null) {
            return false;
        }
        synchronized (recent) {
            prune(recent);
            return recent.size() >= maxFailures;
        }
    }

    public void recordFailure(String address) {
        Deque<Long> recent = failures.computeIfAbsent(address, a -> new ArrayDeque<>());
        synchronized (recent) {
            prune(recent);
            recent.addLast(clock.millis());
        }
        if (failures.size() > 10_000) {
            failures.entrySet().removeIf(e -> {
                synchronized (e.getValue()) {
                    prune(e.getValue());
                    return e.getValue().isEmpty();
                }
            });
        }
    }

    private void prune(Deque<Long> recent) {
        long cutoff = clock.millis() - WINDOW.toMillis();
        while (!recent.isEmpty() && recent.peekFirst() < cutoff) {
            recent.pollFirst();
        }
    }
}
