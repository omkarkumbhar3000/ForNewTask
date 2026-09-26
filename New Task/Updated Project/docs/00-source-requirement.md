# Source Requirement — Kids Learn / CleverCubs enhancement (verbatim)

**Received:** 2026-09-26, from the owner in the CLI session · **Objective:** `OBJ-034`
(`../../../BLAST/Objective.md`) · **Status:** ⛔ verbatim record; never edit

Everything below the line is the owner's text exactly as given. Clarifications and owner answers are
recorded in [`03-decisions.md`](03-decisions.md), never here.

---

# Kids Learn Project — Enhancement & Development Requirements

## 1. Project Context

I have an existing/older project that I uploaded into the current project folder. Treat this as the baseline **Kids Learn / CleverCubs project**.

I now want to enhance this application based on requirements received from colleagues, review feedback, and future feedback that may be provided.

The goal is **not simply to modify individual pages**. First understand the existing application, its structure, flows, functionality, data handling, and limitations. Then create an enhanced version in the **updated project folder that already exists inside the New Task folder**.

Do not unnecessarily modify or overwrite the original project.

Before making implementation decisions, inspect the existing project thoroughly.

---

# 2. Core Objective

The primary objective is to make the application:

* More child-friendly
* Easier to use
* Simple and intuitive
* Visually attractive
* Lightweight and performant
* Safe and secure
* Easy for parents to understand
* Easy to maintain and extend
* Ready for future mobile usage

The application should feel modern, friendly, educational, and engaging without becoming unnecessarily complex.

Use appropriate UI/UX improvements, animations, micro-interactions, illustrations/icons where useful, progress indicators, helpful messages, and child-friendly visual elements.

Keep the overall experience **simple, crisp, clear, and lightweight**.

Use a **light theme** with an attractive, age-appropriate color palette.

Do not add animations or visual effects merely for decoration. Every UI element should have a purpose and should not negatively affect performance or accessibility.

---

# 3. Important Development Principle

Do not assume requirements that have not been provided.

If a decision materially affects:

* Architecture
* Data model
* Security
* User roles
* Authentication
* Child/parent relationships
* Course logic
* Quiz logic
* Rewards
* Database structure
* Mobile architecture
* Existing functionality

then first identify the ambiguity and ask for clarification.

However, for minor UI/UX decisions where multiple standard approaches are possible, use reasonable industry-standard practices and document the decision.

Do not block progress unnecessarily for small design decisions.

---

# 4. Existing Application Analysis

Before implementation:

1. Inspect the complete existing project.
2. Understand the current page structure.
3. Understand the current login and registration flow.
4. Understand course and lesson navigation.
5. Understand quiz functionality.
6. Understand profile functionality.
7. Identify frontend/backend responsibilities.
8. Identify current data storage and database dependencies.
9. Identify existing security weaknesses.
10. Identify broken links, missing files, hard-coded paths, obsolete code, and technical debt.
11. Identify reusable components/functionality.
12. Identify areas that can be optimized.

Create an implementation plan before making major structural changes.

Do not remove existing functionality unless:

* it is clearly obsolete,
* it conflicts with the new requirements,
* or I explicitly approve its removal.

---

# 5. Target Users and Age-Based Experience

This application targets **multiple age groups of children**.

The application must therefore support age-appropriate content and experiences.

During registration, the parent should provide the required parent information and the child's information, including the child's age/date of birth as appropriate.

The application should dynamically determine the child's age group and adjust the user experience accordingly.

Examples of dynamically adjustable elements include:

* Language complexity
* Instructions
* Educational content presentation
* UI complexity
* Visual style
* Illustrations
* Feedback messages
* Motivational messages
* Quiz presentation
* Difficulty/context where applicable
* Navigation complexity
* Reward presentation

Do not hard-code inappropriate content for all age groups.

Use age-appropriate and child-safe language.

Do not infer sensitive characteristics about a child from unrelated information.

If exact age-group definitions are required, identify them as a requirement that needs confirmation rather than inventing arbitrary categories.

---

# 6. Registration

Create a proper registration flow supporting both:

## Parent information

Potential fields may include:

* Parent/guardian name
* Address
* Mobile number
* Email ID
* Other appropriate contact information

## Child information

Potential fields may include:

* Child name
* Date of birth / age
* Username
* Other non-sensitive profile information that is genuinely required

Initially, include a reasonable set of fields so that we can review them later.

Clearly distinguish:

* Mandatory fields
* Optional fields
* Additional/recommended fields

Do not collect unnecessary personal or sensitive information.

The final required-field list can be refined during review.

---

# 7. Parent and Child Account Relationship

The system should maintain a clear relationship between:

