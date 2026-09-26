package org.clevercubs.platform.security;

import org.clevercubs.platform.web.ApiException;
import org.springframework.http.HttpStatus;
import org.springframework.security.core.Authentication;
import org.springframework.security.core.context.SecurityContextHolder;
import org.springframework.stereotype.Component;

/**
 * Resolves the caller from the server session. Services call this instead of accepting identity
 * parameters, so a request can never act as someone else.
 */
@Component
public class CurrentUser {

    public SessionAuthentication session() {
        Authentication auth = SecurityContextHolder.getContext().getAuthentication();
        if (auth instanceof SessionAuthentication session && session.isAuthenticated()) {
            return session;
        }
        throw new ApiException(HttpStatus.UNAUTHORIZED, "unauthenticated", "Please sign in.");
    }

    public long accountId() {
        return session().account().accountId();
    }

    /** The child being served in child mode; fails closed in any other mode. */
    public long activeChildId() {
        SessionAuthentication s = session();
        if (s.mode() != Role.CHILD || s.activeChildId() == null) {
            throw ApiException.forbidden();
        }
        return s.activeChildId();
    }

    public void requireMode(Role mode) {
        if (session().mode() != mode) {
            throw ApiException.forbidden();
        }
    }
}
