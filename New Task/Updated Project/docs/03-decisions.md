# Decisions — What the owner decides, and what follows standard practice

**Objective:** `OBJ-034` · **Requirement:** [`00-source-requirement.md`](00-source-requirement.md) §3, §31 ·
**Status:** ✅ all 12 owner decisions answered (2026-09-26); defaults in §3 apply unless overridden. `DD-20`–`DD-26`
were added during the build (2026-09-27) and are open to the owner's review

---

## 1. How this file works

Requirement §3 separates two kinds of decision, and this file keeps them apart.

| Kind | Rule | Here |
|---|---|---|
| **DQ — owner decision** | Materially affects architecture, data model, security, roles, auth, parent–child relationships, course, quiz or reward logic, the database, the mobile design or existing functionality. **Asked, never assumed** | §2 |
| **DD — documented default** | A minor or standard decision. Follows established practice, is written down, and the owner can override it at any time | §3 |
| **INF — information required** | A fact nobody has supplied yet. Built as a clearly marked placeholder, never invented | [`02-issue-register.md`](02-issue-register.md) §5 |

Each answered DQ is also recorded as an owner decision in the repository history
(`docs/history/02-decisions.md`, `D56` onwards).

## 2. Owner decisions (DQ)

### DQ-01 — Backend framework and frontend approach (§21, §23, §26)

The requirement fixes Java and asks for justified dependencies only. The baseline frontend is 44 static pages
with no build step.

| Option | What it means |
|---|---|
| **A. Spring Boot 4.1 + static pages and vanilla JS calling a JSON API** (recommended) | Spring Security supplies sessions, CSRF, RBAC, password hashing and protected-route redirects, so none of it is hand-written. The pages are plain HTML, CSS and ES modules, with no build step. They call a versioned REST API (`/api/v1`), the same API a mobile app would use later (§23) |
| B. Spring Boot + server-rendered templates (Thymeleaf) | Also light, but UI and API are coupled, so a mobile client would need a second, parallel API |
| C. Minimal framework (Javalin, plain servlets) + hand-built security | Fewer dependencies, but sessions, CSRF and RBAC are written by hand: exactly the kind of code the baseline got wrong |

**Answer (2026-09-26): ✅ A.** Spring Boot 4.1 with plain HTML, CSS and JavaScript pages calling a versioned
REST API. History `D56`.

### DQ-02 — Database and how it runs locally (§22)

The baseline uses MySQL (`kidslearn`). Neither MySQL nor PHP is installed on this machine. Docker Desktop is
installed but its engine is stopped.

| Option | What it means |
|---|---|
| **A. MySQL 8, run in Docker for development and in Testcontainers for tests** (recommended) | Same engine family as the baseline. Tests run against a real MySQL, not an imitation. Needs Docker Desktop started and a one-time image download (about 0.5 GB on C:) |
| B. MySQL 8 from the portable "no-install" zip | No Docker. A larger download, started by a script; tests use the same server |
| C. H2 embedded database (zero install) with MySQL for production | Easiest to run, but tests would pass against a database the application will not use in production |

**Answer (2026-09-26): ✅ A.** MySQL 8, run in Docker for development and through Testcontainers for tests.
History `D57`.

### DQ-03 — How a child signs in (§6, §7, §8, §12)

Young children cannot manage passwords, and a parent–child relationship is required.

| Option | What it means |
|---|---|
| **A. Parent signs in, then picks the child ("Who is learning?")** (recommended) | The child never handles a password. The session switches into a child mode that can reach learning pages only. Leaving child mode or opening the parent area asks for the parent's password again |
| B. Each child has an own username and password, set up by the parent | Children log in directly. Suits older children, but young children forget or share passwords |
| C. A, plus an optional own login for children in the oldest age group | Most flexible, and more to build and test |

**Answer (2026-09-26): ✅ A.** The parent signs in, then picks the child. The child never holds a password.
Leaving child mode, or opening the parent area, asks for the parent's password again. History `D58`.

### DQ-04 — Age groups (§5)

The requirement asks for age groups to be confirmed, not invented. The baseline content (alphabet, numbers,
colours, animals, rhymes, stories) is toddler and pre-school level.

| Option | What it means |
|---|---|
| **A. Three bands: 2–3, 4–5, 6–8** (recommended) | Follows the common toddler / pre-school / early-primary split. Existing content maps to the first two bands; the third needs new content (`INF`) |
| B. Two bands: 2–4 and 5–7 | Simpler, and closer to the content that exists |
| C. Another definition | The owner specifies the bands |

Whichever is chosen, the bands are stored as data (editable by the Super Admin), not hard-coded.