**Parent/Guardian Account → Child Account → Courses → Lessons → Quizzes → Progress**

The parent email/contact configured during registration should be associated with the child account.

If a child encounters an issue where an action requires parent involvement, the system should provide an appropriate mechanism to redirect/escalate the action to the registered parent/guardian.

Do not expose the parent's private information to the child unnecessarily.

Do not automatically expose parent credentials to the child.

The exact fallback/escalation behavior should be clearly documented and implemented securely.

---

# 8. Authentication and Access Control

A user must be authenticated before accessing protected application content.

When a user directly opens a protected URL without a valid authenticated session:

**Redirect the user to the login page.**

Do not allow users to bypass authentication simply by directly entering a URL.

Implement proper:

* Authentication
* Session management
* Authorization
* Role-based access control
* Session expiration
* Logout
* Protected routes
* Unauthorized-access handling

At minimum, support the appropriate roles required by the application, such as:

* Child/User
* Parent/Guardian
* Super Admin

Do not rely only on frontend checks for authorization.

Authorization must also be enforced on the backend.

---

# 9. Course and Lesson Experience

The application contains multiple courses.

Improve the course experience with:

* Course cards
* Clear course descriptions
* Course progress
* Lesson progress
* Completed/incomplete states
* Helpful navigation
* Age-appropriate presentation
* Clear next-step actions
* Resume-learning functionality where appropriate

The UI should clearly communicate what the child has completed and what remains.

---

# 10. Course Progress Tracking

Each course should have a progress bar.

The progress calculation must follow the actual learning flow.

A course must **not show 100% completion before the required quiz is completed**.

For example:

**Lessons completed → Progress increases**

**Required quiz not completed → Course remains below 100%**

**Required quiz successfully completed → Course can reach 100%**

Track the child's progress persistently.

The system should be able to determine:

* Course started
* Lessons completed
* Lessons remaining
* Quiz attempted
* Quiz attempts remaining
* Quiz result
* Course completion status
* Overall progress

Do not fake progress only on the frontend.

Progress should be stored and calculated reliably by the backend/database.

---

# 11. Quiz Requirements

Each course can contain a quiz.

A child should have a maximum of:

**3 quiz attempts per quiz.**

Track every attempt appropriately.

The system should show:

* Attempt number
* Attempts remaining
* Score
* Completion status
* Appropriate feedback

Do not allow the frontend alone to bypass the 3-attempt limit.

The backend must enforce the limit.

If the quiz is required for course completion, the course must not be marked as 100% complete until the quiz requirement has been satisfied.

The exact behavior after all 3 attempts are exhausted should be identified clearly. If the existing project does not define this behavior, flag it for review rather than silently inventing a business rule.

---

# 12. Profile Enhancement

The existing profile functionality is basic.

Enhance it with appropriate features such as:

* Username creation
* Username modification
* Profile information
* Child-friendly display name
* Optional tag/nickname
* Profile avatar where appropriate
* Course summary
* Progress summary
* Achievements
* Badges
* Certificates where applicable
* Account preferences
* Parent/guardian relationship information where appropriate

Do not add unnecessary personal information.

Any username/nickname must follow appropriate safety and privacy rules.

---

# 13. Rewards and Achievements

Introduce a reward/achievement system.

A reward should become available only when the defined performance threshold is achieved.

Initial requirement:

**Reward eligibility starts at scores/progress above 80%.**

Potential rewards include:

* Badges
* Achievement levels
* Certificates
* Completion recognition
* Encouraging messages

Rewards should motivate learning rather than create unhealthy pressure or competition.

Do not create public leaderboards or public child rankings unless explicitly requested.

Keep rewards age-appropriate.

The exact definition of "above 80%" must be made consistent throughout the application. If it is unclear whether this means quiz score, course progress, or another metric, flag this for clarification before implementing the final business rule.

---

# 14. Motivation and Child-Friendly UX

Use appropriate motivational content such as:

* Short positive quotes
* Encouraging messages
* Completion messages
* Progress encouragement
* Friendly illustrations
* Small success animations
* Helpful empty states

The tone should encourage learning and effort.

Avoid messaging that:

* Shames the child
* Compares one child against another
* Creates unnecessary pressure
* Suggests failure as a negative personal trait
* Makes unrealistic promises

Keep language appropriate for the child's age group.

---

# 15. Parent Feedback

Add a dedicated feedback section where parents/guardians can provide feedback about the application.

Feedback may include:

* General feedback
* Course feedback
* Usability feedback
* Suggestions
* Problems encountered

Feedback should be stored securely and made available to authorized administrators.

Do not expose private parent feedback to child users.

---

# 16. One-Year Course Completion

