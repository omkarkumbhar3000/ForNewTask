package org.clevercubs.platform.security;

import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;

import java.io.IOException;

import org.clevercubs.platform.web.ApiException;
import org.clevercubs.platform.web.ApiExceptionHandler;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.http.HttpStatus;
import org.springframework.http.MediaType;
import org.springframework.http.ProblemDetail;
import org.springframework.security.access.AccessDeniedException;
import org.springframework.security.core.AuthenticationException;
import org.springframework.security.web.AuthenticationEntryPoint;
import org.springframework.security.web.access.AccessDeniedHandler;
import org.springframework.stereotype.Component;
import tools.jackson.databind.ObjectMapper;

/**
 * Answers an unauthenticated or forbidden call to the JSON API with RFC 9457 problem+json, never an HTML
 * redirect, so a fetch() call in the browser receives a status it can branch on instead of a login page
 * (requirement 8; docs/04-architecture-and-plan.md 4.1).
 *
 * <p>This runs inside the filter chain, before any {@code @RestControllerAdvice}, so it builds the body
 * itself. It reuses {@link ApiExceptionHandler#problem} so the shape, the {@code type} URN and the stable
 * {@code code} are identical to every other error the API returns.
 *
 * <p>Nothing about the caller, the session or the reason for the refusal is disclosed in the body. The
 * message is deliberately generic, so it cannot reveal whether an account exists (SEC-E07, SEC-E08). The
 * cause is written to the server log only (SEC-E06, SEC-E11).
 */
@Component
public class ApiProblemEntryPoint implements AuthenticationEntryPoint, AccessDeniedHandler {

    private static final Logger log = LoggerFactory.getLogger(ApiProblemEntryPoint.class);

    private final ObjectMapper json;

    public ApiProblemEntryPoint(ObjectMapper json) {
        this.json = json;
    }

    @Override
    public void commence(HttpServletRequest request, HttpServletResponse response, AuthenticationException e)
            throws IOException {
        log.info("Unauthenticated API call to {}: {}", request.getRequestURI(), e.getMessage());
        write(response, HttpStatus.UNAUTHORIZED, "unauthenticated", "Please sign in.");
    }

    @Override
    public void handle(HttpServletRequest request, HttpServletResponse response, AccessDeniedException exception)
            throws IOException {
        log.info("Forbidden API call to {}: {}", request.getRequestURI(), exception.getMessage());
        write(response, HttpStatus.FORBIDDEN, "forbidden", "You do not have access to this.");
    }

    /**
     * Writes any refusal the same way, from inside the filter chain where no advice runs. Used by the
     * filters that have to refuse a request themselves, so a refusal from a filter is indistinguishable in
     * shape from one from a controller.
     */
    void write(HttpServletResponse response, ApiException refusal) throws IOException {
        write(response, refusal.status(), refusal.code(), refusal.getMessage());
    }

    void write(HttpServletResponse response, HttpStatus status, String code, String message)
            throws IOException {
        ProblemDetail problem = ApiExceptionHandler.problem(status, code, message);
        response.setStatus(status.value());
        response.setContentType(MediaType.APPLICATION_PROBLEM_JSON_VALUE);
        response.setCharacterEncoding("UTF-8");
        json.writeValue(response.getOutputStream(), problem);
    }
}
