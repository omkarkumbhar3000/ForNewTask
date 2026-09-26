package org.clevercubs.support;

import java.nio.file.Path;

import org.springframework.test.context.DynamicPropertyRegistry;
import org.testcontainers.mysql.MySQLContainer;
import org.testcontainers.utility.DockerImageName;
import org.testcontainers.utility.MountableFile;

/**
 * One real MySQL 8.4 for the whole test run, set up exactly like development: the same image and the same
 * user-creation script (../db/init/01-users.sh), so tests exercise the least-privilege cc_app user and the
 * Flyway grants rather than a superuser.
 */
public final class TestDatabase {

    public static final String MIGRATOR_PASSWORD = "migratorTestPw1";
    public static final String APP_PASSWORD = "appTestPw1";

    @SuppressWarnings("resource") // lives for the whole JVM; Testcontainers' Ryuk removes it afterwards
    private static final MySQLContainer MYSQL = new MySQLContainer(DockerImageName.parse("mysql:8.4"))
            .withDatabaseName("clevercubs")
            .withEnv("CC_DB_MIGRATOR_PASSWORD", MIGRATOR_PASSWORD)
            .withEnv("CC_DB_APP_PASSWORD", APP_PASSWORD)
            .withCommand("--character-set-server=utf8mb4", "--collation-server=utf8mb4_0900_ai_ci")
            .withCopyFileToContainer(
                    MountableFile.forHostPath(Path.of("..", "db", "init", "01-users.sh").toAbsolutePath(), 0755),
                    "/docker-entrypoint-initdb.d/01-users.sh");

    static {
        MYSQL.start();
    }

    private TestDatabase() {
    }

    public static String jdbcUrl() {
        return "jdbc:mysql://" + MYSQL.getHost() + ":" + MYSQL.getMappedPort(3306)
                + "/clevercubs?connectionTimeZone=UTC&forceConnectionTimeZoneToSession=true"
                + "&characterEncoding=UTF-8&allowPublicKeyRetrieval=true&sslMode=DISABLED";
    }

    /** Points the application at the container as cc_app, and Flyway as cc_migrator. */
    public static void register(DynamicPropertyRegistry registry) {
        registry.add("spring.datasource.url", TestDatabase::jdbcUrl);
        registry.add("spring.datasource.username", () -> "cc_app");
        registry.add("spring.datasource.password", () -> APP_PASSWORD);
        registry.add("spring.flyway.user", () -> "cc_migrator");
        registry.add("spring.flyway.password", () -> MIGRATOR_PASSWORD);
    }
}
