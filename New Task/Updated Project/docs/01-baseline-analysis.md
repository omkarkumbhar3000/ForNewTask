# Baseline Analysis — The uploaded CleverCubs project, as it is

**Objective:** `OBJ-034` · **Requirement:** [`00-source-requirement.md`](00-source-requirement.md) §4, §29
(Phases 1–2) · **Baseline:** `New Task/Current Project/Kids_learn_project/` (read-only, never modified) ·
**Status:** ✅ Phases 1–2 complete (2026-09-26)

This document answers the twelve points of requirement §4 from the files themselves. Every claim cites a
file; where the baseline is silent, it says so. Issues found here are registered once, in
[`02-issue-register.md`](02-issue-register.md), and referenced by ID.

---

## 1. What the baseline is

| Measure | Value |
|---|---|
| Product | "CleverCubs — an interactive learning platform for toddlers" (`CleverCubs.pptx` slide 1), a student project |
| Layout | One flat folder with no subfolders, build, package manifest, tests or separate `.js` / `.css` files |
| Files | 388: 44 `.html`, 6 `.php`, 1 `.pptx`, 337 media files |
| Size | 579 MB, almost all of it media |
| Code | 12,334 lines of HTML and PHP. The styles and scripts are inline in each page |
| Stack | Browser pages (HTML, CSS, vanilla JavaScript) and PHP 7+ endpoints on MySQL (`mysqli`), in an XAMPP-style setup (`localhost`, `root`, empty password) |
| External code | One CDN script: `canvas-confetti@1.6.0` from jsDelivr (`quize_page.html:450`) |
| Language | English UI; code comments in Marathi, written in Latin script |
| Requirements material | `CleverCubs.pptx`: 22 slides with the problem statement, objectives, an ER diagram, table screenshots, UI screenshots and future scope. Plus the owner's requirement ([`00-source-requirement.md`](00-source-requirement.md)). No separate colleague-feedback document was uploaded (`INF-06`) |

## 2. Page structure and navigation (§4.2, §4.4)

Every page repeats the same header: a logo, five nav links (Home, Learning, Quizzes, Progress, Profile), a
Feedback button and Login/Logout. It also repeats the same footer. The links form this graph:

```text
index.php ─┬─ fisrt_page.html (a second copy of the home screen)
           ├─ second_page.html  "Learning" hub: 11 cards
           │     ├─ <topic>_voice.html  ×9 lessons ──"Try Quiz?"──► <topic>_quize.html  ×8, and num_quiz.html
           │     ├─ poem_video2.html    9 rhymes (video + lyrics)
           │     └─ story.html          6 stories (video)
           ├─ quize_page.html   "Quizzes" hub: 9 cards ──► <topic>_qq.html ×8, and num_quiz.html
           ├─ progres_page.html "Progress": bars and badges from localStorage
           ├─ profil_page.html  "Profile": emoji avatar, mood, stats
           └─ feedback1.html    star rating + message ──► feedback.php
```

**11 of the 44 pages (25%) are orphans that nothing links to:** the six `<topic>_q.html` prototypes,
`body_part_quize.html`, `progres_page.php.html`, `great_job_page.html`, `demo_login.html` and
`maths_lesson_page.html`. Details and the obsolete-or-not verdict are in §9.

## 3. Login and registration (§4.3)

The baseline has **two independent account systems that do not know about each other.**

| | System 1 — server | System 2 — browser only |
|---|---|---|
| Where | `index.php` (the entry page; plain HTML despite the extension) | A copy of the same modal in `fisrt_page.html`, `second_page.html`, `quize_page.html`, `progres_page.html`, `progres_page.php.html`, `feedback1.html`, `demo_login.html` |
| Register | `fetch("register.php")`, which checks the username is free and stores a `password_hash()` in table `stds` (`register.php:12-25`) | Saves `username` and `password` in plain text in `localStorage` (`fisrt_page.html:344-353`) |
| Login | `fetch("login.php")` runs `password_verify()`, which prints `success` (`login.php:12-29`); the page then sets `localStorage.loggedIn = "true"` | Compares the typed password with the one in `localStorage` (`fisrt_page.html:356-370`) |
| Session | **None.** No cookie, token or `session_start()` anywhere | None |
| Logout | Removes `loggedIn` (and `username`) from `localStorage` (`index.php:389-395`) | Removes `loggedIn` (`fisrt_page.html:372-376`) |
| Gate | Pages lock their cards unless `localStorage.loggedIn === "true"` (`second_page.html:428-440`) | Same flag |

