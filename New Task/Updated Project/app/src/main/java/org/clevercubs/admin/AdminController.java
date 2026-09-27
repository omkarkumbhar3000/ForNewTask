package org.clevercubs.admin;

import java.util.List;
import java.util.Map;

import jakarta.servlet.http.HttpServletRequest;
import jakarta.validation.Valid;
import jakarta.validation.constraints.Email;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotNull;
import jakarta.validation.constraints.Size;

import org.clevercubs.child.ChildService;
import org.clevercubs.family.ParentService;
import org.clevercubs.family.ParentService.ChildReport;
import org.clevercubs.feedback.FeedbackService;
import org.clevercubs.feedback.FeedbackService.FeedbackView;
import org.clevercubs.platform.security.CurrentUser;
import org.clevercubs.platform.security.RecentAuthentication;
import org.clevercubs.platform.security.Role;
import org.clevercubs.platform.web.ApiException;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PatchMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.PutMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

/**
 * The Super Admin API (requirement section 19). Being signed in is not enough: every call requires the
 * SUPER_ADMIN role (SecurityConfig and {@link #admin()}), and changes to accounts, settings, programs and
 * age groups also need a recent password confirmation (DD-02). Lists are paginated, at most 100 rows.
 */
@RestController
@RequestMapping("/api/v1/admin")
class AdminController {

    record NewSuperAdmin(@NotBlank(message = "required") @Email(message = "must be an email address")
            @Size(max = 254, message = "is too long") String email) {
    }

    record AccountAction(@NotBlank(message = "required") String action) {
    }

    record CourseChanges(String title, String description, String icon, String status, Integer sortOrder) {
    }

    record LessonChanges(String title, String status) {
    }

    record ItemChanges(String word, String description, String altText) {
    }

    record QuizChanges(Integer passMarkPercent, Boolean required, String status) {
    }

    record QuestionChanges(String prompt, String pool, List<Map<String, Object>> options) {
    }

    record ProgramCourses(@NotNull(message = "required") List<Long> courseIds) {
    }

    record AgeGroupChanges(String name, Integer minAge, Integer maxAge) {
    }

    record BadgeChanges(String title, String description, String icon, Boolean active) {
    }

    record MessageChanges(String text, Boolean active) {
    }

    record NewMessage(@NotBlank(message = "required") String key, Long ageGroupId,
            @NotBlank(message = "required") @Size(max = 300) String text) {
    }

    record SettingValue(@NotNull(message = "required") String value) {
    }

    record FeedbackStatus(@NotBlank(message = "required") String status) {
    }

    private final CurrentUser currentUser;
    private final AdminService admin;
    private final FeedbackService feedback;
    private final ParentService parents;
    private final ChildService children;
    private final RecentAuthentication recent;

    AdminController(CurrentUser currentUser, AdminService admin, FeedbackService feedback, ParentService parents,
            ChildService children, RecentAuthentication recent) {
        this.currentUser = currentUser;
        this.admin = admin;
        this.feedback = feedback;
        this.parents = parents;
        this.children = children;
        this.recent = recent;
    }

    private long admin() {
        currentUser.requireMode(Role.SUPER_ADMIN);
        return currentUser.accountId();
    }

    private static int size(int size) {
        return Math.clamp(size, 1, 100);
    }

    @GetMapping("/overview")
    Map<String, Object> overview() {
        admin();
        return admin.overview();
    }

    @GetMapping("/reports/courses")
    List<Map<String, Object>> courseReport() {
        admin();
        return admin.courseReport();
    }

    @GetMapping("/accounts")
    List<Map<String, Object>> accounts(@RequestParam(required = false) String q,
            @RequestParam(defaultValue = "50") int size, @RequestParam(defaultValue = "0") int page) {
        admin();
        return admin.accounts(q, size(size), Math.max(0, page));
    }

    /**
     * D79: add another Super Admin. Sensitive, so the password must have been proven recently (DD-26). The
     * random temporary password is returned once, to this admin only; the new admin must replace it at the
     * first sign-in.
     */
    @PostMapping("/accounts")
    ResponseEntity<Map<String, Object>> addSuperAdmin(@Valid @RequestBody NewSuperAdmin body,
            HttpServletRequest request) {
        long adminId = admin();
        recent.require(request);
        return ResponseEntity.status(201).body(admin.createSuperAdmin(adminId, body.email()));
    }

    @PostMapping("/accounts/{id}/status")
    ResponseEntity<Void> accountStatus(@PathVariable long id, @Valid @RequestBody AccountAction body,
            HttpServletRequest request) {
        long adminId = admin();
        recent.require(request);
        admin.changeAccountStatus(adminId, id, body.action());
        return ResponseEntity.noContent().build();
    }

    @PostMapping("/accounts/{id}/temporary-password")
    Map<String, String> temporaryPassword(@PathVariable long id, HttpServletRequest request) {
        long adminId = admin();
        recent.require(request);
        return Map.of("temporaryPassword", admin.issueTemporaryPassword(adminId, id));
    }

    @GetMapping("/children")
    List<Map<String, Object>> children(@RequestParam(required = false) String q,
            @RequestParam(defaultValue = "50") int size, @RequestParam(defaultValue = "0") int page) {
        admin();
        return admin.children(q, size(size), Math.max(0, page));
    }

