package org.clevercubs.platform.security;

import java.util.LinkedHashMap;
import java.util.List;

import jakarta.servlet.DispatcherType;

import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.http.HttpMethod;
import org.springframework.security.config.Customizer;
import org.springframework.security.config.annotation.web.builders.HttpSecurity;
import org.springframework.security.config.annotation.web.configuration.EnableWebSecurity;
import org.springframework.security.config.http.SessionCreationPolicy;
import org.springframework.security.crypto.bcrypt.BCryptPasswordEncoder;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.security.web.AuthenticationEntryPoint;
import org.springframework.security.web.SecurityFilterChain;
import org.springframework.security.web.access.AccessDeniedHandler;
import org.springframework.security.web.access.AccessDeniedHandlerImpl;
import org.springframework.security.web.access.RequestMatcherDelegatingAccessDeniedHandler;
import org.springframework.security.web.access.intercept.AuthorizationFilter;
import org.springframework.security.web.authentication.DelegatingAuthenticationEntryPoint;
import org.springframework.security.web.context.SecurityContextRepository;
import org.springframework.security.web.csrf.CookieCsrfTokenRepository;
import org.springframework.security.web.csrf.CsrfFilter;
import org.springframework.security.web.csrf.CsrfTokenRequestAttributeHandler;
import org.springframework.security.web.header.writers.ReferrerPolicyHeaderWriter.ReferrerPolicy;
import org.springframework.security.web.servlet.util.matcher.PathPatternRequestMatcher;
import org.springframework.security.web.util.matcher.RequestMatcher;
import org.springframework.security.web.util.matcher.RequestMatcherEntry;

/**
 * The one place access to the application is decided (docs/04-architecture-and-plan.md 4.1).
 *
 * <p>Design, unchanged from the approved Blueprint: the server session is the only source of identity
 * ({@link SessionAuthentication}), so the page routes themselves are protected on the server and logout
 * invalidates the session. HTTP Basic and form login are switched off deliberately, because either one
 * would make the browser send a credential on every request and would give the generated in-memory user
 * that Spring Boot otherwise creates.
 *
 * <p>Two different refusals, because the caller is a browser page or a fetch() call: an unauthenticated
 * API call gets {@code 401} problem+json, an unauthenticated page gets {@code 302 /login?next=…}, and the
 * wrong role always gets {@code 403}. Every rule below is an explicit allow; {@code anyRequest} requires
 * authentication, so a route added later is closed until someone opens it on purpose.
 */
@Configuration
@EnableWebSecurity
public class SecurityConfig {

    /** The JSON API. Anything under here answers with problem+json, never with a redirect. */
    private static final String API = "/api/**";

    /** Pages anyone may open: the welcome page, sign-in, registration and the information pages. */
    private static final String[] PUBLIC_PAGES = {
        "/", "/register", "/terms", "/privacy", "/contact", "/*.html", "/favicon.ico", "/favicon.svg"};

    /** A wrong role on the API is problem+json; on a page it is the friendly HTML 403 page. */
    private static AccessDeniedHandler accessDenied(ApiProblemEntryPoint apiRefusals) {
        AccessDeniedHandlerImpl pages = new AccessDeniedHandlerImpl();
        pages.setErrorPage("/403.html");
        LinkedHashMap<RequestMatcher, AccessDeniedHandler> byPath = new LinkedHashMap<>();
        byPath.put(matcher(API), apiRefusals);
        return new RequestMatcherDelegatingAccessDeniedHandler(byPath, pages);
    }

