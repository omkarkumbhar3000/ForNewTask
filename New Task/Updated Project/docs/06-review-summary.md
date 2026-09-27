# Review Summary — What the enhanced CleverCubs delivers, and what is still open

**Objective:** `OBJ-034` · **Requirement:** [`00-source-requirement.md`](00-source-requirement.md) §29 Phase 6 ·
**Date:** 2026-09-27 · **Status:** ✅ build complete, verified locally and live at https://clevercubs.vercel.app (§7)

---

## 1. In one paragraph

The PHP site with 44 hand-written pages became one Java application (Spring Boot 4.1, MySQL 8.4) with
about 20 data-driven pages. Parents register with their first child and give consent; a child learns in a
session the parent opens, without a password. Progress, quiz tries, badges, certificates and the year
summary are all decided by the server. A Super Admin dashboard manages accounts, content, wording, settings
and feedback, with an audit trail. Every piece of baseline content was migrated (11 courses, 53 lessons,
189 cards, 90 quiz questions, 305 media files), and the application no longer depends on the old folder.

## 2. What changed

| Area | Before (baseline) | Now |
|---|---|---|
| Backend | 6 PHP endpoints, SQL built from strings, `root` with no password | Java 25, Spring Boot 4.1, bound SQL only, two least-privilege database users, Flyway migrations |
| Accounts | Two account systems that do not talk to each other; passwords in the browser | One parent account (bcrypt, cost 12); children have no password and are opened from the parent's session |
| Access | A browser flag unlocks pages | Server sessions, CSRF, RBAC for Child, Parent and Super Admin, protected pages redirect to sign-in |
| Learning | 44 pages of cards, three quizzes per topic with 50%, 70% and 80% pass marks | 11 courses of short lessons, one quiz per topic at 70%, progress 70% lessons + 30% quiz, three tries then a parent grant |
| Rewards | A "claim reward" button that rarely appeared | Badges at a best score of 80% or more, completion badges, a year certificate, no leaderboards |
| Parents | None | Dashboard, child progress with every quiz try, requests inbox, feedback, year summary with next-year choice, data export and deletion |
| Admin | None | Accounts (disable, unlock, temporary password), children, courses, lessons, cards, quizzes, programs, age groups, badges, wording, feedback, reports, settings, audit trail |
| Design | Background videos under every page, fixed widths, no keyboard use | One light design system, self-hosted fonts, responsive to 375 px, keyboard and screen-reader friendly, reduced-motion respected |
| Weight | Heaviest lesson 56.85 MB before any tap | 385 KB; the welcome page 141 KB; other pages 26–36 KB (`e2e/measure.mjs`) |

## 3. What was preserved

Every topic, card, picture, sound, rhyme with its lyrics, story and quiz question of the baseline; the
baseline's own progress rule (70% for lessons, 100% after the quiz, `D61`); the lesson-linked quiz banks
(the other two banks are kept as a reserve pool, `DD-18`); the body-parts picture with its clickable areas;
the brand logo and the green brand colour. Spelling fixes to displayed words keep the original text in the
content files (`sourceWord`).

## 4. Requirement by requirement

