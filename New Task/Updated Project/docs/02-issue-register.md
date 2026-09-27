# Issue Register — Existing and new issues, kept apart

**Objective:** `OBJ-034` · **Requirement:** [`00-source-requirement.md`](00-source-requirement.md) §20, §27 ·
**Baseline:** `New Task/Current Project/Kids_learn_project/` (read-only; removed after migration on 2026-09-27, `D80`) · **Status:** 🟡 living document;
verification of every `E` issue against the build is in §6 (2026-09-27)

---

## 1. How to read this register

Every issue belongs to exactly one of the five classes that requirement §27 defines. An issue changes class
as work proceeds; it never changes ID.

| Class | Meaning | ID prefix |
|---|---|---|
| **E — Existing issue** | Present in the uploaded baseline. Never reported as a regression | `SEC-E`, `FUN-E` |
| **F — Fixed existing issue** | An `E` issue whose fix is built **and verified** in `Updated Project/`. The row keeps its ID and gains the verification | same ID |
| **N — New enhancement** | Something the requirement adds; not a defect | tracked in the plan, not here |
| **R — New issue introduced during development** | A defect found in the new code | `SEC-R`, `FUN-R` |
| **I — Information or requirement still required** | Cannot be settled from the baseline or the requirement | `INF-` |

**Severity** follows the OWASP risk-rating idea (likelihood × impact) for this application: children's
personal data on a web server.

| Severity | Used when |
|---|---|
| Critical | Remotely exploitable without an account, and reads, alters or destroys data for any user |
| High | Defeats authentication or access control, or exposes credentials |
| Medium | Weakens a control, or helps an attacker chain issues together |
| Low | Defence in depth, or a hygiene issue with limited direct impact |
| Info | No direct exploit; privacy, compliance or design exposure to review |

**References:** OWASP Top 10 (2021) category · OWASP ASVS 4.0.3 requirement where one fits.

## 2. Existing security issues in the baseline (class E)

Found by reading every `.php` file and every `.html` page's scripts. Line numbers refer to the baseline
files. "Latent" means the code path is broken today (a file is missing), but the flaw is in the design and
would go live the moment the gap was filled.

### 2.1 Server side (PHP / MySQL)

