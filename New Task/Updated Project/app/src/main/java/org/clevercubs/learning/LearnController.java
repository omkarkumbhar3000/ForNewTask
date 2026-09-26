package org.clevercubs.learning;

import java.util.List;
import java.util.Map;

import jakarta.validation.Valid;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotNull;
import jakarta.validation.constraints.Size;

import org.clevercubs.child.ChildService;
import org.clevercubs.child.ChildService.ChildView;
import org.clevercubs.family.RequestService;
import org.clevercubs.family.RequestService.RequestView;
import org.clevercubs.learning.LearningService.CourseView;
import org.clevercubs.learning.LearningService.Home;
import org.clevercubs.learning.LearningService.LessonView;
import org.clevercubs.learning.LearningService.ViewResult;
import org.clevercubs.learning.ProgressService.CourseProgress;
import org.clevercubs.platform.security.CurrentUser;
import org.clevercubs.quiz.QuizService;
import org.clevercubs.quiz.QuizService.AnswerResult;
import org.clevercubs.quiz.QuizService.AttemptView;
import org.clevercubs.reward.RewardService;
import org.clevercubs.reward.RewardService.BadgeView;
import org.clevercubs.reward.RewardService.CertificateView;
import org.springframework.http.HttpStatus;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.PutMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.ResponseStatus;
import org.springframework.web.bind.annotation.RestController;

/**
 * The child's API (child mode only, D58). The child is always the session's active child, re-checked
 * against the signed-in parent account on every call; no endpoint accepts a child id.
 */
@RestController
@RequestMapping("/api/v1/learn")
class LearnController {

    record AnswerRequest(@NotNull(message = "required") Long optionId) {
    }

    record ChildRequest(@NotBlank(message = "required") @Size(max = 20) String type, Long quizId,
            @Size(max = 40, message = "is too long") String requestedValue) {
    }

    record Profile(ChildView child, List<CourseProgress> courses, List<BadgeView> badges,
            List<CertificateView> certificates, List<RequestView> requests) {
    }

    private final CurrentUser currentUser;
    private final ChildService children;
    private final LearningService learning;
    private final QuizService quizzes;
    private final RewardService rewards;
    private final RequestService requests;
    private final ProgressService progress;

    LearnController(CurrentUser currentUser, ChildService children, LearningService learning, QuizService quizzes,
            RewardService rewards, RequestService requests, ProgressService progress) {
        this.currentUser = currentUser;
        this.children = children;
        this.learning = learning;
        this.quizzes = quizzes;
        this.rewards = rewards;
        this.requests = requests;
        this.progress = progress;
    }

    /** The active child, confirmed to belong to the signed-in parent. */
    private long child() {
        long childId = currentUser.activeChildId();
        children.requireOwned(currentUser.accountId(), childId);
        return childId;
    }

    @GetMapping("/me")
    ChildView me() {
        return children.view(learning.child(child()));
    }

    @GetMapping("/home")
    Home home() {
        return learning.home(child());
    }

    @GetMapping("/courses/{slug}")
    CourseView course(@PathVariable String slug) {
        return learning.course(child(), slug);
    }

    @GetMapping("/lessons/{id}")
    LessonView lesson(@PathVariable long id) {
        return learning.lesson(child(), id);
    }

    @PutMapping("/items/{id}/view")
    ViewResult view(@PathVariable long id) {
        return learning.viewItem(child(), id);
    }

    @GetMapping("/quizzes/{id}")
    QuizService.QuizOverview quiz(@PathVariable long id) {
        return quizzes.overview(child(), id);
    }

    @PostMapping("/quizzes/{id}/attempts")
    AttemptView startQuiz(@PathVariable long id) {
        return quizzes.start(child(), id);
    }

    @GetMapping("/attempts/{id}")
    AttemptView attempt(@PathVariable long id) {
        return quizzes.view(child(), id);
    }

    @PutMapping("/attempts/{id}/answers/{questionId}")
    AnswerResult answer(@PathVariable long id, @PathVariable long questionId,
            @Valid @RequestBody AnswerRequest body) {
        return quizzes.answer(child(), id, questionId, body.optionId());
    }

    @GetMapping("/profile")
    Profile profile() {
        long childId = child();
        return new Profile(children.view(learning.child(childId)), List.copyOf(progress.forChild(childId).values()),
                rewards.badgesOf(childId), rewards.certificatesOf(childId), requests.forChild(childId));
    }

    @PostMapping("/requests")
    @ResponseStatus(HttpStatus.CREATED)
    RequestView ask(@Valid @RequestBody ChildRequest body) {
        return requests.create(child(), body.type(), body.quizId(), body.requestedValue());
    }

    @GetMapping("/requests")
    List<RequestView> myRequests() {
        return requests.forChild(child());
    }

    @GetMapping("/avatars")
    Map<String, String> avatars() {
        return org.clevercubs.child.Avatars.all();
    }
}
