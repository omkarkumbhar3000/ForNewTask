package org.clevercubs.account;

import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;
import jakarta.validation.Valid;
import jakarta.validation.constraints.Email;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.Size;

import org.clevercubs.platform.security.CurrentUser;
import org.clevercubs.platform.security.LoginThrottle;
import org.clevercubs.platform.security.ReauthenticationConfirmation;
import org.clevercubs.platform.security.ReauthenticationToken;
import org.clevercubs.platform.security.SessionAuthentication;
import org.clevercubs.platform.web.ApiException;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.security.authentication.AuthenticationManager;
import org.springframework.security.authentication.UsernamePasswordAuthenticationToken;
import org.springframework.security.core.Authentication;
import org.springframework.security.core.AuthenticationException;
import org.springframework.security.core.context.SecurityContext;
import org.springframework.security.core.context.SecurityContextHolder;
import org.springframework.security.web.authentication.logout.LogoutHandler;
import org.springframework.security.web.context.SecurityContextRepository;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

/**
 * Signing in, who am I, signing out, proving the password again and changing it — the endpoints of
 * requirement §8, in the API shape {@code docs/04-architecture-and-plan.md} §5 sets out. The identity they
 * establish is a server session ({@link SessionAuthentication}), not a token the browser holds, and a future
 * mobile client uses the same calls over the same cookie or header the pages use.
 *
 * <p>There is no page form and no HTTP Basic here, so this controller is the only way in. It never accepts
 * an account id from the request: the account is found by the email address and the role comes from the
 * row, so a caller cannot ask to be someone else.
 */
@RestController
@RequestMapping("/api/v1/auth")
public class AuthController {

    /**
     * One message for every refusal, whatever the real reason. A different answer for "no such address"
     * than for "wrong password" would tell a stranger which addresses are registered (SEC-E07, SEC-E08);
     * the reason itself is recorded in {@code audit_event}.
     */
    private static final String INVALID_CREDENTIALS =
            "That email address and password do not match an account.";

    private final AuthenticationManager authenticationManager;
    private final SecurityContextRepository securityContext;
    private final LogoutHandler logoutHandler;
    private final CurrentUser currentUser;
    private final PasswordChangeService passwordChanges;
    private final RegistrationService registrations;
    private final LoginThrottle throttle;

    public AuthController(AuthenticationManager authenticationManager, SecurityContextRepository securityContext,
            LogoutHandler logoutHandler, CurrentUser currentUser, PasswordChangeService passwordChanges,
            RegistrationService registrations, LoginThrottle throttle) {
        this.authenticationManager = authenticationManager;
        this.securityContext = securityContext;
        this.logoutHandler = logoutHandler;
        this.currentUser = currentUser;
        this.passwordChanges = passwordChanges;
        this.registrations = registrations;
        this.throttle = throttle;
    }

    /**
     * Registers a parent with their first child and consent (requirement section 6), then signs the parent in
     * under a new session id, exactly as a sign-in would.
     */
    @PostMapping("/register")
    ResponseEntity<AccountSummary> register(@Valid @RequestBody RegistrationService.RegistrationRequest body,
            HttpServletRequest request, HttpServletResponse response) {
        SessionAuthentication session = SessionAuthentication.signedIn(registrations.register(body));
        if (request.getSession(false) != null) {
            request.changeSessionId();
        }
        store(request, response, session);
        ReauthenticationConfirmation.mark(request);
        return ResponseEntity.status(HttpStatus.CREATED).body(AccountSummary.of(session));
    }

