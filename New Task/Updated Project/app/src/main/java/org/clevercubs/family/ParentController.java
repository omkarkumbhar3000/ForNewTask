package org.clevercubs.family;

import java.time.LocalDate;
import java.util.List;
import java.util.Map;

import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;
import jakarta.validation.Valid;
import jakarta.validation.constraints.Max;
import jakarta.validation.constraints.Min;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotNull;
import jakarta.validation.constraints.Pattern;
import jakarta.validation.constraints.Size;

import org.clevercubs.child.ChildService;
import org.clevercubs.child.ChildService.ChildInput;
import org.clevercubs.child.ChildService.ChildUpdate;
import org.clevercubs.child.ChildService.ChildView;
import org.clevercubs.family.ParentService.Account;
import org.clevercubs.family.ParentService.ChildReport;
import org.clevercubs.family.ParentService.Overview;
import org.clevercubs.family.ParentService.YearSummary;
import org.clevercubs.family.RequestService.RequestView;
import org.clevercubs.feedback.FeedbackService;
import org.clevercubs.feedback.FeedbackService.FeedbackView;
import org.clevercubs.platform.security.CurrentUser;
import org.clevercubs.platform.security.RecentAuthentication;
import org.clevercubs.platform.security.Role;
import org.clevercubs.platform.web.ApiException;
import org.springframework.http.HttpHeaders;
import org.springframework.http.HttpStatus;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.security.web.authentication.logout.LogoutHandler;
import org.springframework.web.bind.annotation.DeleteMapping;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PatchMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

/**
 * The parent's API. The account is always the session's; every child id in a path is checked to belong to
 * it (a child of another family is "not found"). Deleting and exporting data need a recent password.
 */
@RestController
@RequestMapping("/api/v1/parent")
class ParentController {

    record NewChild(@NotBlank(message = "required") @Size(max = 40, message = "is too long") String firstName,
            @Size(max = 40, message = "is too long") String displayName,
            @NotNull(message = "required") LocalDate dateOfBirth,
            @Size(max = 20, message = "is too long") String username,
            @Size(max = 30) String avatarCode) {
    }

    record ChildChanges(@Size(max = 40, message = "is too long") String displayName,
            @Size(max = 20, message = "is too long") String username, @Size(max = 30) String avatarCode,
            LocalDate dateOfBirth, Boolean soundEffects, Boolean readAloud) {
    }

    record Decision(@NotBlank(message = "required") String decision) {
    }

    record NewFeedback(@NotBlank(message = "required") String category, Long courseId,
            @Min(value = 1, message = "must be 1 to 5") @Max(value = 5, message = "must be 1 to 5") Integer rating,
            @NotBlank(message = "required") @Size(max = 2000, message = "is too long") String message) {
    }

    record AccountChanges(@NotBlank(message = "required") @Size(max = 100, message = "is too long") String fullName,
            @Size(max = 20, message = "is too long")
            @Pattern(regexp = "^$|^[+0-9 ()-]{6,20}$", message = "must be a phone number") String mobile,
            @Size(max = 80, message = "is too long") String city) {
    }

    private final CurrentUser currentUser;
    private final ParentService parents;
    private final ChildService children;
    private final RequestService requests;
    private final FeedbackService feedback;
    private final RecentAuthentication recent;
    private final LogoutHandler logoutHandler;

    ParentController(CurrentUser currentUser, ParentService parents, ChildService children,
            RequestService requests, FeedbackService feedback, RecentAuthentication recent,
            LogoutHandler logoutHandler) {
        this.currentUser = currentUser;
        this.parents = parents;
        this.children = children;
        this.requests = requests;
        this.feedback = feedback;
        this.recent = recent;
        this.logoutHandler = logoutHandler;
    }

    private long account() {
        currentUser.requireMode(Role.PARENT);
        return currentUser.accountId();
    }

    @GetMapping("/overview")
    Overview overview() {
        return parents.overview(account());
    }

    @GetMapping("/children")
    List<ChildView> children() {
        return children.forAccount(account()).stream().map(children::view).toList();
    }