    @Bean
    SecurityFilterChain applicationSecurity(HttpSecurity http, ApiProblemEntryPoint apiRefusals,
            LoginRedirectEntryPoint loginRedirect, SecurityContextRepository sessions) throws Exception {

        // DD-03: the token travels in the X-XSRF-TOKEN header, which is the name
        // CookieCsrfTokenRepository already reads, so the cookie is left readable by the fetch wrapper. The
        // cookie is not HttpOnly for that reason alone; it is not a credential and grants no access itself.
        CookieCsrfTokenRepository csrf = CookieCsrfTokenRepository.withHttpOnlyFalse();
        csrf.setCookiePath("/");
        CsrfTokenRequestAttributeHandler csrfHandler = new CsrfTokenRequestAttributeHandler();

        // An API call is refused with 401; a page is sent to the login form. Chosen by path, not by
        // Accept, so a browser fetching JSON is never handed an HTML page it cannot parse. The login
        // redirect is the default, and the single "/api/**" entry is tested first.
        DelegatingAuthenticationEntryPoint entryPoint = new DelegatingAuthenticationEntryPoint(loginRedirect,
                List.of(new RequestMatcherEntry<>(matcher(API), apiRefusals)));

        http
            // No HTTP Basic, no form login, no default logout redirect: the JSON API in B1 owns all three.
            .httpBasic(basic -> basic.disable())
            .formLogin(form -> form.disable())
            .logout(logout -> logout.disable())
            .anonymous(Customizer.withDefaults())
            .securityContext(context -> context.securityContextRepository(sessions))
            .sessionManagement(session -> session
                    .sessionCreationPolicy(SessionCreationPolicy.IF_REQUIRED)
                    .sessionFixation(fixation -> fixation.changeSessionId()))
            .requestCache(Customizer.withDefaults())
                    .csrf(csrfConfig -> csrfConfig
                            .csrfTokenRepository(csrf)
                            .csrfTokenRequestHandler(csrfHandler))
                    // The token is resolved on every request, so the cookie is issued with the page that a
                    // browser loads and its first POST is not refused for want of a token it never received.
                    .addFilterAfter(new CsrfCookieIssuingFilter(), CsrfFilter.class)
                    // After the decision, so it can only narrow it: an account still on a temporary password
                    // reaches its own account and nothing else until the password is changed.
                    .addFilterAfter(new PasswordChangeRequiredFilter(apiRefusals), AuthorizationFilter.class)
            .headers(headers -> headers
                    // DD-11. No 'unsafe-inline' and no third-party origin: the pages ship their own CSS and
                    // JS, and nothing is loaded from a CDN at runtime (DD-12).
                    .contentSecurityPolicy(csp -> csp.policyDirectives(
                            "default-src 'self'; base-uri 'self'; form-action 'self'; frame-ancestors 'none';"
                            + " object-src 'none'; script-src 'self'; style-src 'self'; img-src 'self' data:;"
                            + " media-src 'self'; font-src 'self'"))
                    .frameOptions(frame -> frame.deny())
                    .referrerPolicy(referrer -> referrer.policy(ReferrerPolicy.SAME_ORIGIN))
                    .contentTypeOptions(Customizer.withDefaults()))
            .exceptionHandling(exceptions -> exceptions
                    .authenticationEntryPoint(entryPoint)
                    .accessDeniedHandler(accessDenied(apiRefusals)))
            .authorizeHttpRequests(auth -> auth
                    // Internal forwards (a clean URL to its .html file) and error dispatches were already
                    // authorised as the request the browser made; checking them again adds nothing.
                    .dispatcherTypeMatchers(DispatcherType.FORWARD, DispatcherType.ERROR).permitAll()

                    // --- open to everyone, by name, and nothing else ---
                    .requestMatchers(HttpMethod.OPTIONS, "/**").permitAll()
                    .requestMatchers("/api/v1/public/**").permitAll()
                    .requestMatchers("/login").permitAll()
                    .requestMatchers(HttpMethod.GET, PUBLIC_PAGES).permitAll()
                    .requestMatchers(HttpMethod.GET, "/css/**", "/js/**", "/img/**", "/fonts/**").permitAll()
                    .requestMatchers(HttpMethod.POST, "/api/v1/auth/register", "/api/v1/auth/login").permitAll()

                    // --- the signed-in account itself ---
                    .requestMatchers("/api/v1/auth/**").authenticated()

                    // --- switching between the parent and the child (D58) ---
                    .requestMatchers("/api/v1/session/child").hasRole(Role.PARENT.name())
                    .requestMatchers("/api/v1/session/parent").hasRole(Role.CHILD.name())

                    // --- course media: any signed-in session, never strangers ---
                    .requestMatchers(HttpMethod.GET, "/media/**").authenticated()

                    // --- one role per area. Child mode drops ROLE_PARENT, so a child cannot reach
                    //     /parent/** or /admin/** even though the account is a parent's (D58). ---
                    .requestMatchers("/api/v1/parent/**", "/parent/**").hasRole(Role.PARENT.name())
                    .requestMatchers("/api/v1/learn/**", "/learn/**").hasRole(Role.CHILD.name())
                    .requestMatchers("/api/v1/admin/**", "/admin/**").hasRole(Role.SUPER_ADMIN.name())

                    // Default deny: static files, the media library and anything added later stay closed
                    // until a rule above opens them.
                    .anyRequest().authenticated());

        return http.build();
    }

    /**
     * BCrypt at cost 12 (DD-01): never a plain or reversible encoding. A hash records its own cost, so hashes
     * made at an earlier cost still verify. The cost is configurable only so the test suite can run fast.
     */
    @Bean
    PasswordEncoder passwordEncoder(
            @org.springframework.beans.factory.annotation.Value("${clevercubs.security.bcrypt-strength:12}")
            int strength) {
        return new BCryptPasswordEncoder(strength);
    }

    private static RequestMatcher matcher(String pattern) {
        return PathPatternRequestMatcher.withDefaults().matcher(pattern);
    }
}
