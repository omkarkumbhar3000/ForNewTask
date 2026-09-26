package org.clevercubs.platform.security;

import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;

import org.springframework.security.core.context.SecurityContext;
import org.springframework.security.core.context.SecurityContextHolder;
import org.springframework.security.web.context.SecurityContextRepository;
import org.springframework.stereotype.Component;

/**
 * Puts an identity into the server session. Used by sign-in, registration, the password change and the
 * child/parent mode switch, so every path writes the same session attribute the filter chain reads.
 */
@Component
public class SessionWriter {

    private final SecurityContextRepository repository;

    public SessionWriter(SecurityContextRepository repository) {
        this.repository = repository;
    }

    /** Stores the identity without touching the session id (a password change keeps its session). */
    public void store(HttpServletRequest request, HttpServletResponse response, SessionAuthentication session) {
        SecurityContext context = SecurityContextHolder.createEmptyContext();
        context.setAuthentication(session);
        SecurityContextHolder.setContext(context);
        repository.saveContext(context, request, response);
    }

    /**
     * Stores a new identity or a change of privilege (sign-in, registration, entering or leaving child
     * mode) under a new session id, so an id seen before the change cannot carry the new privileges.
     */
    public void storeRotating(HttpServletRequest request, HttpServletResponse response,
            SessionAuthentication session) {
        if (request.getSession(false) != null) {
            request.changeSessionId();
        }
        store(request, response, session);
    }
}