    @GetMapping("/children/{id}/progress")
    ChildReport childProgress(@PathVariable long id) {
        admin();
        return parents.reportOf(children.find(id).orElseThrow(() -> ApiException.notFound("Child")));
    }

    @GetMapping("/courses")
    List<Map<String, Object>> courses() {
        admin();
        return admin.courses();
    }

    @GetMapping("/courses/{id}")
    Map<String, Object> course(@PathVariable long id) {
        admin();
        return admin.course(id);
    }

    @PatchMapping("/courses/{id}")
    Map<String, Object> updateCourse(@PathVariable long id, @RequestBody CourseChanges body) {
        admin.updateCourse(admin(), id, body.title(), body.description(), body.icon(), body.status(),
                body.sortOrder());
        return admin.course(id);
    }

    @PatchMapping("/lessons/{id}")
    ResponseEntity<Void> updateLesson(@PathVariable long id, @RequestBody LessonChanges body) {
        admin.updateLesson(admin(), id, body.title(), body.status());
        return ResponseEntity.noContent().build();
    }

    @PatchMapping("/items/{id}")
    ResponseEntity<Void> updateItem(@PathVariable long id, @RequestBody ItemChanges body) {
        admin.updateItem(admin(), id, body.word(), body.description(), body.altText());
        return ResponseEntity.noContent().build();
    }

    @GetMapping("/quizzes/{id}")
    Map<String, Object> quiz(@PathVariable long id) {
        admin();
        return admin.quiz(id);
    }

    @PatchMapping("/quizzes/{id}")
    Map<String, Object> updateQuiz(@PathVariable long id, @RequestBody QuizChanges body) {
        admin.updateQuiz(admin(), id, body.passMarkPercent(), body.required(), body.status());
        return admin.quiz(id);
    }

    @PatchMapping("/questions/{id}")
    ResponseEntity<Void> updateQuestion(@PathVariable long id, @RequestBody QuestionChanges body) {
        admin.updateQuestion(admin(), id, body.prompt(), body.pool(), body.options());
        return ResponseEntity.noContent().build();
    }

    @GetMapping("/programs")
    List<Map<String, Object>> programs() {
        admin();
        return admin.programs();
    }

    @PutMapping("/programs/{id}/courses")
    List<Map<String, Object>> setProgramCourses(@PathVariable long id, @Valid @RequestBody ProgramCourses body,
            HttpServletRequest request) {
        long adminId = admin();
        recent.require(request);
        admin.setProgramCourses(adminId, id, body.courseIds());
        return admin.programs();
    }

    @GetMapping("/age-groups")
    List<Map<String, Object>> ageGroups() {
        admin();
        return admin.ageGroups();
    }

    @PatchMapping("/age-groups/{id}")
    List<Map<String, Object>> updateAgeGroup(@PathVariable long id, @RequestBody AgeGroupChanges body,
            HttpServletRequest request) {
        long adminId = admin();
        recent.require(request);
        admin.updateAgeGroup(adminId, id, body.name(), body.minAge(), body.maxAge());
        return admin.ageGroups();
    }

    @GetMapping("/badges")
    List<Map<String, Object>> badges() {
        admin();
        return admin.badges();
    }

    @PatchMapping("/badges/{id}")
    List<Map<String, Object>> updateBadge(@PathVariable long id, @RequestBody BadgeChanges body) {
        admin.updateBadge(admin(), id, body.title(), body.description(), body.icon(), body.active());
        return admin.badges();
    }

    @GetMapping("/messages")
    List<Map<String, Object>> messages() {
        admin();
        return admin.messages();
    }

    @PatchMapping("/messages/{id}")
    List<Map<String, Object>> updateMessage(@PathVariable long id, @RequestBody MessageChanges body) {
        admin.updateMessage(admin(), id, body.text(), body.active());
        return admin.messages();
    }

    @PostMapping("/messages")
    List<Map<String, Object>> createMessage(@Valid @RequestBody NewMessage body) {
        admin.createMessage(admin(), body.key(), body.ageGroupId(), body.text());
        return admin.messages();
    }

    @GetMapping("/feedback")
    List<FeedbackView> feedback(@RequestParam(required = false) String status,
            @RequestParam(defaultValue = "50") int size, @RequestParam(defaultValue = "0") int page) {
        admin();
        return feedback.forAdmin(status, size(size), Math.max(0, page));
    }

    @PatchMapping("/feedback/{id}")
    FeedbackView feedbackStatus(@PathVariable long id, @Valid @RequestBody FeedbackStatus body) {
        return feedback.setStatus(admin(), id, body.status());
    }

    @GetMapping("/settings")
    Map<String, String> settings() {
        admin();
        return admin.settings();
    }

    @PutMapping("/settings/{key}")
    Map<String, String> updateSetting(@PathVariable String key, @Valid @RequestBody SettingValue body,
            HttpServletRequest request) {
        long adminId = admin();
        recent.require(request);
        admin.updateSetting(adminId, key, body.value());
        return admin.settings();
    }

    @GetMapping("/audit")
    List<Map<String, Object>> audit(@RequestParam(required = false) String action,
            @RequestParam(defaultValue = "50") int size, @RequestParam(defaultValue = "0") int page) {
        admin();
        return admin.audit(action, size(size), Math.max(0, page));
    }

    @GetMapping("/audit/actions")
    List<String> auditActions() {
        admin();
        return admin.auditActions();
    }
}