When the child completes the one-year course/program, show a dedicated completion experience.

Provide information intended primarily for the parent/guardian so they can understand:

* What was completed
* Overall progress
* Achievements
* Quiz performance where appropriate
* Learning summary
* Areas that may require attention
* What the next-year program could contain
* Whether they want to continue to the next year

Do not make unsupported educational or developmental claims about the child.

The continuation decision should remain with the parent/guardian.

---

# 17. Contact Us

Add a clearly visible **Contact Us** option.

It should provide appropriate creator/application contact information.

Do not expose unnecessary personal information.

The location can be in the footer, navigation, profile area, or another appropriate location based on the final UI design.

---

# 18. Terms and Conditions

Add a Terms & Conditions section.

It should clearly explain appropriate responsibilities and limitations, including that the application cannot guarantee a particular learning outcome or level of progress.

Do not use language that blames or shames the child or parent.

The wording should be professionally written and suitable for a child-focused educational application.

Because this application involves children and personal information, identify any areas that require legal/privacy review instead of presenting the application's wording as legally sufficient.

---

# 19. Super Admin Dashboard

Create a dedicated **Super Admin Dashboard**.

The Super Admin should have authorized access to the complete administrative context required to operate the platform.

Potential capabilities include:

* User management
* Parent/guardian management
* Child account management
* Course management
* Lesson management
* Quiz management
* Progress monitoring
* Feedback management
* Rewards/achievement management
* Content management
* Basic reporting
* System configuration
* Appropriate audit information

Do not give administrators unrestricted access merely because they are logged in.

Use proper role-based authorization.

Sensitive actions should be protected appropriately.

Maintain audit information for important administrative changes.

---

# 20. Security Requirements

Security is a mandatory requirement, not an optional enhancement.

Identify and address all security issues found in the existing application and in the new implementation.

Follow established secure-development practices appropriate to the technology stack.

At minimum, review and protect against:

* SQL injection
* XSS
* CSRF where applicable
* Authentication bypass
* Authorization bypass
* Session vulnerabilities
* Broken access control
* Insecure direct object references
* Password exposure
* Plain-text password storage
* Weak password handling
* Sensitive information exposure
* Unsafe file uploads
* Path traversal
* Insecure API endpoints
* Excessive data exposure
* Improper error messages
* Hard-coded credentials/secrets
* Insecure database access
* Missing input validation
* Missing output encoding
* Client-side-only security controls

Passwords must never be stored in plain text.

Use appropriate password hashing and secure authentication practices.

Do not hard-code credentials, API keys, database passwords, or secrets into source code.

Do not expose child or parent personal information unnecessarily.

Because this is a child-focused application, apply privacy-by-design principles and minimize the collection and exposure of personal data.

Do not claim legal/regulatory compliance unless it has actually been verified.

Any applicable child privacy, data protection, retention, consent, and parental-control requirements should be identified for review based on the target deployment jurisdiction.

---

# 21. Backend Technology

For the backend, use:

**Java**

Use a clean and maintainable architecture.

Keep frontend, backend, authentication, business logic, persistence, and configuration appropriately separated.

Use standard Java development practices and suitable frameworks/libraries where justified.

Do not introduce unnecessary frameworks or dependencies.

---

# 22. Database

Design the database according to the actual application requirements.

The data model should appropriately support relationships such as:

* Parent
* Child
* Authentication/account
* Courses
* Lessons
* Quizzes
* Quiz attempts
* Progress
* Rewards
* Feedback
* Admin
* Audit information

Do not finalize the database schema based on assumptions where existing requirements are missing.

If the existing project contains an incomplete or missing schema, identify the gap and propose the required schema before implementation.

---

# 23. Desktop and Future Mobile Support

The initial target is:

**Desktop web browser.**

However, the application should be designed with future mobile usage in mind.

Therefore:

* Use responsive layouts.
* Avoid desktop-only assumptions.
* Use touch-friendly controls where practical.
* Keep components reusable.
* Avoid hard-coded screen dimensions.
* Keep navigation adaptable.
* Design APIs so they can later support a mobile client.

Do not create a separate native mobile application unless explicitly requested.

For now, make the web application **mobile-ready/responsive** while keeping the desktop browser experience as the primary target.

---

# 24. UI/UX and Visual Design

Use a modern child-friendly design system.

Requirements:

* Light theme
* Attractive but controlled colors
* Good typography
* Clear hierarchy
* Rounded/soft visual elements where appropriate
* Friendly illustrations/icons
* Simple navigation
* Consistent buttons and controls
* Clear success/error states
* Meaningful animations
* Smooth transitions
* Progress visualization
* Responsive layout
* Accessible interaction patterns

The application should feel polished without becoming visually overloaded.

