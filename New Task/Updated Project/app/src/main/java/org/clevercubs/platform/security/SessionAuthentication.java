package org.clevercubs.platform.security;

import java.io.Serial;
import java.util.List;

import org.springframework.security.authentication.AbstractAuthenticationToken;
import org.springframework.security.core.authority.SimpleGrantedAuthority;

/**
 * What the server session knows about the caller. The single source of identity for every request: no
 * endpoint ever trusts a user or child ID sent by the browser (fixes SEC-E04, SEC-E15).
 *
 * <p>In child mode the only authority is {@code ROLE_CHILD} and {@link #activeChildId()} is set; the
 * parent's own authority is dropped, so parent and admin endpoints are closed to the child.
 */
public final class SessionAuthentication extends AbstractAuthenticationToken {

    @Serial
    private static final long serialVersionUID = 1L;

    private final AccountPrincipal principal;
    private final Role mode;
    private final Long activeChildId;

    private SessionAuthentication(AccountPrincipal principal, Role mode, Long activeChildId) {
        super(List.of(new SimpleGrantedAuthority(mode.authority())));
        this.principal = principal;
        this.mode = mode;
        this.activeChildId = activeChildId;
        super.setAuthenticated(true);
    }

    /** The mode an account starts in after signing in: parent or admin, by its role. */
    public static SessionAuthentication signedIn(AccountPrincipal principal) {
        return new SessionAuthentication(principal, principal.role(), null);
    }

    public static SessionAuthentication childMode(AccountPrincipal parent, long childId) {
        if (parent.role() != Role.PARENT) {
            throw new IllegalArgumentException("Only a parent can enter child mode");
        }
        return new SessionAuthentication(parent, Role.CHILD, childId);
    }

    public AccountPrincipal account() {
        return principal;
    }

    public Role mode() {
        return mode;
    }

    public Long activeChildId() {
        return activeChildId;
    }

    public SessionAuthentication withPrincipal(AccountPrincipal updated) {
        return new SessionAuthentication(updated, mode, activeChildId);
    }

    @Override
    public Object getCredentials() {
        return null;
    }

    @Override
    public Object getPrincipal() {
        return principal;
    }

    @Override
    public void setAuthenticated(boolean authenticated) {
        if (authenticated) {
            throw new IllegalArgumentException("Create a new SessionAuthentication instead");
        }
        super.setAuthenticated(false);
    }

    @Override
    public boolean equals(Object o) {
        return o instanceof SessionAuthentication other && super.equals(other)
                && principal.accountId() == other.principal.accountId() && mode == other.mode
                && java.util.Objects.equals(activeChildId, other.activeChildId);
    }

    @Override
    public int hashCode() {
        return java.util.Objects.hash(super.hashCode(), principal.accountId(), mode, activeChildId);
    }
}