    @PostMapping("/children")
    ResponseEntity<ChildView> addChild(@Valid @RequestBody NewChild body) {
        long accountId = account();
        long parentId = children.parentIdOf(accountId).orElseThrow(() -> ApiException.notFound("Parent"));
        long childId = children.create(parentId, new ChildInput(body.firstName(), body.displayName(),
                body.dateOfBirth(), body.username(), body.avatarCode()));
        return ResponseEntity.status(HttpStatus.CREATED)
                .body(children.view(children.requireOwned(accountId, childId)));
    }

    @GetMapping("/children/{id}")
    ChildReport child(@PathVariable long id) {
        return parents.report(account(), id);
    }

    @PatchMapping("/children/{id}")
    ChildView updateChild(@PathVariable long id, @Valid @RequestBody ChildChanges body) {
        long accountId = account();
        children.requireOwned(accountId, id);
        children.update(id, new ChildUpdate(body.displayName(), body.username(), body.avatarCode(),
                body.dateOfBirth(), body.soundEffects(), body.readAloud()));
        return children.view(children.requireOwned(accountId, id));
    }

    @DeleteMapping("/children/{id}")
    ResponseEntity<Void> deleteChild(@PathVariable long id, HttpServletRequest request) {
        long accountId = account();
        recent.require(request);
        parents.deleteChild(accountId, id);
        return ResponseEntity.noContent().build();
    }

    @GetMapping("/children/{id}/year-summary")
    YearSummary yearSummary(@PathVariable long id) {
        return parents.yearSummary(account(), id);
    }

    @PostMapping("/children/{id}/next-year")
    YearSummary nextYear(@PathVariable long id, @Valid @RequestBody Decision body) {
        return parents.decideNextYear(account(), id, body.decision());
    }

    @GetMapping("/children/{id}/export")
    ResponseEntity<Map<String, Object>> export(@PathVariable long id, HttpServletRequest request) {
        long accountId = account();
        recent.require(request);
        return ResponseEntity.ok()
                .header(HttpHeaders.CONTENT_DISPOSITION, "attachment; filename=\"clevercubs-child-" + id + ".json\"")
                .contentType(MediaType.APPLICATION_JSON)
                .body(parents.export(accountId, id));
    }

    @PostMapping("/children/{id}/quizzes/{quizId}/grant")
    ResponseEntity<Void> grant(@PathVariable long id, @PathVariable long quizId) {
        requests.grant(account(), id, quizId);
        return ResponseEntity.noContent().build();
    }

    @GetMapping("/requests")
    List<RequestView> requests(@RequestParam(defaultValue = "false") boolean pending) {
        return requests.forParent(account(), pending);
    }

    @PostMapping("/requests/{id}/approve")
    RequestView approve(@PathVariable long id) {
        return requests.approve(account(), id);
    }

    @PostMapping("/requests/{id}/decline")
    RequestView decline(@PathVariable long id) {
        return requests.decline(account(), id);
    }

    @PostMapping("/feedback")
    ResponseEntity<FeedbackView> feedback(@Valid @RequestBody NewFeedback body) {
        return ResponseEntity.status(HttpStatus.CREATED).body(
                feedback.submit(account(), body.category(), body.courseId(), body.rating(), body.message()));
    }

    @GetMapping("/feedback")
    List<FeedbackView> myFeedback() {
        return feedback.ownFeedback(account());
    }

    @GetMapping("/account")
    Account accountDetails() {
        return parents.account(account());
    }

    @PatchMapping("/account")
    Account updateAccount(@Valid @RequestBody AccountChanges body) {
        return parents.updateAccount(account(), body.fullName(), body.mobile(), body.city());
    }

    /** Deletes the account and all its children's data, then signs out (D67). */
    @DeleteMapping("/account")
    ResponseEntity<Void> deleteAccount(HttpServletRequest request, HttpServletResponse response) {
        long accountId = account();
        recent.require(request);
        parents.deleteAccount(accountId);
        logoutHandler.logout(request, response, currentUser.session());
        return ResponseEntity.noContent().build();
    }
}
