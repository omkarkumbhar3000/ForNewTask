package org.clevercubs.platform.security;

/**
 * Account roles stored in {@code user_account.role}. {@link #CHILD} is not an account role: it is the mode
 * a parent's session enters for one of their own children, and it replaces the parent's authority (D58).
 */
public enum Role {
    PARENT, SUPER_ADMIN, CHILD;

    public String authority() {
        return "ROLE_" + name();
    }
}