| ID | Sev. | Issue | Location | How it can be exploited | OWASP · ASVS |
|---|---|---|---|---|---|
| SEC-E01 | Critical | **SQL injection in the feedback endpoint.** `name`, `rating` and `message` are pasted into the SQL string | `feedback.php:10-15` | Anyone can post `message=x'),('a','5','b` to insert extra rows, or put a subquery in a value (`message=x'),('a','5',(SELECT password FROM stds LIMIT 1))-- -`) to copy password hashes into readable feedback rows. Error- and time-based payloads work too | A03 · V5.3.4 |
| SEC-E02 | Critical | **SQL injection in the progress endpoint, including the column name.** `username` and `progress` are quoted by hand, and `subject` becomes a raw column identifier | `progres.php:9-11,15,20,25` | `subject=alphabets='100',username=(SELECT password FROM stds LIMIT 1)-- -` comments out the `WHERE` and rewrites every row; `username=' OR '1'='1` changes every user's progress. Boolean- and time-based blind payloads in `username` (the `SELECT` on line 15) read other tables | A03 · V5.3.4, V5.3.5 |
| SEC-E03 | High | **No server session at all.** `login.php` checks the password and then only prints `success`. No cookie or token is issued, so no later request can prove who sent it | `login.php:25-26` | Every "logged-in" feature rests on the browser alone (SEC-E05). The server cannot enforce access to anything | A07 · V3.1, V3.2 |
| SEC-E04 | High | **Broken access control on progress (IDOR).** `progres.php` trusts whatever `username` the request carries | `progres.php:9,15-25` | Without logging in, anyone can overwrite any child's progress by posting their username | A01 · V4.1.1, V4.2.1 |
| SEC-E05 | High | **Hard-coded database credentials: the `root` superuser with an empty password.** Repeated in three files instead of one config | `db.php:2` · `feedback.php:3-4` · `progres.php:3` | Full database control for anyone who reaches the MySQL port or any injection point. Breaks least privilege; credentials live in source | A05, A07 · V2.10.4, V14.1 |
| SEC-E06 | Medium | **Error details returned to the browser.** The connection error and raw SQL errors are echoed | `db.php:5` · `progres.php:6,32` | The messages disclose the database host, user, schema and SQL fragments, which makes injection faster to develop | A05 · V7.4.1 |
| SEC-E07 | Medium | **User enumeration.** Distinct messages for an unknown user and a wrong password, and for a username already taken | `login.php:18,28` · `register.php:18` | An attacker learns which usernames exist, then targets them (with SEC-E08) | A07 · V2.2.x |
| SEC-E08 | Medium | **No brute-force protection.** No rate limit, lockout, delay or CAPTCHA on login | `login.php` (whole file) | Unlimited online password guessing; children's passwords are typically short | A07 · V2.2.1 |
| SEC-E09 | Medium | **No password policy.** Registration accepts any non-empty password | `register.php:7-10` | One-character passwords are allowed, which multiplies the effect of SEC-E08 | A07 · V2.1.1 |
| SEC-E10 | Medium | **No input validation.** No type, length, range or allow-list checks (rating 1–5, subject names, lengths) | `feedback.php:10-12` · `progres.php:9-11` · `register.php:4-5` | Oversized or malformed data is stored, and SEC-E02's identifier injection is possible only because `subject` is not allow-listed | A03, A04 · V5.1.3 |
| SEC-E11 | Low | **Missing-field handling.** `$_POST[...]` is read without `isset`, and there is no method check | every `.php` endpoint, e.g. `login.php:4-5` | PHP warnings can disclose file paths if `display_errors` is on; GET requests reach the handlers | A05 · V7.4.1 |
| SEC-E12 | Low | **No CSRF protection on state-changing endpoints** | `register.php` · `feedback.php` · `progres.php` | Any website can make a visitor's browser submit feedback, register accounts or write progress. It becomes High once cookie sessions exist, unless tokens or SameSite cookies are added | A01 · V4.2.2 |
| SEC-E13 | Low | **No unique constraint on usernames.** Uniqueness is checked in code, then inserted: a check-then-act race. No schema was supplied, but the deck's screenshot of the users table (`CleverCubs.pptx` slide 9) **shows two rows with the same username**, so the constraint is indeed absent | `register.php:12-23` | Two simultaneous registrations create duplicate usernames, and `login.php` then verifies against whichever row MySQL returns first | A04 |
| SEC-E14 | Low | **No charset set on the connection** (`set_charset` absent) | `db.php:2` | Mis-encoded data. Charset-based injection tricks become possible if escaping were ever added instead of prepared statements | A03 · V5.3 |

### 2.2 Browser side (HTML / JavaScript)

