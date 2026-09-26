package org.clevercubs;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.boot.context.properties.ConfigurationPropertiesScan;
import org.springframework.boot.security.autoconfigure.UserDetailsServiceAutoConfiguration;

/**
 * CleverCubs: a secure, child-friendly early-learning application.
 *
 * <p>Architecture: docs/04-architecture-and-plan.md. Packages are organised by feature (account, child,
 * content, learning, quiz, reward, family, feedback, admin, audit); cross-cutting concerns live in
 * {@code platform}.
 *
 * <p>{@link UserDetailsServiceAutoConfiguration} is excluded on purpose. Left in, Spring Boot creates an
 * in-memory user with a generated password and prints it at startup, which would be a second way into the
 * application beside {@code user_account} and could be re-enabled by a stray annotation later. Accounts come
 * from the database through {@code AccountAuthenticationProvider} and nowhere else.
 */
@SpringBootApplication(exclude = UserDetailsServiceAutoConfiguration.class)
@ConfigurationPropertiesScan
public class CleverCubsApplication {

    public static void main(String[] args) {
        SpringApplication.run(CleverCubsApplication.class, args);
    }
}