Consequences:

- A user registered through `index.php` cannot log in on `fisrt_page.html` (its modal checks `localStorage`),
  and the reverse is also true.
- Nothing on the server knows who is using the site, so every protection is cosmetic (`SEC-E03`, `SEC-E15`,
  `SEC-E16`).
- There is **one role only**. No parent, child or administrator distinction exists anywhere.

## 4. Courses, lessons and quizzes (§4.4, §4.5)

### 4.1 The learning content (the most valuable part of the baseline)

| Topic | Lesson page | Items | One item | Quiz |
|---|---|---:|---|---|
| Alphabets | `alphabets_voice.html` | 26 | Letter, word, image, audio (`A`, "Apple", `apple.png`, `apple audio.mp4`) | 10 questions (5 in the hub variant) |
| Numbers | `number_voice.html` | 20 | Number, word, emoji, audio | 10 |
| Animals | `animal_voice.html` | 15 | Name, photo, audio | 10 |
| Birds | `birds_voice.html` | 20 | Name, photo, audio | 10 |
| Fruits | `frutis_voice.html` | 26 | Name, video | 10 |
| Vegetables | `vegitables voice.html` | 20 | Photo that swaps to a video when tapped | 10 |
| Flowers | `flowers_voice.html` | 18 | Name, photo, audio | 10 |
| Colours | `color_voice.html` | 11 | Name, colour image, audio | 10 |
| Body parts | `body_parts_voice.html` | 19 | SVG hotspot on a body diagram with a one-line description | 10 |
| Rhymes | `poem_video2.html` | 9 | Video plus lyrics (Twinkle Twinkle, Baa Baa Black Sheep, Johnny Johnny, Chubby Cheeks, If You're Happy, Humpty Dumpty, Wheels on the Bus, Five Little Monkeys, Jingle Bells) | none |
| Stories | `story.html` | 6 | Video (The Hare and the Tortoise, The Thirsty Crow, Run O Pumpkin, The Two Cats and a Monkey, The Capseller and the Monkeys, The Lion and the Mouse) | none |
| Maths | `maths_lesson_page.html` (orphan) | 4 | Titles only ("Counting 1–10", "Number Recognition", "Simple Addition", "Simple Subtraction"); no content behind them | none |

So the baseline has **9 topics with lessons and a quiz, plus two media collections (rhymes, stories)**, a
natural first set of courses. A lesson today is a whole topic page: a grid of cards, each playing its sound
or video when tapped.

### 4.2 Quizzes: three parallel implementations per subject

| | `<topic>_q.html` (6) | `<topic>_qq.html` (8) | `<topic>_quize.html` (8) + `num_quiz.html` |
|---|---|---|---|
| Reached from | Nowhere (orphans) | The Quizzes hub | The lesson page's "Try Quiz?" button |
| Questions | 3–4 | 10 (alphabet: 5) | 10 |
| Question shape | `{question, options[4], answer}` in the page's script, e.g. `alphabets_quize.html:158` | same | same |
| Pass rule | None, score shown only | more than 4 of 10 correct = **50%** (`animal_qq.html:125`); alphabet 4 of 5 = **80%** (`alphabets_qq.html:89`) | fewer than 4 mistakes = **70%** (`alphabets_quize.html:227`) |
| Lock | None | Quiz locked until the lessons reach 70% (`animal_qq.html:74`) | None |
| Retry | `location.reload()`, unlimited | unlimited | unlimited |
| On pass | Nothing stored | `progress[subject] = {learned:100, quizPassed:true}`, plus `sessionStorage.lastCompleted` for the hub's "Claim reward" | `{learned:100, quizPassed:true, rewardClaimed:true}` |
| Server | Never | Never | Never |

The two live families write to the same `localStorage.progress[subject]` with different pass marks, so
whichever the child played last wins. Answers are visible in every page's source. **No attempt limit exists
anywhere**, so the requirement's three-attempt rule (§11) is new behaviour.

### 4.3 Progress today

- A lesson page records which cards were tapped (`localStorage["<subject>_touched"]`). It sets
  `learned = touched ÷ total × 70`, so the lessons alone **cap a subject at 70%** (`alphabets_voice.html:284-286`).
- Passing either quiz sets `learned = 100` (`animal_qq.html:128`, `alphabets_quize.html:231`). **The baseline
  therefore already keeps a course below 100% until its quiz is passed**, the rule requirement §10 asks for,
  but only in the browser.
- Every card tap also posts to `progres.php` (`alphabets_voice.html:244-258`). No page ever reads that data
  back: `progres_page.html` shows only `localStorage`, and the page that would read the server
  (`progres_page.php.html`) calls a `get_progress.php` that was never uploaded.
- Rhymes and stories are in the progress list (`second_page.html:444`), but nothing ever records them.
- Badges unlock at 100% (`progres_page.html:358`). The hub's "Claim reward" plays a confetti animation.

## 5. Profile (§4.6)

`profil_page.html` redirects to `fisrt_page.html` unless `loggedIn` is set (`profil_page.html:334-338`). It shows:

- a time-of-day greeting;
- a choice of 8 emoji avatars, saved as `localStorage.userAvatar` (`profil_page.html:385-388`);
- a name that is **hard-coded "Clever Cub"** and never filled from the username (`profil_page.html:265`);
- a mood picker that is not saved;
- a badge count and "Smart Level %", computed from `localStorage.progress` (`profil_page.html:356-368`);
- a random "Did you know?" fact.

There is no username creation or change, no parent information and no account settings. Everything in
§12 of the requirement beyond the emoji avatar is new.

## 6. Frontend and backend responsibilities (§4.7)

| Concern | Where it happens today | Should be |
|---|---|---|
| Authentication | Server checks the password (System 1) **or** the browser does (System 2) | Server only |
| Session / "who is this" | Browser `localStorage` | Server session |
| Access control | Browser only (a CSS lock on the card grid) | Server, on every route and API call |
| Lesson content | Hard-coded in each page's HTML | Data (database or content files) served by the backend |
| Quiz questions and answers | Hard-coded in each page's script, answers included | Server-held; the browser gets questions without answers |
| Scoring | Browser | Server |
| Progress | Computed in the browser; stored in `localStorage` and, by the lesson pages, posted to `progres.php` | Calculated by the server from stored records (§10) |
| Feedback | Browser form → `feedback.php` → table `stds2` | Server, with authentication and admin-only reading (§15) |
| Admin | Does not exist | Server-enforced Super Admin area (§19) |

## 7. Data storage and database dependencies (§4.8)

**No schema, migration or SQL dump was uploaded.** What the database must look like is derived from the SQL
in the PHP files. These are the tables the code *assumes*:

| Table | Columns the code uses | Used by | Notes |
|---|---|---|---|
| `stds` (users) | `id`, `username`, `password` (a `password_hash`) | `register.php:12,23` · `login.php:12` | Unique username enforced only in code (`SEC-E13`) |
| `stds2` (feedback) | `name`, `rating`, `message` | `feedback.php:14` | No link to a user, no timestamp |
| `std3` (progress) | `username`, then one column per subject: `alphabets`, `animals`, `birds`, `body`, `colors`, `flowers`, `fruits`, `numbers`, `vegetables` | `progres.php:15,20,25` | Keyed by username text, not by user ID. A new subject means a new column |

Browser storage keys in use: `loggedIn`, `username`, `password` (plain text), `progress`, `userAvatar`
(`localStorage`) and `lastCompleted` (`sessionStorage`).

**Data-model gaps against the requirement (§22):** parents, children, the parent–child link, roles, age or
date of birth, courses, lessons, quizzes, questions, quiz attempts, lesson completion, rewards and badges,
programs (one-year), feedback authorship and categories, consent records and an audit trail. **None of
these exists.** The new schema is designed from the requirement, not extended from these three tables. The
proposal comes before implementation (§22), in the plan.

## 8. Security weaknesses (§4.9)

26 existing security issues are registered in [`02-issue-register.md`](02-issue-register.md) §2: 2 Critical,
5 High, 10 Medium, 8 Low and 1 Info. The root causes are few:

1. **No server-side identity.** There is no session, so the server cannot enforce anything (`SEC-E03`,
   `-E04`, `-E15`, `-E22`).
2. **Trust in the browser.** Access gates, passwords, scores and progress all live in client code or
   `localStorage` (`SEC-E15`, `-E16`, `-E17`).
3. **SQL built from strings** in two of the four endpoints (`SEC-E01`, `-E02`). The other two already use
   prepared statements, which shows the fix was known but not applied consistently.
4. **No configuration layer.** Credentials are pasted into three files, as `root` with no password
   (`SEC-E05`).
5. **No defensive defaults**: headers, validation, rate limits, error handling (`SEC-E06`–`-E12`, `-E20`).

What the baseline does right, and the new version keeps: `password_hash` / `password_verify` and prepared
statements in `login.php` and `register.php`.

## 9. Broken links, missing files, hard-coded paths, obsolete code, technical debt (§4.10)

Every item is registered with its location in [`02-issue-register.md`](02-issue-register.md) §3.

| Kind | Summary | Register |
|---|---|---|
| Dead links | `index.html` (5 links), `progress.html` (8), `learning.html` (7), `body_quiz.html` (1), `get_progress.php` (1) | `FUN-E04`, `FUN-E05` |
| Missing files | The "Capseller and the Monkeys" story video; any body-parts audio; the database schema | `FUN-E30`, `FUN-E06`, §7 |
| Hard-coded paths | `C:\Users\…` in `frutis_voice.html:142` and `maths_lesson_page.html:162-165` | `FUN-E08`, `SEC-E24` |
| Script bugs | Body-parts audio never plays; one rhyme line shows "false"; reward can never be claimed for Alphabets or Numbers | `FUN-E06`, `FUN-E07`, `FUN-E09` |
| Obsolete pages | 11 orphans (25% of the pages) | `FUN-E21` |
| Technical debt | Everything copied into every page; three quiz implementations; two account systems; quirks mode on 29 pages | `FUN-E20`, `FUN-E02`, `FUN-E01`, `FUN-E25` |

**Obsolete, by the requirement's own test (§4: "clearly obsolete"):** the six `<topic>_q.html` prototypes,
`great_job_page.html`, `demo_login.html` and `progres_page.php.html`. Each is unreachable and duplicates a
live page in a less complete form. They are not carried forward as pages; any content they hold that the
live pages lack is. `maths_lesson_page.html` holds only four titles, which become `INF-08`.
`body_part_quize.html` is **not** obsolete: it is the body-parts quiz, orphaned only by a wrong link
(`FUN-E05`).

## 10. Reusable parts (§4.11)

| Asset | Reuse |
|---|---|
| **The learning content**: 9 topics and 175 lesson items, each with its word, image and sound or video; 9 rhymes with lyrics; 5 story videos (§4.1) | Migrated into course, lesson and item data. This is the core of the product |
| **The quiz banks**: 10 questions per topic in the `{question, options, answer}` shape | Migrated into quiz and question data; answers stay on the server |
| **The media**: 317 referenced files, 569 MB | Reused as they are, and optimised where measurement shows a gain (§11) |
| **The course rules already in the code**: lessons worth 70%, a quiz pass to reach 100%, the quiz locked until the lessons are done, a 70% pass mark | Kept, now enforced on the server (`D61`, `D62`, `DD-16`) |
| **The good backend practice**: `password_hash` / `password_verify` and prepared statements (`login.php`, `register.php`) | The same principles, through Spring Security and parameterised queries |
| **Identity**: the name "CleverCubs", `logo.png`, the green primary colour (`#2f6f4e`), the friendly emoji-rich tone and the avatar idea | Kept as the product's identity, refined into a light design system (§24) |
| **The authors' intended data model**: the ER diagram in `CleverCubs.pptx` slide 7. It shows Parent → Child_profile (age, birthdate, avatar) → Progress (topic, status, score, time spent), plus Quiz (difficulty), Achievements, Feedback, Notification and Content_category | It matches the requirement closely, although the code never implemented it. It is an input to the schema proposal |
| **The authors' future scope** (slide 21): more modules (shapes, seasons, transport), a PWA for offline use, a multi-language interface, gamification | A PWA and localisation fit §23 and are noted as recommendations. **Leaderboards conflict with requirement §13** and are not planned |

## 11. Optimisation opportunities (§4.12)

Measured, not assumed (§25). Figures are MiB.

| Where the weight is | Files | MB | Share |
|---|---:|---:|---:|
| Rhyme videos | 9 | 229 | 40% |
| Background loops (autoplay) | 9 | 149 | 26% |
| Story videos | 5 | 123 | 21% |
| Fruit and vegetable clips | 44 | 50 | 9% |
| Audio clips (AAC, 1–10 s) | 115 | 8.3 | 1.4% |
| Images | 153 | 11.5 | 2% |

**Heaviest page loads before any tap** (eager weight): `birds_voice.html` 56.85 MB, `vegitables voice.html`
50.40 MB, `frutis_voice.html` 11.85 MB, `color_voice.html` 9.50 MB. The 10 hub pages each pull the same
7.61 MB `background video.mp4`.

| Opportunity | Expected gain | Basis |
|---|---|---|
| **Drop the autoplaying background videos**, replacing them with a light illustrated background (a static poster at most) | Removes 149 MB of downloads and a constant decode on every hub and lesson page; also fixes the readability problem (`FUN-E18`) | `FUN-E26`, `FUN-E27` |
| **Load media only on demand**: `preload="none"` or `metadata` on players, `loading="lazy"` on images, and a poster frame for each video | First load drops to the page and its visible images | `FUN-E28` |
| **Resize the card images** to at most twice their display size, in WebP | About 5 MB saved, plus the 225 KB logo shown at 80 px on every page | `FUN-E29` |
| **Stream the long videos** (HTTP range requests, which Spring serves for static resources) | Playback starts at once instead of after a full download | the 17-minute `baba blackship.mp4` is 79 MB |
| **Re-encode the rhyme and story videos** at a child-appropriate bitrate | Likely 40–60% smaller. Needs `ffmpeg`, which is not installed, and a visual check. **Deferred until measured**, and never at the cost of quality | FUN-E26 data |
| **One shared stylesheet and one set of script modules**, cached across pages | 150 KB of repeated inline CSS and 138 KB of inline JS become one cached download | `FUN-E20` |
| **Server-side progress read in one request** per dashboard | Replaces a POST on every card tap (`FUN-E22`) | §4.3 |

## 12. Environment on this machine (for the build)

Measured 2026-09-26.

| Tool | State |
|---|---|
| Java | Oracle JDK 26.0.2. `JAVA_HOME` points at a non-existent `jdk-26.0.1`, so every Maven run sets `JAVA_HOME=C:\Program Files\Java\jdk-26.0.2` |
| Maven | 3.9.3 (`C:\Program Files\apache-maven-3.9.3`), and Maven Central is reachable. Spring Boot 4.1 needs Maven 3.6.3+ and runs on Java 17–26 |
| Database | No MySQL, MariaDB or PHP installed |
| Docker | Docker Desktop is installed per user (`%LOCALAPPDATA%\Programs\DockerDesktop`) with a WSL2 `docker-desktop` distribution. The engine is stopped, and Docker Hub is reachable |
| Node | v24.16.0 (for browser tests only, if needed) |
| Media tools | No `ffmpeg` / `ffprobe` |
| Disk | D: 5.1 GB free (99% used); C: 48 GB free |
