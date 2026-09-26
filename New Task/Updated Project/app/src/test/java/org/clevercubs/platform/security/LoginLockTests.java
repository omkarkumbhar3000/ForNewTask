package org.clevercubs.platform.security;

import static org.assertj.core.api.Assertions.assertThat;
import static org.clevercubs.support.Journeys.json;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.post;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.jsonPath;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import java.time.LocalDateTime;

import org.clevercubs.support.IntegrationTest;
import org.clevercubs.support.Journeys;
import org.clevercubs.support.Journeys.Family;
import org.junit.jupiter.api.AfterEach;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.jdbc.core.simple.JdbcClient;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.test.web.servlet.MockMvc;

/** DD-05 and SEC-E08: repeated wrong passwords lock the account for a while, without saying so. */
class LoginLockTests extends IntegrationTest {

    @Autowired
    MockMvc mvc;

    @Autowired
    JdbcClient jdbc;

    @Autowired
    PasswordEncoder passwords;

    Journeys journeys;

    @BeforeEach
    void setUp() {
        journeys = new Journeys(mvc, jdbc, passwords);
    }

    @AfterEach
    void cleanUp() {
        journeys.cleanUp();
    }

    private void attempt(String email, String password, int expected) throws Exception {
        mvc.perform(json(post("/api/v1/auth/login"), "{\"email\":\"" + email + "\",\"password\":\"" + password + "\"}"))
                .andExpect(status().is(expected))
                .andExpect(jsonPath("$.code").value("invalid-credentials"));
    }

    @Test
    @DisplayName("five wrong passwords lock the account; even the right password is then refused, in the same words")
    void fiveFailuresLockTheAccount() throws Exception {
        Family f = journeys.family(4);
        for (int i = 0; i < AccountAuthenticationProvider.MAX_FAILURES; i++) {
            attempt(f.email(), "wrong-password-" + i, 401);
        }
        LocalDateTime lockedUntil = jdbc.sql("SELECT locked_until FROM user_account WHERE email = :e")
                .param("e", f.email()).query(LocalDateTime.class).single();
        assertThat(lockedUntil).as("locked for about 15 minutes").isAfter(LocalDateTime.now(java.time.ZoneOffset.UTC).plusMinutes(10));
        attempt(f.email(), Journeys.PASSWORD, 401);
        assertThat(jdbc.sql("SELECT COUNT(*) FROM audit_event WHERE action = 'AUTH_ACCOUNT_LOCKED' AND target_id = :a")
                .param("a", f.accountId()).query(Integer.class).single()).isEqualTo(1);
    }

    @Test
    @DisplayName("a successful sign-in resets the count of failures")
    void successResetsTheCount() throws Exception {
        Family f = journeys.family(4);
        for (int i = 0; i < AccountAuthenticationProvider.MAX_FAILURES - 1; i++) {
            attempt(f.email(), "wrong-password-" + i, 401);
        }
        journeys.login(f.email(), Journeys.PASSWORD);
        assertThat(jdbc.sql("SELECT failed_logins FROM user_account WHERE email = :e").param("e", f.email())
                .query(Integer.class).single()).isZero();
    }
}
