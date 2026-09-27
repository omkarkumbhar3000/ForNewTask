package org.clevercubs.platform.security;

import static org.assertj.core.api.Assertions.assertThat;

import java.net.URI;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;
import java.nio.charset.StandardCharsets;
import java.util.List;
import java.util.UUID;

import org.clevercubs.platform.db.Timestamps;
import org.clevercubs.support.IntegrationTest;
import org.junit.jupiter.api.AfterEach;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.boot.test.web.server.LocalServerPort;
import org.springframework.jdbc.core.simple.JdbcClient;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.session.jdbc.JdbcIndexedSessionRepository;

/**
 * The database-backed sessions the running application uses (Spring Session JDBC, D73). The rest of the
 * suite turns them off, because MockMvc carries its sessions as MockHttpSession objects. This class turns
 * them back on, starts the real embedded server (which is what applies the session cookie's name and flags)
 * and, like a browser, carries nothing between requests but cookies.
 */
@SpringBootTest(webEnvironment = SpringBootTest.WebEnvironment.RANDOM_PORT,
        properties = "spring.autoconfigure.exclude=")
class JdbcSessionTests extends IntegrationTest {

    private static final String PASSWORD = "Session-Store-Check-7";
    private static final String CSRF = UUID.randomUUID().toString();

    @LocalServerPort
    int port;

    @Autowired
    JdbcClient jdbc;

    @Autowired
    PasswordEncoder passwords;

    @Autowired(required = false)
    JdbcIndexedSessionRepository sessions;

    private final HttpClient http = HttpClient.newHttpClient();
    private Long accountId;

    @AfterEach
    void removeAccount() {
        if (accountId != null) {
            jdbc.sql("DELETE FROM user_account WHERE id = :id").param("id", accountId).update();
        }
    }

    @Test
    @DisplayName("a sign-in is kept in the database, indexed by account id, and removed on sign-out")
    void aSignInLivesInTheDatabase() throws Exception {
        assertThat(sessions).as("database sessions are switched on in this context").isNotNull();
        String email = "session-" + UUID.randomUUID() + "@example.test";
        jdbc.sql("""
                        INSERT INTO user_account (email, password_hash, role, status, failed_logins, must_change_password,
                                                  password_changed_at, created_at, updated_at)
                        VALUES (:e, :h, 'SUPER_ADMIN', 'ACTIVE', 0, FALSE, :now, :now, :now)""")
                .param("e", email).param("h", passwords.encode(PASSWORD)).param("now", Timestamps.now()).update();
        accountId = jdbc.sql("SELECT id FROM user_account WHERE email = :e").param("e", email)
                .query(Long.class).single();

        HttpResponse<String> signIn = send(post("/api/v1/auth/login", "",
                "{\"email\":\"" + email + "\",\"password\":\"" + PASSWORD + "\"}"));
        assertThat(signIn.statusCode()).as(signIn.body()).isEqualTo(200);
        String setCookie = signIn.headers().allValues("Set-Cookie").stream()
                .filter(c -> c.startsWith("CCSESSION=")).findFirst().orElse(null);
        assertThat(setCookie).as("the session cookie keeps its configured name; got %s",
                signIn.headers().allValues("Set-Cookie")).isNotNull();
        assertThat(setCookie).as("the configured cookie flags").containsIgnoringCase("HttpOnly")
                .containsIgnoringCase("SameSite=Lax");
        String session = setCookie.substring(0, setCookie.indexOf(';'));

        // Only the cookie travels, as from a browser: the session must come back from the database.
        assertThat(send(get("/api/v1/public/session", session)).body()).contains("\"signedIn\":true");

        List<String> indexed = jdbc.sql("SELECT PRINCIPAL_NAME FROM SPRING_SESSION WHERE PRINCIPAL_NAME IN (:id, :email)")
                .param("id", accountId.toString()).param("email", email).query(String.class).list();
        assertThat(indexed).as("indexed by account id, never by email address").containsExactly(accountId.toString());

        List<byte[]> stored = jdbc.sql("""
                        SELECT a.ATTRIBUTE_BYTES FROM SPRING_SESSION_ATTRIBUTES a
                        JOIN SPRING_SESSION s ON s.PRIMARY_ID = a.SESSION_PRIMARY_ID
                        WHERE s.PRINCIPAL_NAME = :id""")
                .param("id", accountId.toString()).query(byte[].class).list();
        assertThat(stored).isNotEmpty();
        assertThat(stored).allSatisfy(bytes -> assertThat(new String(bytes, StandardCharsets.ISO_8859_1))
                .as("the password hash is erased before the session is stored").doesNotContain("$2a$"));

        HttpResponse<String> signOut = send(post("/api/v1/auth/logout", session, ""));
        assertThat(signOut.statusCode()).as(signOut.body()).isBetween(200, 299);

        assertThat(jdbc.sql("SELECT COUNT(*) FROM SPRING_SESSION WHERE PRINCIPAL_NAME = :id")
                .param("id", accountId.toString()).query(Integer.class).single())
                .as("signing out deletes the stored session").isZero();
        assertThat(send(get("/api/v1/public/session", session)).body()).contains("\"signedIn\":false");
    }

    private HttpRequest get(String path, String cookie) {
        return HttpRequest.newBuilder(uri(path)).header("Accept", "application/json").header("Cookie", cookie)
                .GET().build();
    }

    /** A POST with the double-submit CSRF pair the pages send: the same value as cookie and header. */
    private HttpRequest post(String path, String cookie, String json) {
        String cookies = cookie.isEmpty() ? "XSRF-TOKEN=" + CSRF : cookie + "; XSRF-TOKEN=" + CSRF;
        return HttpRequest.newBuilder(uri(path))
                .header("Accept", "application/json").header("Content-Type", "application/json")
                .header("Cookie", cookies).header("X-XSRF-TOKEN", CSRF)
                .POST(HttpRequest.BodyPublishers.ofString(json)).build();
    }

    private URI uri(String path) {
        return URI.create("http://localhost:" + port + path);
    }

    private HttpResponse<String> send(HttpRequest request) throws Exception {
        return http.send(request, HttpResponse.BodyHandlers.ofString());
    }
}