    /**
     * Signs a parent or a Super Admin in and stores the result in the session.
     *
     * <p>Deliberately a POST with a JSON body and no form, and deliberately behind the same CSRF token as
     * every other state-changing call (DD-03): a browser that is made to post here is still only doing what
     * the user's own page did.
     */
    @PostMapping("/login")
    AccountSummary login(@Valid @RequestBody LoginRequest body, HttpServletRequest request,
            HttpServletResponse response) {
        // DD-05: one address may not walk through many accounts. The per-account lock is in the provider.
        String address = request.getRemoteAddr();
        if (throttle.isBlocked(address)) {
            throw ApiException.tooManyAttempts();
        }
        Authentication authenticated;
        try {
            authenticated = authenticationManager.authenticate(
                    UsernamePasswordAuthenticationToken.unauthenticated(body.email(), body.password()));
        } catch (AuthenticationException refused) {
            throttle.recordFailure(address);
            throw new ApiException(HttpStatus.UNAUTHORIZED, "invalid-credentials", INVALID_CREDENTIALS);
        }

        SessionAuthentication session = sessionOf(authenticated);

        // Session fixation defence, the same change the filter chain performs for its own sign-ins: an id
        // an attacker may have planted before the identity was known is never the id that carries it.
        if (request.getSession(false) != null) {
            request.changeSessionId();
        }

        store(request, response, session);
        ReauthenticationConfirmation.mark(request);

        return AccountSummary.of(session);
    }

    /**
     * Puts an identity into the server session, replacing whatever was there.
     *
     * <p>Shared by the two moments that establish one: a sign-in, and a password change that has just
     * cleared the temporary-password requirement. Both write the session attribute and both leave the
     * session id alone here — a sign-in rotates it just above, and a password change must not, because the
     * session it is repairing is the one the caller is using right now.
     */
    private void store(HttpServletRequest request, HttpServletResponse response, SessionAuthentication session) {
        SecurityContext context = SecurityContextHolder.createEmptyContext();
        context.setAuthentication(session);
        SecurityContextHolder.setContext(context);
        securityContext.saveContext(context, request, response);
    }

    /** Who the session belongs to. Never the password, and never the stored hash. */
    @GetMapping("/me")
    AccountSummary me() {
        return AccountSummary.of(currentUser.session());
    }

    /**
     * Signs out. The session is invalidated and the cookie is expired, so the next request from this client
     * is an unauthenticated one and gets 401. Behind CSRF protection like any other POST.
     */
    @PostMapping("/logout")
    ResponseEntity<Void> logout(HttpServletRequest request, HttpServletResponse response) {
        logoutHandler.logout(request, response, currentUser.session());
        return ResponseEntity.noContent().build();
    }

    /**
     * Proves the password again for a session that is already signed in — the confirmation DD-02 asks for
     * before the parent area is opened again, and the "recent password confirmation" of docs/04 §4.1.
     * Returning from child mode is a different, later call ({@code POST /session/parent}); this one is the
     * plain re-confirmation.
     *
     * <p>The account is taken from the session, never from the request, so there is no field here that
     * could point this at somebody else's account. The check itself is the same
     * {@code AccountAuthenticationProvider} the sign-in uses, so the password is verified the same way, a
     * locked or disabled account is still refused, and a wrong password is audited exactly as a wrong
     * password at sign-in is. The refusal is the same generic {@code invalid-credentials} answer, so this
     * endpoint reveals nothing about which accounts exist.
     *
     * <p>Nothing about the session changes on success: the identity is the one already in the session, so
     * there is nothing to re-issue and no session id to rotate. A temporary-password account stays a
     * temporary-password account — this call proves a password, it does not accept a new one.
     */
    @PostMapping("/reauth")
    ResponseEntity<Void> reauth(@Valid @RequestBody ReauthRequest body, HttpServletRequest request) {
        SessionAuthentication session = currentUser.session();
        try {
            authenticationManager.authenticate(
                    ReauthenticationToken.of(session.account().email(), body.password()));
        } catch (AuthenticationException refused) {
            throw new ApiException(HttpStatus.UNAUTHORIZED, "invalid-credentials", INVALID_CREDENTIALS);
        }
        ReauthenticationConfirmation.mark(request);
        return ResponseEntity.noContent().build();
    }