| ID | Sev. | Issue | Location | How it can be exploited | OWASP · ASVS |
|---|---|---|---|---|---|
| SEC-E15 | High | **Authentication bypass: the only access control is a browser flag.** Pages unlock when `localStorage.loggedIn === "true"` | `second_page.html:429-431` and the checks at `demo_login.html:225`, `feedback1.html:294,371`, `fisrt_page.html:318`, `profil_page.html:334`, `progres_page.html:262`, `progres_page.php.html:266`, `quize_page.html:513`, `second_page.html:372` | Run `localStorage.loggedIn="true"` in the console, or open any page URL directly: every lesson, quiz and page is reachable without an account | A01, A07 · V4.1.1 |
| SEC-E16 | High | **Plain-text passwords stored in the browser by a second, client-only account system.** Six pages register and log in without the server, saving the password in `localStorage` and comparing it in JavaScript | set: `fisrt_page.html:350` · `second_page.html:406` · `quize_page.html:487` · `progres_page.html:308` · `progres_page.php.html:322` · `feedback1.html:330` · `demo_login.html:261`; compared: `fisrt_page.html:359-363` and the matching lines on the other pages | Anyone using the same device, any browser extension, or any script injected into the origin reads the password in clear text. Families often reuse passwords. Two account systems also disagree about who is logged in | A02, A07 · V2.4.1, V8.2.2 |
| SEC-E17 | Medium | **Progress, scores and completion are decided and stored in the browser.** Quiz answers are in the page source, the score is computed client-side, and `localStorage.progress` is trusted | every quiz page, e.g. `alphabets_qq.html:92`; `progres_page.html:341-359` | Anyone can mark every course 100% complete or earn every badge from the console. This defeats requirements §10, §11 and §13 by design | A04 · V11.1 |
| SEC-E18 | Medium | **Stored XSS (latent).** The progress page writes server data straight into `innerHTML`, and `progres.php` stores any string as "progress" for any user (SEC-E04) | `progres_page.php.html:366,385-393` | Post `progress=<img src=x onerror=…>` for a victim's username; the victim's progress page would run the script. Latent because `get_progress.php` was never uploaded | A03 · V5.3.3 |
| SEC-E19 | Medium | **Request bodies built by string concatenation, without URL encoding.** | `index.php:353,374`; the `saveProgress` body in every lesson page, e.g. `alphabets_voice.html:253` | A password with `&`, `+` or `%` is silently altered; a username such as `bob&subject=…` injects extra parameters | A03 · V5.1.1 |
| SEC-E20 | Medium | **No security headers and no HTTPS enforcement.** No CSP, `X-Content-Type-Options`, `frame-ancestors` / `X-Frame-Options`, `Referrer-Policy` or HSTS, and passwords are posted over plain HTTP in the XAMPP setup | all pages | Clickjacking of child-facing pages, easier XSS exploitation, and credentials in transit on shared networks | A05 · V14.4, V9.1 |
| SEC-E21 | Low | **Third-party code and requests at runtime.** A CDN script without Subresource Integrity, and a sound effect fetched from a third-party site | `quize_page.html:450` (`canvas-confetti@1.6.0` from jsDelivr) · `quize_page.html:556` (`assets.mixkit.co` audio) | A compromised CDN copy would run with full page access. Each third-party request also discloses the child's IP address and visit to an outside service | A08 · V14.2.3; privacy |
| SEC-E22 | Low | **Logout does nothing on the server.** It only removes the browser flag | `index.php:391` · `fisrt_page.html:373` | There is nothing to invalidate today (SEC-E03). A future session model must invalidate on logout | A07 · V3.3.1 |
| SEC-E23 | Low | **Username in a GET query string (latent).** | `progres_page.php.html:366` (`get_progress.php?username=`) | Identifiers end up in server logs, browser history and `Referer` headers, and it is the same IDOR as SEC-E04 for reads | A01 · V8.3.1 |

### 2.3 Information exposure and privacy

| ID | Sev. | Issue | Location | Exposure | Reference |
|---|---|---|---|---|---|
| SEC-E24 | Low | **Absolute paths from the authors' machines** reveal Windows user names and folder layout | `frutis_voice.html:142` · `maths_lesson_page.html:162-165` | Personal information of the authors, and broken links (see §3) | A05 · V14.3 |
| SEC-E25 | Medium | **Credentials and personal data in a document inside the web root.** `CleverCubs.pptx`: slide 9 is a screenshot of the users table with usernames, **two plain-text passwords** and six (truncated) password hashes; slide 1 names the team and guide; the file metadata holds an email address | `CleverCubs.pptx` (slides 1, 9; `docProps`) | Anyone who can reach the site can download it. It also shows that an earlier version stored passwords in plain text. **The owner should treat those passwords as compromised wherever they are reused.** The values are deliberately not reproduced in this register | A02, A05 · V8.3; privacy |
| SEC-E26 | Info | **Children's data without privacy controls.** There is no privacy notice, no parental consent, no retention or deletion policy, and no way for a parent to see or delete a child's data | whole application | Child-privacy law in the target jurisdiction (to be confirmed, `INF-`) typically requires verifiable parental consent, data minimisation and deletion rights | requirement §18, §20 |

## 3. Existing functional issues in the baseline (class E)

Each was verified against the file. Where a subagent's first reading was wrong, the verified behaviour is
recorded (see `FUN-E06`).

### 3.1 Broken behaviour

