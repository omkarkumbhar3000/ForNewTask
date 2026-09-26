package org.clevercubs.platform.web;

import java.net.URI;
import java.util.List;
import java.util.Map;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.core.Ordered;
import org.springframework.core.annotation.Order;
import org.springframework.http.HttpStatus;
import org.springframework.http.ProblemDetail;
import org.springframework.http.converter.HttpMessageNotReadableException;
import org.springframework.security.access.AccessDeniedException;
import org.springframework.security.core.AuthenticationException;
import org.springframework.web.HttpMediaTypeNotSupportedException;
import org.springframework.web.HttpRequestMethodNotSupportedException;
import org.springframework.web.bind.MethodArgumentNotValidException;
import org.springframework.web.bind.annotation.ExceptionHandler;
import org.springframework.web.bind.annotation.RestControllerAdvice;
import org.springframework.web.method.annotation.MethodArgumentTypeMismatchException;
import org.springframework.web.servlet.resource.NoResourceFoundException;

/**
 * Turns every failure into RFC 9457 problem+json with a stable {@code code} and a user-safe message.
 * Internal detail goes to the server log only (fixes SEC-E06 and SEC-E11). Validation errors name the
 * field and the rule, never echo the rejected value.
 *
 * <p>The order matters. Spring Boot auto-configures its own {@code ProblemDetailsExceptionHandler}, which
 * answers most of the same exceptions with a correct problem body that has no {@code code} in it. A client
 * that branches on {@code code} — as the API contract says it must — would then have nowhere to branch on
 * for a rejected sign-in. This advice is therefore consulted first, and Boot's handler stays behind it as
 * the backstop for anything not named here.
 */
@Order(Ordered.HIGHEST_PRECEDENCE)
@RestControllerAdvice
public class ApiExceptionHandler {

    private static final Logger log = LoggerFactory.getLogger(ApiExceptionHandler.class);

    @ExceptionHandler(ApiException.class)
    ProblemDetail api(ApiException e) {
        ProblemDetail p = problem(e.status(), e.code(), e.getMessage());
        if (e.field() != null) {
            p.setProperty("fields", List.of(Map.of("field", e.field(), "message", e.getMessage())));
        }
        return p;
    }

    /** Rows that already exist (a taken email or username raced past the service check) are a 409. */
    @ExceptionHandler(org.springframework.dao.DuplicateKeyException.class)
    ProblemDetail duplicate(org.springframework.dao.DuplicateKeyException e) {
        log.info("Duplicate key: {}", e.getMostSpecificCause().getMessage());
        return problem(HttpStatus.CONFLICT, "already-exists", "That is already taken. Please choose another.");
    }

    @ExceptionHandler(MethodArgumentNotValidException.class)
    ProblemDetail invalid(MethodArgumentNotValidException e) {
        List<Map<String, String>> fields = e.getBindingResult().getFieldErrors().stream()
                .map(f -> Map.of("field", f.getField(), "message", String.valueOf(f.getDefaultMessage())))
                .toList();
        ProblemDetail p = problem(HttpStatus.BAD_REQUEST, "invalid-input", "Some details need another look.");
        p.setProperty("fields", fields);
        return p;
    }

    @ExceptionHandler({HttpMessageNotReadableException.class, MethodArgumentTypeMismatchException.class})
    ProblemDetail unreadable(Exception e) {
        return problem(HttpStatus.BAD_REQUEST, "invalid-input", "The request could not be read.");
    }

    @ExceptionHandler(HttpRequestMethodNotSupportedException.class)
    ProblemDetail method(HttpRequestMethodNotSupportedException e) {
        return problem(HttpStatus.METHOD_NOT_ALLOWED, "method-not-allowed", "This action is not supported here.");
    }

    @ExceptionHandler(HttpMediaTypeNotSupportedException.class)
    ProblemDetail mediaType(HttpMediaTypeNotSupportedException e) {
        return problem(HttpStatus.UNSUPPORTED_MEDIA_TYPE, "unsupported-media-type", "Send the request as JSON.");
    }

    /**
     * A missing API resource is problem+json; a missing page gets the friendly HTML 404 page instead, so a
     * child who follows an old link sees a way home rather than raw JSON.
     */
    @ExceptionHandler(NoResourceFoundException.class)
    Object noResource(NoResourceFoundException e, jakarta.servlet.http.HttpServletRequest request) {
        String path = request.getRequestURI();
        if (!path.startsWith("/api/") && !path.startsWith("/media/")) {
            var page = new org.springframework.core.io.ClassPathResource("static/404.html");
            if (page.exists()) {
                return org.springframework.http.ResponseEntity.status(HttpStatus.NOT_FOUND)
                        .contentType(org.springframework.http.MediaType.TEXT_HTML)
                        .body(page);
            }
        }
        return problem(HttpStatus.NOT_FOUND, "not-found", "This page or file does not exist.");
    }

    @ExceptionHandler(AccessDeniedException.class)
    ProblemDetail denied(AccessDeniedException e) {
        return problem(HttpStatus.FORBIDDEN, "forbidden", "You do not have access to this.");
    }

    @ExceptionHandler(AuthenticationException.class)
    ProblemDetail unauthenticated(AuthenticationException e) {
        return problem(HttpStatus.UNAUTHORIZED, "unauthenticated", "Please sign in.");
    }

    @ExceptionHandler(Exception.class)
    ProblemDetail unexpected(Exception e) {
        log.error("Unhandled error", e);
        return problem(HttpStatus.INTERNAL_SERVER_ERROR, "server-error",
                "Something went wrong on our side. Please try again.");
    }

    public static ProblemDetail problem(HttpStatus status, String code, String message) {
        ProblemDetail p = ProblemDetail.forStatusAndDetail(status, message);
        p.setType(URI.create("urn:clevercubs:problem:" + code));
        p.setTitle(status.getReasonPhrase());
        p.setProperty("code", code);
        return p;
    }
}