**Answer (2026-09-26): ✅ A.** Three bands, 2–3, 4–5 and 6–8, stored as editable data. Content for 6–8 is
`INF-01`. History `D66`.

### DQ-05 — What a lesson is (§9, §10)

A baseline topic page is one long page of cards (A–Z, 1–10, …). Progress and "resume" need a smaller unit.

| Option | What it means |
|---|---|
| **A. Each topic is a course, split into short lessons of about five items** (recommended) | For example, Alphabets becomes A–E, F–J and so on. Progress moves visibly, and "resume" returns to the next lesson |
| B. Each item is its own lesson | The finest-grained progress, but 26 lessons for the alphabet alone |
| C. Each topic page is one lesson | The simplest, but progress jumps from 0% straight to its maximum |

**Answer (2026-09-26): ✅ A.** Each topic is a course of short lessons of about five items. Each rhyme and
each story is one lesson. History `D60`.

### DQ-12 — How course progress is calculated (§10)

The baseline already has a rule. Tapping every lesson card caps a subject at **70%**, and passing its quiz
sets it to **100%** (`alphabets_voice.html:284-286`, `animal_qq.html:128`). It is computed in the browser; the
new version computes it on the server.

| Option | What it means |
|---|---|
| **A. Keep the baseline's weighting: lessons make up 70%, passing the quiz adds the last 30%** (recommended) | Existing behaviour, and it already meets §10. With five lessons, each completed lesson adds 14% |
| B. Treat the quiz as one more step: `completed steps ÷ (lessons + 1)` | With five lessons, the lessons reach 83% and the quiz the last 17%. The quiz weighs less as a course grows |

**Answer (2026-09-26): ✅ A.** Lessons make up 70% of a course and passing the quiz adds the last 30%,
calculated on the server. A course without a quiz (rhymes, stories) reaches 100% through its lessons.
History `D61`.

### DQ-06 — What counts as passing the required quiz (§10, §11)

The requirement says a course reaches 100% only when the required quiz is "successfully completed", but it
does not define a pass mark. The baseline has **three different pass marks** for the same subjects. The
quizzes linked from the lessons pass on fewer than 4 mistakes out of 10, i.e. 70% (`alphabets_quize.html:227`).
The quiz-hub quizzes pass on more than 4 correct out of 10, i.e. 50% (`animal_qq.html:125`). The 5-question
alphabet hub quiz passes on 4 or more, i.e. 80% (`alphabets_qq.html:89`).

| Option | What it means |
|---|---|
| **A. 70%, the rule of the quizzes linked from the lessons** (recommended) | Keeps the baseline's main rule. Passing (course completion) stays separate from rewards (above 80%), which keeps pressure low for young children (§14). Stored per quiz, so the Super Admin can change it |
| B. Passing means scoring above 80% | A single threshold, but a course cannot complete without a reward-level score |
| C. 50%, the rule of the quiz-hub quizzes | The gentlest threshold |

**Answer (2026-09-26): ✅ A.** The pass mark is 70%, stored per quiz and editable by the Super Admin.
History `D62`.

### DQ-07 — What happens after three unsuccessful attempts (§11)

The baseline allows unlimited retries (`location.reload()`), so it defines no rule. The requirement says to flag
this.

| Option | What it means |
|---|---|
| **A. The quiz locks, and the parent can grant three more attempts** (recommended) | The course stays below 100%. The child sees an encouraging "Let's practise the lessons again" and an "Ask a grown-up" option, and the parent unlocks it from the parent area. Every reset is recorded |
| B. Attempts reset automatically after the child reviews the lessons again | No adult needed, but the three-attempt limit becomes soft |
| C. Only a Super Admin can reset attempts | The strictest option, and slow for families |

**Answer (2026-09-26): ✅ A.** After three unsuccessful attempts the quiz locks and the course stays below
100%. The child is encouraged to practise and can ask a grown-up; the parent grants three more attempts from
the parent area. Every grant is audited. History `D63`.

### DQ-08 — What "above 80%" measures for rewards (§13)

With 10 questions, "above 80%" taken literally means 9 or 10 correct. On the 5-question alphabet quiz it
means a perfect score.

| Option | What it means |
|---|---|
| **A. Best quiz score of 80% or more** (recommended) | 8 of 10, or 4 of 5, earns the reward. The same rule applies everywhere |
| B. Best quiz score strictly above 80% | Literal wording: 9 of 10, or 5 of 5 |
| C. Course progress above 80% | Rewards effort through lessons, not the quiz result |

**Answer (2026-09-26): ✅ A.** A reward needs a best quiz score of **80% or more**: 8 of 10, or 4 of 5. This is
the one reward rule used everywhere. History `D64`.