    /**
     * Replaces the signed-in account's password, and ends the temporary-password state it may be in.
     *
     * <p>This is the one route {@link org.clevercubs.platform.security.PasswordChangeRequiredFilter} allows
     * an account in that state to reach besides its own account, signing out and signing in again — the one
     * whose whole purpose is to end that state. Without it the Super Admin the bootstrap creates would sign
     * in, read itself, and be unable to do anything else, which is exactly what {@code D69} left in place
     * when it made that admin's password temporary.
     *
     * <p>Like {@link #reauth}, it takes no account id and no email address: the account is the session's,
     * and the only credential in the body is proved against it. The work is in
     * {@link PasswordChangeService}; this method is transport — the answer, and putting the new identity
     * into the session so the very next request from this client is no longer refused. The session id is not
     * reissued and the session is not invalidated, so a client part-way through a task keeps its place.
     *
     * <p>{@code 204} and an empty body, like every other successful call here: a new password is never echoed
     * back, not even to the client that just sent it.
     */
    @PostMapping("/change-password")
    ResponseEntity<Void> changePassword(@Valid @RequestBody ChangePasswordRequest body,
            HttpServletRequest request, HttpServletResponse response) {
        store(request, response, passwordChanges.change(body.currentPassword(), body.newPassword()));
        return ResponseEntity.noContent().build();
    }

    private static SessionAuthentication sessionOf(Authentication authenticated) {
        if (authenticated instanceof SessionAuthentication session) {
            return session;
        }
        // Only reachable if a different AuthenticationProvider is introduced; the contract of this
        // application is that the session carries a SessionAuthentication.
        throw new IllegalStateException("The authentication provider returned "
                + authenticated.getClass().getSimpleName() + " instead of a SessionAuthentication");
    }

    /**
     * The sign-in request. The password is bounded so a huge body cannot be turned into expensive hashing;
     * it is never trimmed, never normalised and never logged.
     */
    public record LoginRequest(
            @NotBlank(message = "required") @Email(message = "must be an email address")
            @Size(max = 254, message = "is too long") String email,
            @NotBlank(message = "required") @Size(max = 200, message = "is too long") String password) {
    }

    /**
     * The re-authentication request: a password and nothing else. There is deliberately no email address and
     * no account id, because the account is the session's. The password is bounded so a huge body cannot be
     * turned into expensive hashing, and is never trimmed, never normalised and never logged.
     */
    public record ReauthRequest(
            @NotBlank(message = "required") @Size(max = 200, message = "is too long") String password) {
    }

    /**
     * The password-change request: the current password, because it has to be proved, and the one to put in
     * its place. There is no email address and no account id for the same reason {@link ReauthRequest} has
     * none — the account is the session's.
     *
     * <p>Both are bounded, and neither is trimmed or normalised: a password is what the user typed. The
     * length rule on the new one is {@code DD-01}'s 12 characters and is the only rule, so a rejected value
     * comes back as an ordinary {@code invalid-input} field error rather than a new error code.
     */
    public record ChangePasswordRequest(
            @NotBlank(message = "required")
            @Size(max = PasswordChangeService.MAXIMUM_LENGTH, message = "is too long") String currentPassword,
            @NotBlank(message = "required")
            @Size(min = PasswordChangeService.MINIMUM_LENGTH, max = PasswordChangeService.MAXIMUM_LENGTH,
                    message = "must be between 12 and 200 characters") String newPassword) {
    }

    /**
     * What the client is told about the signed-in account. A hand-built record, never the principal itself,
     * so no field can be added to {@link org.clevercubs.platform.security.AccountPrincipal} and start
     * travelling to the browser by accident.
     */
    public record AccountSummary(long accountId, String email, String role, String mode, Long activeChildId,
            boolean mustChangePassword) {

        static AccountSummary of(SessionAuthentication session) {
            var account = session.account();
            return new AccountSummary(account.accountId(), account.email(), account.role().name(),
                    session.mode().name(), session.activeChildId(), account.mustChangePassword());
        }
    }
}
