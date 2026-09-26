package org.clevercubs.platform.web;

import org.springframework.http.HttpStatus;

/**
 * A failure the caller may be told about. The message is written for the user and must never contain
 * internal detail (SQL, stack traces, other people's data). Anything unexpected is not an ApiException and
 * becomes a generic 500 in {@link ApiExceptionHandler}.
 */
public class ApiException extends RuntimeException {

    private final HttpStatus status;
    private final String code;
    private final String field;

    public ApiException(HttpStatus status, String code, String userMessage) {
        this(status, code, userMessage, null);
    }

    private ApiException(HttpStatus status, String code, String userMessage, String field) {
        super(userMessage);
        this.status = status;
        this.code = code;
        this.field = field;
    }

    /** The request field the problem belongs to, so a form can show it beside the input; may be null. */
    public String field() {
        return field;
    }

    /** A 400 about one named field of the request body (for example a weak password or a taken username). */
    public static ApiException field(String code, String field, String userMessage) {
        return new ApiException(HttpStatus.BAD_REQUEST, code, userMessage, field);
    }

    /** The action is sensitive and the password was last proven too long ago (DD-02). */
    public static ApiException reauthRequired() {
        return new ApiException(HttpStatus.FORBIDDEN, "reauth-required",
                "Please confirm your password to continue.");
    }

    public static ApiException tooManyAttempts() {
        return new ApiException(HttpStatus.TOO_MANY_REQUESTS, "too-many-attempts",
                "Too many tries. Please wait a few minutes and try again.");
    }

    public HttpStatus status() {
        return status;
    }

    /** A stable, machine-readable reason, e.g. {@code quiz-locked}; clients branch on this, not on text. */
    public String code() {
        return code;
    }

    public static ApiException notFound(String what) {
        return new ApiException(HttpStatus.NOT_FOUND, "not-found", what + " was not found.");
    }

    public static ApiException forbidden() {
        return new ApiException(HttpStatus.FORBIDDEN, "forbidden", "You do not have access to this.");
    }

    /**
     * The account is signed in but is still using a password it did not choose — an admin-issued temporary
     * password (docs/04 §142). It may look at its own account, sign out, and change the password; nothing
     * else, until it has. The message says what happened and not how the caller got here, so an
     * unauthenticated caller cannot use it to find an account in this state — which is why the check is the
     * session's and never a parameter.
     */
    public static ApiException passwordChangeRequired() {
        return new ApiException(HttpStatus.FORBIDDEN, "password-change-required",
                "Choose a password of your own before using this account.");
    }

    public static ApiException conflict(String code, String userMessage) {
        return new ApiException(HttpStatus.CONFLICT, code, userMessage);
    }

    public static ApiException rule(String code, String userMessage) {
        return new ApiException(HttpStatus.UNPROCESSABLE_CONTENT, code, userMessage);
    }

    public static ApiException badRequest(String code, String userMessage) {
        return new ApiException(HttpStatus.BAD_REQUEST, code, userMessage);
    }
}