### DQ-09 — What the "one-year program" is (§16)

Nothing in the baseline defines a year or a program.

| Option | What it means |
|---|---|
| **A. A program is an admin-defined list of courses for one age group** (recommended) | "Year 1" for a band is complete when all its courses reach 100%. The parent then sees the summary and decides about "Year 2" (the next band's program, content `INF`) |
| B. A program is 12 months from registration | Time-based: completion depends on the calendar, not on learning |
| C. All courses in the application | One program for everyone; no age-based next year |

**Answer (2026-09-26): ✅ A.** A program is an admin-defined list of courses for one age group. It is
complete when all its courses reach 100%, and the parent decides about the next year. History `D65`.

### DQ-10 — How a child escalates to the parent (§7)

No email or SMS provider is available, and the baseline has none.

| Option | What it means |
|---|---|
| **A. In-app parent gate and request inbox** (recommended) | An action that needs a parent shows "Ask a grown-up". The parent either approves on the spot by entering their password, or later from the parent area, where pending requests wait. No parent data is shown to the child |
| B. Email the parent an approval link | Reaches the parent anywhere, but needs an email provider and credentials (`INF`) |
| C. A now, B later when an email provider is configured | The same code path, with email added through configuration |

**Answer (2026-09-26): ✅ C.** An in-app parent gate and request inbox now. Email notification is switched
on by configuration once a provider exists (`INF-04`). History `D59`.

### DQ-11 — Target jurisdiction for child-privacy review (§18, §20)

Consent, retention and parental-rights rules depend on where the application is offered. Compliance is never
claimed until reviewed.

| Option | What it means |
|---|---|
| India (DPDP Act 2023) | Verifiable parental consent for anyone under 18, no tracking or targeted advertising of children |
| United States (COPPA) | Verifiable parental consent under 13, a privacy notice, and parental review and deletion rights |
| EU / UK (GDPR, UK Age-Appropriate Design Code) | Consent age 13–16 by country, high-privacy defaults, data-protection impact assessment |
| **Not decided yet** (recommended if unsure) | Build to the strictest common baseline: parental consent at registration, minimal data, no tracking, export and delete on request. Flag every legal text for review |

**Answer (2026-09-26): ✅ Not decided yet.** The build follows the strictest common baseline:
- recorded parental consent at registration;
- data minimisation, with no tracking, analytics or advertising;
- parent export and deletion of a child's data;
- every legal text marked "Draft — requires legal review" (`INF-03`).

History `D67`.

## 3. Documented defaults (DD)

Standard practice, applied unless the owner overrides it. Each one closes a security or quality gap recorded
in [`02-issue-register.md`](02-issue-register.md).

| ID | Area | Default | Basis |
|---|---|---|---|
| DD-01 | Passwords | Parent and admin passwords: at least 12 characters, checked against a list of common passwords, no composition rules. Hashed with bcrypt (cost 12) through Spring Security's `DelegatingPasswordEncoder`, so the algorithm can be upgraded later | NIST SP 800-63B; OWASP Password Storage Cheat Sheet |
| DD-02 | Sessions | Server-side sessions. The cookie is `HttpOnly`, `Secure` (once HTTPS is in place) and `SameSite=Lax`. The session ID is regenerated at login, the idle timeout is 30 minutes, and logout invalidates the session. Opening the parent area needs a password again if the last one was more than 15 minutes ago | OWASP Session Management Cheat Sheet; ASVS V3 |
| DD-03 | CSRF | Spring Security CSRF tokens on every state-changing request, sent by the JavaScript client in a header | ASVS V4.2.2 |
| DD-04 | Access control | Roles `CHILD`, `PARENT`, `SUPER_ADMIN`, enforced on every API endpoint and page route on the server. Ownership checks: a parent sees only their own children, and a child only their own data | ASVS V4 |
| DD-05 | Login abuse | Generic "username or password is incorrect" message. Per-account and per-IP throttling with a growing delay, and a temporary lock after repeated failures | ASVS V2.2 |
| DD-06 | Avatars | A fixed set of illustrated avatars; **no photo upload**. This removes the unsafe-upload risk and keeps children's photos out of the system | Privacy by design (§20); avoids the §20 "unsafe file uploads" class entirely |
| DD-07 | Progress source | Progress is calculated in the backend from stored lesson-completion and quiz-attempt records, by the formula chosen in DQ-12. The browser never sends a progress value | §10; fixes `SEC-E17` |
| DD-17 | Video lessons | A rhyme or story video counts as viewed once it has played to the end, or at least 90% of the way. A picture or sound card counts when it is opened, as in the baseline | The baseline counted a tap (`alphabets_voice.html:260-292`); a long video needs more than a tap to mean "watched" |
| DD-18 | Quiz banks | Each topic's quiz uses the lesson-linked bank (`<topic>_quize.html`, `num_quiz.html`: 10 questions), the same family whose 70% pass mark was chosen (`D62`). The hub-quiz questions are kept in the content files as a reserve for the Super Admin | One canonical bank per course ends `FUN-E02` |
| DD-19 | Attempt counting | An attempt is used when it **starts**. Leaving mid-quiz does not lose it: reopening the quiz resumes the same attempt. Each answer is final and scored by the server, which then shows friendly feedback | Starting-counts prevents peeking at questions for free; resume protects a child who closes the page by accident (§11) |
| DD-16 | Quiz unlock | A course's quiz unlocks once its lessons are complete. This is the baseline hub quizzes' rule (`animal_qq.html:74`, lessons at 70% or more). The lesson-linked quizzes had no lock, so the stricter of the two existing behaviours is kept | Baseline behaviour; §10 learning flow |
| DD-08 | Child usernames | 3–20 characters from letters, digits, `_` and `-`. Checked against the child's own name, email and phone shapes, and a blocked-words list. Suggested automatically as friendly word pairs (e.g. `happy-panda-12`) | §12 ("appropriate safety and privacy rules") |
| DD-09 | Registration fields | Mandatory: parent name, email, password, consent checkbox; child first name or nickname, date of birth. Optional: parent mobile, city. **Not collected:** full address, school, gender, photos. The owner reviews the list later (§6) | Data minimisation (§6, §20) |
| DD-10 | API | JSON under `/api/v1`, errors in the RFC 9457 `application/problem+json` shape, and no internal detail in error responses | §23; ASVS V7.4 |
| DD-11 | Security headers | A strict Content Security Policy (no inline scripts), `X-Content-Type-Options: nosniff`, `frame-ancestors 'none'`, `Referrer-Policy: same-origin`, and HSTS once HTTPS is in place | ASVS V14.4 |
| DD-12 | Third-party code | No CDN scripts at runtime. The confetti effect becomes a small local animation that respects `prefers-reduced-motion`; fonts are self-hosted | ASVS V14.2; children's privacy (no third-party requests) |
| DD-13 | Configuration and secrets | Database credentials and the first Super Admin come from environment variables (`.env`, gitignored); only `.env.example` is kept. The application connects as a dedicated least-privilege database user, never as `root` | §20; ASVS V2.10, V14.1 |
| DD-14 | Audit | Every administrative change, attempt reset, role change and login failure is written to an append-only audit table: who, what, when and the affected record. Passwords and personal fields are never written to it | §19 |
| DD-15 | Architecture | A modular monolith, packaged by feature (accounts, learning, quiz, progress, rewards, feedback, admin, audit). Business rules such as progress, attempt limits and reward thresholds live in plain Java classes, testable without Spring or a database. Controllers stay thin | §21, §26; clean-architecture practice, without layers that simple CRUD does not need |
| DD-20 | Year programs | Each age group's Year-1 program starts with every published course, because the baseline content is the only content (`INF-01`). The age group changes the presentation, not the course list. The Super Admin edits the lists (Programs) | `D65`; no content exists that could tell the bands apart |
| DD-21 | Completion recognition | A course without a quiz (rhymes, stories) earns a completion badge at 100%, and a completed year earns a badge and a certificate. Score badges still follow `D64` (80% or more) | §13 lists "completion recognition"; 100% progress is above the 80% line |
| DD-22 | Registration message | A taken email is reported as taken ("Please sign in instead"), so a parent knows what to do. Tracked as `SEC-R01` with its mitigations | Usability over a small enumeration risk; the sign-in itself reveals nothing |
| DD-23 | Child messages | "Ask a grown-up" sends a request type only (more tries, a new username, help), never free text from the child | Privacy by design (§20); no moderation needed |
| DD-24 | Quiz feedback | After each answer the child sees whether it was right and, if not, the right answer, in encouraging words. Answers are final | §11 "appropriate feedback"; learning from the answer |
| DD-25 | Forgotten passwords | Until an email provider exists (`INF-04`), a Super Admin issues a random temporary password, shown once and audited; the owner must replace it at the next sign-in | §19 user management; no email channel |
| DD-26 | Sensitive actions | Exporting or deleting a child, deleting an account, and admin changes to accounts, settings, programs and age groups need the password proven within `parent.reauth_minutes` (15) | `DD-02`; ASVS V3 re-authentication |
