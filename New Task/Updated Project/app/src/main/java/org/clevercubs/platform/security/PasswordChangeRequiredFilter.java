package org.clevercubs.platform.security;

import java.io.IOException;
import java.util.List;

import org.clevercubs.platform.web.ApiException;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.http.HttpMethod;
import org.springframework.security.core.Authentication;
import org.springframework.security.core.context.SecurityContextHolder;
import org.springframework.security.web.servlet.util.matcher.PathPatternRequestMatcher;
import org.springframework.security.web.util.matcher.RequestMatcher;
import org.springframework.web.filter.OncePerRequestFilter;

import jakarta.servlet.FilterChain;
import jakarta.servlet.ServletException;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;

/**
 * Holds an account that is still using an admin-issued temporary password ({@code must_change_password},
 * docs/05 §1) to its own account until the password is changed.
 *
 * <p>The flag is already read at sign-in and already reaches the client, but a value the client may ignore
 * is not a restriction. The baseline's central failure was exactly that — access decided in the browser
 * (docs/01 "Trust in the browser") — so the decision is taken here, on the server, for every request.
 *
 * <p>Placed after {@code AuthorizationFilter}, so it can only ever narrow what the allow list already
 * granted: a request the chain has already refused never reaches this filter, and a request it lets through
 * unchanged is untouched. It reads the account from the session, never from the request, so a caller cannot
 * claim, drop or forge the requirement.
 *
 * <p>While the flag is set the account keeps exactly what it needs to get out of the situation and nothing
 * else:
 * <ul>
 *   <li>{@code GET /api/v1/auth/me} — how the client learns the flag at all;</li>
 *   <li>{@code POST /api/v1/auth/logout} — the way back out;</li>
 *   <li>{@code POST /api/v1/auth/login} — signing in again is harmless, because the flag is read from
 *       {@code user_account} on every sign-in, so the new session is restricted too. It is allowed so that
 *       a documented endpoint does not answer a correct password with a refusal;</li>
 *   <li>{@code POST /api/v1/auth/reauth} — the same reasoning: the credential check must be able to happen,
 *       and a re-authentication neither clears the flag nor grants a single protected route;</li>
 *   <li>{@code POST /api/v1/auth/change-password} — the one route whose purpose is to end this state. It is
 *       allowed for exactly this reason and grants nothing on its own: until the password is actually
 *       changed, the flag is still set in {@code user_account} and every other route below is still
 *       refused. A caller that reaches it and fails to change anything has gained nothing;</li>
 *   <li>{@code /api/v1/public/**} — public already, and it protects nothing.</li>
 * </ul>
 * Every other route is refused with {@code password-change-required}. The list is deliberately short, and a
 * new route is refused rather than allowed: nothing here decides what a new route will do, only whether an
 * account in this state may reach it.
 *
 * <p>Nothing about the account, the session or the reason is disclosed: the refusal is the same generic shape
 * as any other, so it cannot be used to find out which addresses carry a temporary password.
 */
final class PasswordChangeRequiredFilter extends OncePerRequestFilter {

    private static final Logger log = LoggerFactory.getLogger(PasswordChangeRequiredFilter.class);

    private static final List<RequestMatcher> ALLOWED_WHILE_FLAGGED = List.of(
            PathPatternRequestMatcher.withDefaults().matcher(HttpMethod.GET, "/api/v1/auth/me"),
            PathPatternRequestMatcher.withDefaults().matcher(HttpMethod.POST, "/api/v1/auth/logout"),
            PathPatternRequestMatcher.withDefaults().matcher(HttpMethod.POST, "/api/v1/auth/login"),
            // Re-authenticating is how an account proves a password again; it is not a way past this rule.
            // It is reachable so the operation itself can happen, and it changes nothing here: the flag is
            // only cleared by a password being changed, and that is a different call.
            PathPatternRequestMatcher.withDefaults().matcher(HttpMethod.POST, "/api/v1/auth/reauth"),
            // The way out. Allowed for a flagged account only, and it clears nothing by being reached — see
            // the note in the class comment.
            PathPatternRequestMatcher.withDefaults().matcher(HttpMethod.POST, "/api/v1/auth/change-password"),
            PathPatternRequestMatcher.withDefaults().matcher("/api/v1/public/**"));

    private static final RequestMatcher API = PathPatternRequestMatcher.withDefaults().matcher("/api/**");

    private final ApiProblemEntryPoint refusals;

    PasswordChangeRequiredFilter(ApiProblemEntryPoint refusals) {
        this.refusals = refusals;
    }

    @Override
    protected void doFilterInternal(HttpServletRequest request, HttpServletResponse response, FilterChain chain)
            throws ServletException, IOException {

        // Only the data API is closed. Page shells, scripts and styles carry no data, and the account needs
        // them to reach the change-password form at all.
        if (mustChangePassword() && API.matches(request)
                && ALLOWED_WHILE_FLAGGED.stream().noneMatch(m -> m.matches(request))) {
            log.info("Refused {} for an account that must change its password", request.getRequestURI());
            refusals.write(response, ApiException.passwordChangeRequired());
            return;
        }
        chain.doFilter(request, response);
    }

    /**
     * The account as the session knows it. Keyed on the account and not on the mode, so entering child mode
     * cannot shed the requirement: it is the same parent password that is temporary.
     */
    private static boolean mustChangePassword() {
        Authentication authentication = SecurityContextHolder.getContext().getAuthentication();
        return authentication instanceof SessionAuthentication session
                && session.account().mustChangePassword();
    }
}