Avoid excessive animations, large assets, unnecessary libraries, and heavy visual effects.

---

# 25. Performance and Optimization

Perform meaningful optimization across the application.

Review:

* Page load performance
* JavaScript execution
* CSS size
* Image/media optimization
* Video handling
* API calls
* Database queries
* Duplicate code
* Unnecessary dependencies
* Caching opportunities
* Lazy loading
* Asset loading
* Backend response times
* Error handling

Do not optimize blindly.

Measure or identify actual bottlenecks where possible.

The final application should remain lightweight and responsive.

---

# 26. Maintainability

Keep the project maintainable.

Where appropriate:

* Reuse components
* Remove unnecessary duplication
* Use meaningful names
* Keep configuration separate
* Keep secrets outside source control
* Add appropriate comments/documentation
* Keep frontend/backend responsibilities clear
* Maintain a clean folder structure
* Avoid unnecessary complexity

Do not rewrite the entire application merely for stylistic reasons if the existing implementation can be safely improved.

---

# 27. Existing Security and Functional Issues

While reviewing the current project, document all existing issues separately from newly introduced issues.

For example, if an issue already exists in the uploaded project, do not incorrectly report it as a regression caused by the enhancement.

Maintain a clear distinction between:

1. Existing issue
2. Fixed existing issue
3. New enhancement
4. New issue introduced during development
5. Information/requirement still required

---

# 28. Testing Requirements

Before considering the enhanced project complete, test the important application flows.

At minimum verify:

### Authentication

* Login
* Logout
* Invalid credentials
* Protected URL access
* Session handling

### Registration

* Parent registration
* Child registration
* Required/optional fields
* Validation
* Parent-child relationship

### Courses

* Course access
* Lesson navigation
* Progress tracking
* Resume behavior

### Quiz

* Quiz completion
* Score calculation
* 3-attempt limit
* Attempt tracking
* Course completion dependency

### Profile

* Username
* Profile updates
* Progress/achievement visibility

### Rewards

* 80% threshold behavior
* Badge/certificate behavior

### Parent

* Feedback
* Course completion information
* Parent-related flows

### Admin

* Authentication
* Authorization
* User management
* Course management
* Progress visibility
* Feedback management

### Security

* Unauthorized access
* SQL injection protection
* XSS protection
* Authentication bypass
* Authorization bypass
* Sensitive-data exposure
* Password handling

Also test responsive behavior for desktop and smaller screen sizes.

---

# 29. Development Workflow

Follow this sequence:

### Phase 1 — Understand

Inspect the existing project completely.

### Phase 2 — Analyze

Identify:

* Existing functionality
* Architecture
* UX issues
* Security issues
* Performance issues
* Missing requirements
* Data-model gaps

### Phase 3 — Plan

Create a clear implementation plan.

### Phase 4 — Build

Implement the enhanced application in the existing **updated project folder**.

Do not modify the original baseline unnecessarily.

### Phase 5 — Validate

Run appropriate functional, security, and quality checks.

### Phase 6 — Review

Summarize:

* What changed
* What was preserved
* What security issues were fixed
* What remains
* What requires clarification
* What assumptions were made
* What additional recommendations exist

---

# 30. Git / Repository Handling

At this stage, **do not perform Git push or pull activities**.

Do not push anything to a remote repository.

Do not assume that the project is ready for commit.

The project should be treated as being stored and developed locally until I explicitly confirm that I am ready for Git activities.

Before any future commit, identify:

* Large files
* Videos/media
* Git LFS requirements
* Secrets
* Generated files
* Temporary files
* Build artifacts
* Unnecessary files

Do not commit secrets or sensitive information.

---

# 31. Important Final Instruction

Think beyond the explicitly listed requirements and identify improvements that would genuinely enhance:

* Child experience
* Parent experience
* Usability
* Accessibility
* Security
* Performance
* Maintainability
* Scalability
* Future mobile readiness
* Course engagement
* Progress tracking
* Administration

However, do **not** add random features simply to increase the feature count.

Every additional feature should have a clear purpose and should integrate properly with the rest of the application.

Do not make assumptions about important business rules.

If clarification is required, stop at the appropriate decision point and ask me.

For minor implementation/design decisions, use established industry practices and document the decision.

The final result should be a **simple, lightweight, secure, child-friendly, modern educational application** with a strong foundation for future enhancement.

---

# Addendum — the owner's covering note, same message

Whatever I have created for this project, I have already uploaded all the available files and related materials to the respective current project folder.

Please use the current project folder as the primary source of truth. If you find that any required file, configuration, documentation, or other project artifact is missing, create it as needed based on the existing project structure and requirements. & if possible use skill that we have.
