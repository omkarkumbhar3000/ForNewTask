package org.clevercubs.platform.security;

import java.io.Serial;
import java.time.Instant;
import java.util.Collection;
import java.util.List;

import org.springframework.security.core.CredentialsContainer;
import org.springframework.security.core.GrantedAuthority;
import org.springframework.security.core.authority.SimpleGrantedAuthority;
import org.springframework.security.core.userdetails.UserDetails;

/**
 * A signed-in account (a parent or a Super Admin). Children never have a principal of their own: a parent
 * enters child mode instead (D58). The password hash is erased after authentication.
 */
public final class AccountPrincipal implements UserDetails, CredentialsContainer {

    @Serial
    private static final long serialVersionUID = 1L;

    private final long accountId;
    private final String email;
    private final Role role;
    private final boolean active;
    private final Instant lockedUntil;
    private final boolean mustChangePassword;
    private String passwordHash;

    public AccountPrincipal(long accountId, String email, String passwordHash, Role role, boolean active,
            Instant lockedUntil, boolean mustChangePassword) {
        this.accountId = accountId;
        this.email = email;
        this.passwordHash = passwordHash;
        this.role = role;
        this.active = active;
        this.lockedUntil = lockedUntil;
        this.mustChangePassword = mustChangePassword;
    }

    public long accountId() {
        return accountId;
    }

    public String email() {
        return email;
    }

    public Role role() {
        return role;
    }

    public boolean mustChangePassword() {
        return mustChangePassword;
    }

    public AccountPrincipal withPasswordChanged() {
        return new AccountPrincipal(accountId, email, null, role, active, lockedUntil, false);
    }

    @Override
    public Collection<? extends GrantedAuthority> getAuthorities() {
        return List.of(new SimpleGrantedAuthority(role.authority()));
    }

    @Override
    public String getPassword() {
        return passwordHash;
    }

    @Override
    public String getUsername() {
        return email;
    }

    @Override
    public boolean isAccountNonLocked() {
        return lockedUntil == null || lockedUntil.isBefore(Instant.now());
    }

    @Override
    public boolean isEnabled() {
        return active;
    }

    @Override
    public void eraseCredentials() {
        passwordHash = null;
    }

    @Override
    public String toString() {
        return "AccountPrincipal[id=" + accountId + ", role=" + role + "]";
    }
}
