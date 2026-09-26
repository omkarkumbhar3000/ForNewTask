package org.clevercubs.platform.security;

import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;

import java.io.IOException;
import java.net.URLEncoder;
import java.nio.charset.StandardCharsets;

import org.springframework.security.core.AuthenticationException;
import org.springframework.security.web.AuthenticationEntryPoint;
import org.springframework.stereotype.Component;

/**
 * Sends an unauthenticated browser (page) request to {@code /login?next=…}, so the family returns to the
 * page they asked for after signing in (requirement 8; docs/04-architecture-and-plan.md 4.1).
 *
 * <p>{@code next} is rebuilt from the request's own URI and query, never echoed from a parameter, and it is
 * accepted only when it is a local path. A value such as {@code //evil.example} or {@code /\\evil.example}
 * is protocol-relative or backslash-smuggled and a browser would send the family to another site with the
 * login page as the pretext, so it is discarded and the family lands on the plain login page. That closes
 * the open-redirect half of SEC-E08.
 */
@Component
public class LoginRedirectEntryPoint implements AuthenticationEntryPoint {

    static final String DEFAULT_LOGIN_PATH = "/login";

    private final String loginPath;

    public LoginRedirectEntryPoint() {
        this(DEFAULT_LOGIN_PATH);
    }

    public LoginRedirectEntryPoint(String loginPath) {
        this.loginPath = loginPath;
    }

    @Override
    public void commence(HttpServletRequest request, HttpServletResponse response, AuthenticationException e)
            throws IOException {
        String next = safeNext(request);
        response.sendRedirect(loginPath + "?next=" + URLEncoder.encode(next, StandardCharsets.UTF_8));
    }

    /** The local path the caller asked for, or the login page itself when the value cannot be trusted. */
    private String safeNext(HttpServletRequest request) {
        String uri = request.getRequestURI();
        if (!isLocalPath(uri)) {
            return loginPath;
        }
        String query = request.getQueryString();
        return (query == null || query.isBlank()) ? uri : uri + "?" + query;
    }

    /**
     * True only for a path that stays on this site: exactly one leading slash, and no second slash or
     * backslash directly after it, which a browser would read as a scheme-relative URL.
     */
    static boolean isLocalPath(String value) {
        if (value == null || value.isEmpty() || value.charAt(0) != '/') {
            return false;
        }
        if (value.length() == 1) {
            return true;
        }
        char second = value.charAt(1);
        return second != '/' && second != '\\';
    }
}
