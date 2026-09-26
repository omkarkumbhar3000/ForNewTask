package org.clevercubs.platform.security;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.security.authentication.AuthenticationManager;
import org.springframework.security.authentication.ProviderManager;
import org.springframework.security.web.authentication.logout.CompositeLogoutHandler;
import org.springframework.security.web.authentication.logout.CookieClearingLogoutHandler;
import org.springframework.security.web.authentication.logout.LogoutHandler;
import org.springframework.security.web.authentication.logout.SecurityContextLogoutHandler;
import org.springframework.security.web.context.HttpSessionSecurityContextRepository;
import org.springframework.security.web.context.SecurityContextRepository;

/**
 * The plumbing the JSON API signs in with, kept beside {@link SecurityConfig} so the filter chain and the
 * sign-in endpoint cannot drift apart: both use the same {@link SecurityContextRepository} instance and so
 * write the same session attribute.
 *
 * <p>The {@link AuthenticationManager} is declared explicitly, which is deliberate. Left to itself Spring
 * Boot builds one from whatever authentication components it finds, and it also offers a generated in-memory
 * user with a printed password; {@code CleverCubsApplication} excludes that auto-configuration, so the only
 * way to authenticate is {@link AccountAuthenticationProvider} against {@code user_account}.
 */
@Configuration
public class AuthenticationConfig {

    /** The server session is the only place a signed-in identity is kept (DD-02). */
    @Bean
    SecurityContextRepository securityContextRepository() {
        return new HttpSessionSecurityContextRepository();
    }

    /**
     * Signing out is the framework's own work: invalidate the session and clear the context, then tell the
     * browser to drop the session cookie. The cookie name is read from configuration, not repeated here.
     */
    @Bean
    LogoutHandler authenticationLogoutHandler(
            @Value("${server.servlet.session.cookie.name}") String sessionCookieName) {
        return new CompositeLogoutHandler(
                new SecurityContextLogoutHandler(),
                new CookieClearingLogoutHandler(sessionCookieName));
    }

    @Bean
    AuthenticationManager authenticationManager(AccountAuthenticationProvider provider) {
        return new ProviderManager(provider);
    }
}
