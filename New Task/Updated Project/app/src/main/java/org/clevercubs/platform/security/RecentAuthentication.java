package org.clevercubs.platform.security;

import java.time.Duration;
import java.time.Instant;

import jakarta.servlet.http.HttpServletRequest;

import org.clevercubs.platform.settings.Settings;
import org.clevercubs.platform.web.ApiException;
import org.springframework.stereotype.Component;

/**
 * Guards sensitive actions (deleting a child, exporting data, admin account and settings changes) behind a
 * recent password confirmation: the password must have been proven within {@code parent.reauth_minutes}
 * (DD-02, docs/04 section 4.1). Otherwise the caller gets {@code reauth-required}; the page asks for the
 * password ({@code POST /api/v1/auth/reauth}) and retries.
 */
@Component
public class RecentAuthentication {

    private final Settings settings;

    public RecentAuthentication(Settings settings) {
        this.settings = settings;
    }

    public void require(HttpServletRequest request) {
        Duration window = Duration.ofMinutes(settings.intValue(Settings.PARENT_REAUTH_MINUTES));
        Instant confirmed = ReauthenticationConfirmation.confirmedAt(request).orElse(Instant.EPOCH);
        if (confirmed.plus(window).isBefore(Instant.now())) {
            throw ApiException.reauthRequired();
        }
    }
}