| § | Requirement | Where it is met | Evidence |
|---|---|---|---|
| 1, 4, 29 | Understand the baseline first; enhanced version in `Updated Project/` | `01-baseline-analysis.md`, `02-issue-register.md`; the app, content and media all in `Updated Project/` | This document; the app runs without the old folder |
| 2, 24 | Child-friendly, simple, light theme, purposeful animation | Design system `css/app.css`; one celebration on success; age-adaptive pages | Browser review at 1440 and 375 px |
| 3, 31 | Ask before material decisions | `D56`–`D75`; defaults `DD-01`–`DD-29` documented | `03-decisions.md` |
| 5 | Age groups from the date of birth; experience adapts | Bands 2–3, 4–5, 6–8 as data; `ui_profile` drives size, wording, stars or numbers | `ChildRulesTests`, `LearningFlowTests.homeStartsAtZero` |
| 6 | Parent and child registration, mandatory and optional fields | `register.html`, `RegistrationService` (`DD-09`) | `RegistrationTests` (11) |
| 7 | Parent → child → courses → progress; escalation to the parent | Child mode (`D58`), "Ask a grown-up" requests, parent inbox (`D59`) | `QuizAttemptTests.parentGrantsMoreAttempts`, `ParentAreaTests.usernameRequest`, `e2e` |
| 8 | Authentication, sessions, RBAC, protected URLs redirect to login, backend authorisation | `SecurityConfig`, `SessionAuthentication`, ownership checks | `AuthenticationTests`, `SecurityConfigurationTests`, `PagesAndMediaTests`, `LoginLockTests` |
| 9 | Course cards, descriptions, progress, resume | Child home, course and lesson pages; "Continue" target | `LearningFlowTests` |
| 10 | Progress by the backend; never 100% before the quiz | `ProgressRules`, `ProgressService` | `ProgressRulesTests`, `LearningFlowTests.lessonsAloneStopAtSeventy` |
| 11 | Three tries per quiz, enforced by the backend; attempt number, remaining, score | `QuizService` (row lock), quiz page | `QuizAttemptTests` (12), browser check of a 4th try refused |
| 12 | Profile: username, nickname, avatar, summaries, badges, preferences | Parent child page (edit), child profile page | `ParentAreaTests.addAndEditChild` |
| 13 | Rewards at "above 80%", no leaderboards | `RewardService` (`D64`, `DD-21`) | `QuizAttemptTests.passMarkAndRewardLineAreSeparate` |
| 14 | Encouraging, age-appropriate messages | `ui_message` rows per age group, editable by the admin | Browser review |
| 15 | Parent feedback, admins only | `FeedbackService`; admin Feedback section | `ParentAreaTests.feedbackVisibility` |
| 16 | One-year completion summary; the parent decides about next year | Year summary page, certificate, next-year choice | `ParentAreaTests.completingTheYear` |
| 17 | Contact Us, clearly visible | Footer on every page; `contact.html` | `e2e` public pages |
| 18 | Terms & Conditions, flagged for legal review | `terms.html`, `privacy.html` marked draft | `INF-03` |
| 19 | Super Admin dashboard, RBAC, protected sensitive actions, audit | `/admin/`, `AdminService`, recent-password rule (`DD-26`) | `AdminTests` (8) |
| 20 | Security list | See `02-issue-register.md` §6 (every baseline issue with its test) | 219 JUnit tests |
| 21 | Java, clean architecture, justified dependencies | Packages by feature, no ORM, no Lombok, no JS framework | `pom.xml` (7 runtime starters) |
| 22 | Schema from the requirements, proposed first | `05-data-model.md` (approved with `D68`), migrations V1–V4, a PostgreSQL copy for the cloud (`D73`) | `DatabaseSetupTests` on both databases |
| 23 | Desktop first, responsive, mobile-ready APIs | Versioned JSON API; responsive pages | `e2e` at 1440, 1024, 768, 375 px |
| 25 | Measured performance work | See §2 "Weight" and §6; lighter media (`DD-29`) | `e2e/measure.mjs`, `MediaWeightTests` |
| 26 | Maintainable | One stylesheet, shared modules, docs per area, `README.md` | — |
| 27 | Existing issues kept apart from new ones | `02-issue-register.md` §2–§6 | — |
| 28 | Test the listed flows | JUnit (219, on MySQL and on PostgreSQL) and Playwright (6 journeys) | §5 |
| 30 | Git: check media, LFS, secrets, generated files before committing | `.gitignore`, LFS rules for `media/` | §7 |

## 5. How it was tested

| Level | What | Result |
|---|---|---|
| Unit | Progress, quiz, reward, age-group, username and password rules; throttle; media weight (`MediaWeightTests`) | ✅ |
| Integration (Testcontainers MySQL 8.4) | Registration, sign-in, lock, sessions, child mode, lessons, quizzes (limit, lock, grant, resume, simultaneous starts), rewards, year completion, parent area, admin, pages and media, security headers, CSRF, IDOR, injection strings | ✅ 219 tests, 0 failures (`mvnw verify`) |
| The same suite on PostgreSQL 17 (`-Dclevercubs.test.db=postgresql`, `D73`) | Everything above, plus database sessions over a real server and letter case in email addresses and usernames | ✅ 219 tests, 0 failures |
| Browser (Playwright, installed Chrome) | Public pages at four widths without script errors; protected URLs; register → child mode → lesson → ask a grown-up → parent gate → requests → progress → feedback → delete the account; at 1440 and 375 px | ✅ 6 of 6 against the development server (MySQL) and ✅ 6 of 6 against production, https://clevercubs.vercel.app (Neon PostgreSQL) |
| Manual browser review | Every page of the three areas, the quiz with a wrong answer, the lock after three tries, the admin dashboard | ✅ found and fixed `FUN-R01`–`FUN-R04` |

