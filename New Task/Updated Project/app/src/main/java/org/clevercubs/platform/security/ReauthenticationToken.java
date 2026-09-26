package org.clevercubs.platform.security;

import java.io.Serial;

import org.springframework.security.authentication.UsernamePasswordAuthenticationToken;

/**
 * A request to prove the password again for a session that is <em>already</em> signed in — the
 * re-confirmation of {@code POST /api/v1/auth/reauth} (docs/04 §5, listed in phase B1 of §9), and the
 * confirmation {@code DD-02} asks for before the parent area is opened again.
 *
 * <p>It exists to tell one thing to {@link AccountAuthenticationProvider}: this is the same credential
 * decision as a sign-in, so it goes through the same lookup, the same BCrypt comparison, the same lock and
 * disabled checks and the same audit of a refusal — but it is not a sign-in. It must not overwrite
 * {@code last_login_at} and it must not write an {@code AUTH_LOGIN_SIGNED_IN} row, because neither of those
 * happened: a session was already open, and an audit trail that records a sign-in that did not occur is
 * worse than one that records nothing (DD-14).
 *
 * <p>Only the email address and the password are carried, both taken from the server side; there is nothing
 * here a caller could set to choose a different account.
 */
public final class ReauthenticationToken extends UsernamePasswordAuthenticationToken {

    @Serial
    private static final long serialVersionUID = 1L;

    private ReauthenticationToken(String email, String password) {
        super(email, password);
    }

    public static ReauthenticationToken of(String email, String password) {
        return new ReauthenticationToken(email, password);
    }
}