| ID | Sev. | Issue | Location |
|---|---|---|---|
| FUN-E01 | High | **Two account systems that do not interoperate.** A user registered on `index.php` cannot log in on the six client-only pages, and the reverse | `index.php:343-387` vs `fisrt_page.html:344-370` and five copies |
| FUN-E02 | High | **Three parallel quizzes per subject, with pass marks of 50%, 70% and 80%.** Two of them write to the same progress entry, so the last one played wins | `animal_qq.html:125` · `alphabets_quize.html:227` · `alphabets_qq.html:89` |
| FUN-E03 | Medium | **Server progress is written but never read.** Every card tap posts to `progres.php`, while the progress page shows only `localStorage`; the two copies drift apart | `alphabets_voice.html:244-258` · `progres_page.html:337-361` |
| FUN-E04 | Medium | **Dead links to files that do not exist:** `index.html` (from `index.php:212`, `progres_page.html:185`, `progres_page.php.html:185`, `feedback1.html:203,241`); `progress.html` (the "View My Badges" button in 7 of 8 lesson quizzes, e.g. `alphabets_quize.html:242`); `learning.html` (the hub quizzes' lock screen, e.g. `animal_qq.html:79`); `body_quiz.html` (`body_parts_voice.html:189`); `get_progress.php` (`progres_page.php.html:366`) | as listed |
| FUN-E05 | Medium | **The body-parts quiz is unreachable from its lesson.** The lesson links to `body_quiz.html`; the real file `body_part_quize.html` has no incoming link | `body_parts_voice.html:189` |
| FUN-E06 | Medium | **Body-parts audio never plays.** Hotspots call `showInfo(name, desc)` with two arguments; the function expects three and sets `audio.src = undefined` | `body_parts_voice.html:147-178` vs `:215-222` |
| FUN-E07 | Low | **One rhyme line shows "false".** A stray `!` in `"JOhnny, Johnny",!` turns the next line into `!"Yes, Papa?"`, which is `false`. The script still runs (a first reading reported a syntax error; it is not one) | `poem_video2.html:258` |
| FUN-E08 | Medium | **The apple video uses an absolute path from an author's machine**, so it never loads anywhere else. `maths_lesson_page.html` has four nav links of the same kind | `frutis_voice.html:142` · `maths_lesson_page.html:162-165` |
| FUN-E09 | Low | **"Claim reward" can never appear for Alphabets or Numbers.** Their quizzes never set `sessionStorage.lastCompleted` | `alphabets_qq.html:89-91` · `num_quiz.html` |
| FUN-E10 | Low | **Rhymes and stories are listed as progress subjects but never recorded** | `second_page.html:444` |
| FUN-E11 | Low | **Profile name is hard-coded "Clever Cub"**, and the mood picker is not saved | `profil_page.html:265` |
| FUN-E12 | Low | **Home-page topic cards look clickable but do nothing** (no handler) | `index.php:236-263` |
| FUN-E13 | Low | **Wrong title:** the orphan alphabet prototype is headed "Funny Colors Quiz" | `alphabets_q.html:138` |

### 3.2 Responsive design and accessibility

| ID | Sev. | Issue | Location |
|---|---|---|---|
| FUN-E14 | High | **14 of 44 pages have no viewport meta tag**, including every lesson page and the Learning hub, so phones render them at desktop width | `alphabets_voice.html`, `animal_voice.html`, `birds_voice.html`, `body_parts_voice.html`, `color_voice.html`, `flowers_voice.html`, `frutis_voice.html`, `number_voice.html`, `vegitables voice.html`, `second_page.html`, `poem_video2.html`, `story.html`, `maths_lesson_page.html`, `great_job_page.html` |
| FUN-E15 | Medium | **Fixed widths overflow small screens:** the login modal is `width: 380px`, and the body diagram is 500 × 800 px with no breakpoint | the modal copies (e.g. `second_page.html`); `body_parts_voice.html:56-57` |
| FUN-E16 | Medium | **Lesson cards cannot be used from a keyboard.** They are `<div onclick>`, with no `tabindex`, `role` or key handler | e.g. `alphabets_voice.html:130`; `poem_video2.html:168`; `story.html:135` |
| FUN-E17 | Medium | **Images without `alt` text:** 221 `<img>` tags, only 116 `alt` attributes. `birds_voice.html` labels 1 of 22 | e.g. `birds_voice.html:135`, `animal_voice.html:147` |
| FUN-E18 | Medium | **Text colour depends on a background video.** White or red text with no page background colour becomes unreadable when the video does not load | `alphabets_voice.html:7` · `animal_voice.html:8` · `frutis_voice.html:8` |
| FUN-E19 | Low | **No `prefers-reduced-motion` support.** Looping background videos, hover transforms and confetti always run | all pages |

### 3.3 Maintainability and dead code

| ID | Sev. | Issue | Location |
|---|---|---|---|
| FUN-E20 | Medium | **Everything is duplicated in every page:** the header, footer and styles on all 44, and the login modal with its ≈50 lines of script on 7. There is no shared CSS or JS file | all pages |
| FUN-E21 | Medium | **11 orphan pages (25%)** that nothing links to: the six `<topic>_q.html` prototypes, `body_part_quize.html` (see `FUN-E05`), `progres_page.php.html`, `great_job_page.html` (a static "4 out of 5" screen with dead buttons), `demo_login.html` (a seventh login modal) and `maths_lesson_page.html` (four titles, dead buttons, absolute paths) | as listed |
| FUN-E22 | Low | **Every card tap posts progress**, logs the reply to the console and ignores failures | `alphabets_voice.html:244-258` and 8 copies |
| FUN-E23 | Low | **Leftover template comments** such as `// ADD THIS LINE BELOW:` and `// ... rest of code` | `animal_qq.html:127-132` and the other hub quizzes |
| FUN-E24 | Low | **Misspelt, inconsistent file names** (`frutis`, `vegitables`, `fisrt`, `progres`, `quize`, `num_q` vs `<topic>_q`; spaces and double spaces) | throughout |
| FUN-E25 | Low | **Only 21 of 50 pages declare `<!DOCTYPE html>`**; the rest render in quirks mode | e.g. the lesson pages |

### 3.4 Media and performance

Measured with an ISO-BMFF parser and file headers (all 184 audio and video files parsed; 0 failures).

| ID | Sev. | Issue | Evidence |
|---|---|---|---|
| FUN-E26 | High | **Huge background videos autoplay on page load.** 18 pages autoplay a muted, looping background. `birds_voice.html` loads `birds.mp4` (54.96 MB, 5 min 15 s); `vegitables voice.html` loads `vegitables.mp4` (48.87 MB, 7 min 5 s). Eager weight is 56.85 MB and 50.40 MB before a child taps anything | the `#bgVideo` tags; per-page weights in `01-baseline-analysis.md` §11 |
| FUN-E27 | Medium | **13.31 MB of audio tracks inside muted background videos** that are never heard | 7 of the 9 background files |
| FUN-E28 | Medium | **No `preload`, `poster` or `loading="lazy"` anywhere**, so the browser decides, and every card image loads at once | all 25 media pages |
| FUN-E29 | Medium | **Oversized images for small cards:** 8 images over 300 KB shown at about 200 px (5.51 MB in total), e.g. `juice emoji.jpg` at 3000×4500 for a 200×200 card. `logo.png` (225 KB, 500×500) is shown at 60–80 px on 43 pages | image headers |
| FUN-E30 | Medium | **A story video is missing:** "The Capseller and the Monkeys" has a card and a thumbnail, but its video was never uploaded | `story.html:185` (`INF-09`) |
| FUN-E31 | Low | **20 orphan media files (4.01 MB)** that no page uses, and one byte-identical duplicate (`larlic photo.jpg` = `garlic1 photo.jpg`) | reference map |
| FUN-E32 | Low | **All 115 audio clips store their index after the data** (not "faststart"), so playback waits for the whole file. The clips are small (1–10 s), so the effect is minor | MP4 box order |

## 4. Issues introduced during development (class R)

Defects found in the new code. Fixed ones keep their row so the history stays honest.

| ID | Severity | Issue | Status |
|---|---|---|---|
| SEC-R01 | Low | **Registration says when an email address is already registered** (`email-taken`), which lets someone test whether an address has an account. The sign-in itself reveals nothing (`SEC-E07` fixed) | ⚠️ Open by choice (`DD-22`): a silent failure would leave a real parent unable to tell why they cannot register. Mitigation options: per-address throttling of registration, or an email-verification flow once an email provider exists (`INF-04`) |
| FUN-R01 | Medium | Opening the quiz page started a try at once, so visiting or reloading it used one of the three tries without the child choosing to | ✅ Fixed before release: a read-only `GET /learn/quizzes/{id}` overview; only "Let's go" starts a try (`QuizAttemptTests.overviewUsesNoAttempt`) |
| FUN-R02 | Low | A suggested username could contain the child's own first name (for "Kit": `happy-kitten-42`), which the server's own rule then refused | ✅ Fixed: suggestions are checked against the child's name (`RegistrationTests.suggestionsRespectTheChildsName`); found by the browser tests |
| FUN-R03 | Low | Pressing Enter in a password dialog chose "Cancel" (the first submit button) | ✅ Fixed: Cancel is a plain button; Enter confirms |
| FUN-R04 | Low | The celebration animation widened a 375 px phone page by 2–3 px for a second | ✅ Fixed in two steps: the layer contains its paint; then (2026-09-27) the card "pop" became a small hop instead of a 6% scale, which had pushed the card's sticker past the edge of the screen (`e2e` responsive check, repeated against the cloud image) |
| FUN-R05 | Low | Sessions were held in the server's memory, so a restart signed everyone out | ✅ Fixed: sessions are kept in the database in development and in the cloud (`DD-28`, `JdbcSessionTests`) |
| FUN-R06 | Medium | Found while adding PostgreSQL (`D73`), before any release: there, an email address or username typed in other letter case would not have matched (sign-in refused, a taken username reported as free) | ✅ Fixed before release: `SqlDialect.caseInsensitive` and `CITEXT` columns (`RegistrationTests.identitiesIgnoreLetterCase`, run on both databases) |
| FUN-R07 | Medium | Found by the browser journeys against the live deployment: on the sign-in and registration pages the button worked before the page's script had attached its handler, which on a slower connection takes the time of one or two requests. A click then made the browser submit the form itself: the page reloaded, everything typed was lost, and, as the forms named no method, the fields went into the address as a GET | ✅ Fixed (2026-09-27): both buttons ship disabled and are enabled by the script once it handles the form, and both forms say `method="post"`. Proof: the `e2e/` journeys, which failed at this click on production and pass there now |
| FUN-R08 | High | Found in `OBJ-036`: all three clubs saw the same 11 courses. The seeder put every course into every Year-1 program (`DD-20`). No course, lesson, card or quiz endpoint checked the child's program, so a two-year-old could open any course by its address | ✅ Fixed (2026-09-27, `D78`/`DQ-13`): each club has its own set, `V5` replaced the old rows, and every child endpoint answers `404` outside the child's program. Proof: `ClubProgramsTests` (exact disjoint sets; ages 3, 5 and 7; a Tiny Cub refused a Little and a Big course, lesson, card and quiz, with nothing recorded) |

## 5. Information or requirements still required (class I)

Owner decisions awaiting an answer are in [`03-decisions.md`](03-decisions.md) §2. The items below are
missing facts or material. Each is built as a clearly marked, configurable placeholder, never an invented
value.

| ID | Needed | Why it matters | Placeholder until supplied |
|---|---|---|---|
| INF-01 | **Content for age groups the baseline does not cover**, and for a "next-year" program (§5, §16) | The baseline content is toddler and pre-school level | The 11 courses are split across the three clubs (`DQ-13`), so Big Cubs has only 3. Clubs past Year 1 say the program is being prepared |
| INF-02 | ✅ **Resolved (2026-09-27, `D80`).** Contact Us details (§17) | Must not expose personal details (§17) | The owner supplied two addresses. `CC_CONTACT_EMAIL` now holds a comma-separated list, and the Contact page shows each one (`CleverCubsPropertiesTests`, `PagesAndMediaTests`). No phone number is shown |
| INF-03 | **Legal review** of the Terms & Conditions, privacy notice, consent wording and retention periods (§18, §20) | Children's personal data; compliance is never claimed without review | Drafts marked "Draft — requires legal review" on every page that shows them |
| INF-04 | **An email or SMS provider**, if the parent is to be reached outside the app (DQ-10), including password reset | Without one, a parent who forgets their password cannot reset it alone | In-app flows only; password reset is admin-assisted and audited |
| INF-05 | **Hosting target**: domain, HTTPS, production database (§8, §20) | `Secure` cookies and HSTS need HTTPS; production credentials need a secret store | Local development profile; production settings documented and read from the environment |
| INF-06 | **Colleague and review feedback** (§1). None was uploaded; the owner confirmed that everything available is in the baseline folder | Future feedback may change priorities | Treated as none; the plan leaves room for it |
| INF-07 | **Certificate wording and design** (§12, §13), and who issues it | Shown to parents; must not make unsupported claims (§16) | A neutral "Certificate of completion" template marked for review |
| INF-08 | **Maths course content.** The baseline has four lesson titles and nothing behind them (`maths_lesson_page.html`) | A listed course with no content would mislead | Not published as a course until content exists |
| INF-09 | **The video for "The Capseller and the Monkeys"** (`FUN-E30`) | The story card exists, but its video was never uploaded | The lesson is marked "coming soon" and excluded from progress until the file exists |
| INF-10 | **Audio for the body-parts course.** No body-part audio files exist in the upload (`FUN-E06`) | Every other course has audio | The course works with text and images; audio slots are ready for files |
| INF-11 | **Licences for the lesson media.** Some baseline pictures look like stock images (the body-parts picture carries a stock-site watermark), and the rhyme and story videos have no recorded source | Publishing media without a licence is a legal risk (§18 review areas) | Media is used as uploaded; the Terms list content licences as a review item |

## 6. Verification of the existing issues against the build (E → F)

Checked on 2026-09-27 against the running build and the automated tests (`app/`: JUnit, 219 tests, on
MySQL and on PostgreSQL; 228 after `OBJ-036`, all passing again; `e2e/`: Playwright, desktop and phone). ✅ = fixed and verified (class F), 🟡 = partly fixed, ⚠️ = still open
with its reason, ℹ️ = waiting for information.

| ID | Status | How it is closed, and the evidence |
|---|---|---|
| SEC-E01 | ✅ | All SQL uses bound parameters (`JdbcClient`); `RegistrationTests.injectionPayloadsAreJustText` stores `'); DROP TABLE child;--` as text |
| SEC-E02 | ✅ | No column name comes from a request; progress is calculated by the server (`LearningFlowTests`) |
| SEC-E03 | ✅ | Server sessions, rotated at sign-in (`AuthenticationTests`) |
| SEC-E04 | ✅ | Ownership checked in every service; another family's child or quiz try is "not found" (`ParentAreaTests.otherFamiliesAreInvisible`, `QuizAttemptTests.attemptsArePrivate`, `LearningFlowTests.noChildModeForSomeoneElsesChild`) |
| SEC-E05 | ✅ | Two least-privilege database users, credentials from the environment (`DatabaseSetupTests`) |
| SEC-E06 | ✅ | problem+json without internals; `server.error.include-*` off (`SecurityConfigurationTests`) |
| SEC-E07 | ✅ | One message and equal cost for every refusal (`AuthenticationTests`); registration is `SEC-R01` |
| SEC-E08 | ✅ | Five failures lock the account for 15 minutes; per-address throttle (`LoginLockTests`, `PasswordAndThrottleTests`) |
| SEC-E09 | ✅ | 12 characters, a common-password list, no email or app name (`PasswordPolicy`, `RegistrationTests.weakPasswordsAreRefused`) |
| SEC-E10 | ✅ | Bean Validation on every body plus service rules; field errors named (`RegistrationTests.incompleteRegistrationIsInvalid`, `AdminTests.settingsChange`) |
| SEC-E11 | ✅ | Missing or unreadable fields are a 400 `invalid-input` |
| SEC-E12 | ✅ | CSRF token in a header on every state-changing call (`SecurityConfigurationTests.postWithoutCsrfTokenIsRefused`) |
| SEC-E13 | ✅ | `UNIQUE` email and username plus a service check (`RegistrationTests.takenUsernameIsRefused`) |
| SEC-E14 | ✅ | `utf8mb4` everywhere; 4-byte emoji content is stored and served (numbers course) |
| SEC-E15 | ✅ | Pages are protected on the server; no browser flag exists (`PagesAndMediaTests.protectedPagesRedirect`) |
| SEC-E16 | ✅ | Nothing sensitive in browser storage (no `localStorage` use at all) |
| SEC-E17 | ✅ | Scores, progress and rewards decided by the server; correct answers are not sent before an answer (`QuizAttemptTests.correctAnswersAreNotSentUpFront`) |
| SEC-E18 | ✅ | Every value is written with `textContent`; strict CSP; `<b>`/`<script>` strings show as text (`e2e` feedback step) |
| SEC-E19 | ✅ | Bodies are `JSON.stringify` objects (`js/api.js`) |
| SEC-E20 | ✅ | CSP, `nosniff`, `frame-ancestors 'none'`, `Referrer-Policy` (`SecurityConfigurationTests.securityHeadersArePresent`). HTTPS and HSTS come from the host: on the production deployment (2026-09-27) every page answers over HTTPS with `Strict-Transport-Security: max-age=31536000; includeSubDomains`, and the cookies are `Secure` (checked with `curl -D -`; `07-deployment.md` §9) |
| SEC-E21 | ✅ | No third-party request at runtime; fonts self-hosted; `default-src 'self'` |
| SEC-E22 | ✅ | Sign-out invalidates the session (`AuthenticationTests.signOutInvalidatesTheSession`) |
| SEC-E23 | ✅ | Identity comes from the session; ids in page addresses are ownership-checked |
| SEC-E24 | ✅ | Media paths are relative and validated by the seeder; traversal is refused (`PagesAndMediaTests.mediaForSignedInUsers`) |
| SEC-E25 | ✅ | The deck is not part of the new project, and the baseline folder is kept out of the repository (`D72`) |
| SEC-E26 | 🟡 | Consent records, data minimisation, export and delete, no tracking, legal drafts flagged; the legal review itself is `INF-03` |
| FUN-E01 | ✅ | One account system on the server |
| FUN-E02 | ✅ | One quiz per course at a 70% pass mark (`DD-18`, `D62`) |
| FUN-E03 | ✅ | Every progress view reads the server |
| FUN-E04 | ✅ | All links are internal and exist (`e2e` public pages) |
| FUN-E05 | ✅ | Every quiz opens from its course page |
| FUN-E06 | 🟡 | No body-part audio exists (`INF-10`); the word and its description are read aloud by the browser instead, and the picture highlights the part |
| FUN-E07 | ✅ | The lyric line is recovered by the extraction ("Yes, Papa?") |
| FUN-E08 | ✅ | The apple video uses the media library |
| FUN-E09 | ✅ | Badges are awarded by the server |
| FUN-E10 | ✅ | Rhymes and stories are courses with progress and a completion badge |
| FUN-E11 | ✅ | The profile shows the child's own nickname and avatar |
| FUN-E12 | ✅ | Every course card opens its course |
| FUN-E13 | ✅ | The prototype pages are not carried forward (`D68`) |
| FUN-E14 | ✅ | Every page has a viewport meta tag |
| FUN-E15 | ✅ | No horizontal scrolling at 1440, 1024, 768 and 375 px (`e2e`) |
| FUN-E16 | ✅ | Cards are real buttons with a visible focus ring |
| FUN-E17 | ✅ | Every picture has alt text from the content; decorative images have empty alt |
| FUN-E18 | ✅ | Explicit background and text colours; no background video |
| FUN-E19 | ✅ | `prefers-reduced-motion` disables animation and the celebration |
| FUN-E20 | ✅ | One stylesheet and shared script modules |
| FUN-E21 | ✅ | Orphan pages not carried forward |
| FUN-E22 | ✅ | Views are idempotent; failures are shown to the child |
| FUN-E23 | ✅ | No template leftovers |
| FUN-E24 | ✅ | Media renamed to lower-case, hyphenated names (`media/MEDIA-MAP.csv` keeps the old names) |
| FUN-E25 | ✅ | Every page declares `<!doctype html>` |
| FUN-E26 | ✅ | Background videos removed (`D68`); the heaviest lesson now loads 385 KB before any tap instead of 56.85 MB |
| FUN-E27 | ✅ | Gone with the background videos |
| FUN-E28 | ✅ | `loading="lazy"` on pictures, `preload="metadata"` and posters on videos |
| FUN-E29 | ✅ | The 230 KB logo is now 12 KB. `tools/optimize_media.py` resized the 17 heavy pictures to twice their display size in their own format (cards 320 px, video posters 1280 px): 4.78 MB lighter, e.g. `juice-emoji.jpg` 621 → 11 KB. No path changed (`media/OPTIMISED.csv`). One poster PNG is kept, because re-encoding saves under 20% (`MediaWeightTests.cardPicturesAreSmall`) |
| FUN-E30 | ℹ️ | The missing story is marked "coming soon" and does not count (`INF-09`) |
| FUN-E31 | ✅ | Only media the content uses was copied (305 files, 423 MB) |
| FUN-E32 | ✅ | All 110 sound and video files that had their index after the data were remuxed with the index first by `tools/optimize_media.py` (ffmpeg stream copy: same streams, same length, verified with ffprobe) (`MediaWeightTests.soundAndVideoStartFast`) |