## 6. Performance (measured on the local build)

| Page | Downloads before any tap | Requests |
|---|---:|---:|
| Welcome (first visit, fonts included) | 141 KB | 13 |
| Sign in | 26 KB | 5 |
| Parent dashboard | 28 KB | 6 |
| Child home, 11 courses | 33 KB | 7 |
| Birds lesson 1 (baseline: 56.85 MB) | 385 KB | 13 |
| Rhyme video lesson (video streams on play) | 153 KB | 8 |

Every API answer measured took under 50 ms locally. Videos stream with byte ranges (`206`), pictures load
lazily, and media is cached for a week; pages, scripts and styles revalidate (`304`) so an update is never
hidden.

The media library itself is lighter (`DD-29`): the 17 heaviest pictures were resized to twice their
display size (4.78 MB saved; every card picture is now at most 100 KB, the largest was 621 KB), and the 110
sound and video files that stored their index after the data now store it first, so playback starts
before the whole file has arrived.

## 7. Deployment

Local: `start-dev.ps1` (see `README.md`). **Production: https://clevercubs.vercel.app**, a container on
Vercel built from GitHub `main`, with PostgreSQL from Neon (`D73`). It was verified on 2026-09-27: health,
security headers and HSTS, access control, the six browser journeys, and a read-only check of the cloud
database ([`07-deployment.md`](07-deployment.md) §9). Every push to `main` deploys it. The first Super
Admin is set up with the owner's own password, and the temporary credential is deleted from Vercel.

## 8. What remains, and what needs the owner

| Item | Needed from | Detail |
|---|---|---|
| A faster first visit after an idle spell | Later | Vercel stops an idle instance after 5 minutes, and the application then takes about 15 s to start. Faster start-up (Spring AOT or class-data sharing) or a paid plan's always-on instance would remove it |
| The repository is public | Owner (accepted for now, `D74`) | The media files are publicly downloadable from GitHub while their licences are unconfirmed (`INF-11`) |
| Contact address (`INF-02`) | Owner (unset by choice, `D75`) | Set `CC_CONTACT_EMAIL` on the Vercel project when an address should be shown; until then the page says it is being set up |
| Legal review (`INF-03`) | Owner / counsel | Terms, privacy notice, consent wording, retention, target country |
| Email provider (`INF-04`) | Owner | Self-service password reset and request notifications; until then admins issue temporary passwords (`DD-25`) |
| Content for 6–8 and a Year 2 (`INF-01`) | Owner | The next-year screen says the program is being prepared |
| The missing story video (`INF-09`), body-parts audio (`INF-10`) | Owner | Shown as "coming soon" / read aloud by the browser |
| Media licences (`INF-11`) | Owner | Some pictures look like stock images (one carries a watermark) |
| Certificate wording (`INF-07`) | Owner | A neutral draft is shown |
| `DD-20`–`DD-29` | Owner review | Defaults chosen during the build; each can be changed |

## 9. Assumptions made

No baseline user data exists to migrate (`D68`); the baseline content is the whole Year-1 program for every
age group (`DD-20`); children aged 9 and above keep the oldest band's presentation; a video counts as watched
at 90% (`DD-17`); "Mark as seen" is the parent's answer to a help request.

## 10. Recommendations

1. An email provider, for password reset, request notifications and email verification at registration
   (which also closes `SEC-R01`).
2. A Year-2 program and content for the 6–8 band, so the next-year choice leads somewhere.
3. Re-encode the videos at a child-appropriate bitrate (likely 40–60% less data). That changes what the
   child sees and hears, so it needs the owner's review; the pictures are already resized (`DD-29`).
4. Two-factor sign-in for Super Admins.
5. A PWA with offline lessons, and translations (the wording is already data).
