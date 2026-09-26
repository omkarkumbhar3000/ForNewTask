package org.clevercubs.platform.security;

import static org.assertj.core.api.Assertions.assertThat;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.ValueSource;

/**
 * The open-redirect guard on the {@code next} parameter (SEC-E08), tested as plain JUnit with no Spring,
 * because the decision is a pure function of the string.
 */
class LoginRedirectEntryPointTests {

    @ParameterizedTest
    @ValueSource(strings = { "/", "/login", "/parent/dashboard", "/learn/lesson/7?a=b", "/admin" })
    @DisplayName("keeps a path that stays on this site")
    void keepsLocalPaths(String path) {
        assertThat(LoginRedirectEntryPoint.isLocalPath(path)).isTrue();
    }

    @ParameterizedTest
    @ValueSource(strings = {
            "//evil.example",          // protocol-relative: browser reads the host
            "/\\evil.example",         // backslash is normalised to a slash by the browser
            "https://evil.example",   // absolute
            "http://evil.example",
            "login",                  // relative, would resolve against the current path
            "evil.example",
            "",                        // empty
    })
    @DisplayName("rejects anything that could leave this site")
    void rejectsOffSitePaths(String path) {
        assertThat(LoginRedirectEntryPoint.isLocalPath(path)).isFalse();
    }

    @Test
    @DisplayName("rejects null rather than throwing")
    void rejectsNull() {
        assertThat(LoginRedirectEntryPoint.isLocalPath(null)).isFalse();
    }
}
