package org.clevercubs.platform.security;

import java.io.IOException;

import org.springframework.security.web.csrf.CsrfToken;
import org.springframework.web.filter.OncePerRequestFilter;

import jakarta.servlet.FilterChain;
import jakarta.servlet.ServletException;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;

/**
 * Makes sure the XSRF-TOKEN cookie is on the way out with every response, not only with the ones that are
 * being checked.
 *
 * <p>{@code CsrfFilter} only resolves the token for methods it protects, because that is all it needs to
 * decide whether to refuse a request. With {@code CookieCsrfTokenRepository} the cookie is written at the
 * moment the token is resolved, so a browser that loads a page, receives no cookie, and is then refused on
 * its first POST — the request that would have carried the token. The client would have to be taught to
 * retry, which is exactly the kind of thing a client cannot fix on its own.
 *
 * <p>Reading the token here, after {@code CsrfFilter} has published it, resolves it once and the cookie is
 * written. The value itself is unchanged: it is a random token whose only job is to prove the POST came
 * from a page this server served (DD-03), and it is a per-session nonce that proves nothing about the
 * caller's identity. The token is not a credential, which is why the cookie may be readable by script.
 */
final class CsrfCookieIssuingFilter extends OncePerRequestFilter {

    @Override
    protected void doFilterInternal(HttpServletRequest request, HttpServletResponse response, FilterChain chain)
            throws ServletException, IOException {

        Object attribute = request.getAttribute(CsrfToken.class.getName());
        if (attribute instanceof CsrfToken token) {
            token.getToken();
        }
        chain.doFilter(request, response);
    }
}
