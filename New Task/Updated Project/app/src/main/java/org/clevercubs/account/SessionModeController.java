package org.clevercubs.account;

import java.util.Map;

import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;
import jakarta.validation.Valid;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotNull;
import jakarta.validation.constraints.Size;

import org.clevercubs.audit.AuditLog;
import org.clevercubs.child.ChildService;
import org.clevercubs.platform.security.CurrentUser;
import org.clevercubs.platform.security.ReauthenticationConfirmation;
import org.clevercubs.platform.security.ReauthenticationToken;
import org.clevercubs.platform.security.Role;
import org.clevercubs.platform.security.SessionAuthentication;
import org.clevercubs.platform.security.SessionWriter;
import org.clevercubs.platform.web.ApiException;
import org.springframework.http.HttpStatus;
import org.springframework.security.authentication.AuthenticationManager;
import org.springframework.security.core.AuthenticationException;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

/**
 * "Who is learning?" and the way back (D58). A parent picks one of their own children and the session
 * becomes that child's: only {@code ROLE_CHILD} remains, so the parent and admin areas close. Returning to
 * the parent area needs the parent's password again. Both switches rotate the session id.
 */
@RestController
@RequestMapping("/api/v1/session")
class SessionModeController {

    record ChildModeRequest(@NotNull(message = "required") Long childId) {
    }

    record ParentModeRequest(@NotBlank(message = "required") @Size(max = 200, message = "is too long") String password) {
    }

    private final CurrentUser currentUser;
    private final ChildService children;
    private final SessionWriter sessions;
    private final AuthenticationManager authenticationManager;
    private final AuditLog audit;

    SessionModeController(CurrentUser currentUser, ChildService children, SessionWriter sessions,
            AuthenticationManager authenticationManager, AuditLog audit) {
        this.currentUser = currentUser;
        this.children = children;
        this.sessions = sessions;
        this.authenticationManager = authenticationManager;
        this.audit = audit;
    }

    @PostMapping("/child")
    Map<String, Object> enterChildMode(@Valid @RequestBody ChildModeRequest body, HttpServletRequest request,
            HttpServletResponse response) {
        SessionAuthentication session = currentUser.session();
        currentUser.requireMode(Role.PARENT);
        long accountId = session.account().accountId();
        children.requireOwned(accountId, body.childId());
        sessions.storeRotating(request, response, SessionAuthentication.childMode(session.account(), body.childId()));
        audit.record(accountId, Role.PARENT.name(), "CHILD_MODE_ENTERED", "child", body.childId(), Map.of());
        return Map.of("mode", Role.CHILD.name(), "childId", body.childId());
    }

    @PostMapping("/parent")
    Map<String, Object> returnToParent(@Valid @RequestBody ParentModeRequest body, HttpServletRequest request,
            HttpServletResponse response) {
        SessionAuthentication session = currentUser.session();
        currentUser.requireMode(Role.CHILD);
        try {
            authenticationManager.authenticate(ReauthenticationToken.of(session.account().email(), body.password()));
        } catch (AuthenticationException refused) {
            throw new ApiException(HttpStatus.UNAUTHORIZED, "invalid-credentials", "That password is not right.");
        }
        sessions.storeRotating(request, response, SessionAuthentication.signedIn(session.account()));
        ReauthenticationConfirmation.mark(request);
        return Map.of("mode", Role.PARENT.name());
    }
}
