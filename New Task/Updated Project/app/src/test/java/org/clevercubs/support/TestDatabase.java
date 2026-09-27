package org.clevercubs.support;

import java.nio.file.Path;

import org.springframework.test.context.DynamicPropertyRegistry;
import org.testcontainers.containers.JdbcDatabaseContainer;
import org.testcontainers.mysql.MySQLContainer;
import org.testcontainers.postgresql.PostgreSQLContainer;
import org.testcontainers.utility.DockerImageName;
import org.testcontainers.utility.MountableFile;

/**
 * One real database for the whole test run. By default MySQL 8.4, set up exactly like development: the same
 * image and the same user-creation script (../db/init/01-users.sh), so tests exercise the least-privilege
 * cc_app user and the Flyway grants rather than a superuser.
 *
 * <p>{@code mvnw test -Dclevercubs.test.db=postgresql} runs the same suite on PostgreSQL 17, the database of
 * the hosted deployment (D73). There the schema owner is cc_migrator and the Flyway callback creates cc_app,
 * as it does on the host.
 */
public final class TestDatabase {

    public static final String MIGRATOR_PASSWORD = "migratorTestPassword-1";
    /** At least 16 characters: the PostgreSQL callback refuses a shorter one. */
    public static final String APP_PASSWORD = "appTestPassword-0001";

    public static final boolean POSTGRES =
            "postgresql".equalsIgnoreCase(System.getProperty("clevercubs.test.db", "mysql").trim());

    @SuppressWarnings("resource") // lives for the whole JVM; Testcontainers' Ryuk removes it afterwards
    private static final JdbcDatabaseContainer<?> DATABASE = POSTGRES ? postgres() : mysql();

    static {
        DATABASE.start();
    }

    private TestDatabase() {
    }

    private static MySQLContainer mysql() {
        return new MySQLContainer(DockerImageName.parse("mysql:8.4"))
                .withDatabaseName("clevercubs")
                .withEnv("CC_DB_MIGRATOR_PASSWORD", MIGRATOR_PASSWORD)
                .withEnv("CC_DB_APP_PASSWORD", APP_PASSWORD)
                .withCommand("--character-set-server=utf8mb4", "--collation-server=utf8mb4_0900_ai_ci")
                .withCopyFileToContainer(
                        MountableFile.forHostPath(Path.of("..", "db", "init", "01-users.sh").toAbsolutePath(), 0755),
                        "/docker-entrypoint-initdb.d/01-users.sh");
    }

    private static PostgreSQLContainer postgres() {
        return new PostgreSQLContainer(DockerImageName.parse("postgres:17-alpine"))
                .withDatabaseName("clevercubs")
                .withUsername("cc_migrator")
                .withPassword(MIGRATOR_PASSWORD);
    }

    public static String jdbcUrl() {
        if (POSTGRES) {
            return "jdbc:postgresql://" + DATABASE.getHost() + ":" + DATABASE.getMappedPort(5432) + "/clevercubs";
        }
        return "jdbc:mysql://" + DATABASE.getHost() + ":" + DATABASE.getMappedPort(3306)
                + "/clevercubs?connectionTimeZone=UTC&forceConnectionTimeZoneToSession=true"
                + "&characterEncoding=UTF-8&allowPublicKeyRetrieval=true&sslMode=DISABLED";
    }

    /** The schema that holds the application tables: the database itself on MySQL, "public" on PostgreSQL. */
    public static String schema() {
        return POSTGRES ? "public" : "clevercubs";
    }

    /** Points the application at the container as cc_app, and Flyway as cc_migrator. */
    public static void register(DynamicPropertyRegistry registry) {
        registry.add("spring.datasource.url", TestDatabase::jdbcUrl);
        registry.add("spring.datasource.username", () -> "cc_app");
        registry.add("spring.datasource.password", () -> APP_PASSWORD);
        registry.add("spring.flyway.user", () -> "cc_migrator");
        registry.add("spring.flyway.password", () -> MIGRATOR_PASSWORD);
        registry.add("spring.flyway.placeholders.appPassword", () -> APP_PASSWORD);
    }
}
