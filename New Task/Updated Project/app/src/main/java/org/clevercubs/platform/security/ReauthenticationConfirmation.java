package org.clevercubs.platform.security;

import java.time.Instant;
import java.util.Optional;

import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpSession;

/**
 * When this session last had its password proven, and nothing else.
 *
 * <p>{@code DD-02} asks for the parent area to need the password again once the last one is more than
 * {@code parent.reauth_minutes} old (15, seeded in {@code V2__reference_data.sql} and admin-editable through
 * {@code Settings}), and {@code docs/04} §4.1 asks for a recent password confirmation before a Super Admin's
 * sensitive actions. Re-authenticating is the act that refreshes it; this is where the answer is kept.
 *
 * <p>A session attribute, not a column. The fact being recorded is about <em>this</em> session's holder, not
 * about the account: a second sign-in elsewhere must not refresh the window on the first device, and an
 * account-wide timestamp would have to answer "when was the password last entered", which is not a property
 * of a row. It also needs no migration, which is the reason there is no schema change in this slice.
 *
 * <p>Signing in marks it too, because a sign-in is a password being entered; under the other reading a
 * freshly signed-in parent would be treated as stale the moment they arrived, which cannot be what DD-02
 * means.
 */
public final class ReauthenticationConfirmation {

    private static final String ATTRIBUTE = "clevercubs.password-confirmed-at";

    private ReauthenticationConfirmation() {
    }

    /**
     * Records that the password has just been proven. A request with no session has nothing to mark, which
     * cannot happen on either path that calls this: signing in and re-authenticating have just written one.
     */
    public static void mark(HttpServletRequest request) {
        HttpSession session = request.getSession(false);
        if (session != null) {
            session.setAttribute(ATTRIBUTE, Instant.now());
        }
    }

    /** When the password was last proven in this session, if it ever was. */
    public static Optional<Instant> confirmedAt(HttpServletRequest request) {
        HttpSession session = request.getSession(false);
        if (session == null) {
            return Optional.empty();
        }
        Object stored = session.getAttribute(ATTRIBUTE);
        return stored instanceof Instant when ? Optional.of(when) : Optional.empty();
    }
}
