# Data Model — Proposed schema for the enhanced CleverCubs

**Objective:** `OBJ-034` · **Requirement:** [`00-source-requirement.md`](00-source-requirement.md) §7, §10, §11,
§13, §16, §19, §22 · **Decisions:** [`03-decisions.md`](03-decisions.md) · **Status:** ✅ approved with the
Blueprint (`D68`); migrations follow this document

---

## 1. Basis

- **Why this is a new design:** the baseline has three tables (`stds`, `stds2`, `std3`) and no schema file
  ([`01-baseline-analysis.md`](01-baseline-analysis.md) §7). It supports none of the relationships that
  requirement §22 lists, so the schema is designed from the requirement. It is not extended from those
  tables.
- **What it draws on:**
  - the owner's decisions `D56`–`D67`;
  - the documented defaults `DD-01`–`DD-16`;
  - the authors' own ER diagram (`CleverCubs.pptx` slide 7). The diagram already sketches Parent →
    Child_profile → Progress, and Quiz, Achievements, Feedback, Notification and Content_category.
- **Where uncertain facts go:** nothing here invents a business rule. Where a value is a setting rather
  than a fact, it lives in `system_setting` so the Super Admin can change it.

**Conventions:**

- MySQL 8, InnoDB, `utf8mb4`.
- `BIGINT` surrogate keys, with `created_at` and `updated_at` in UTC.
- Enumerations are `VARCHAR` plus a `CHECK` constraint, so adding a value is a migration.
- Every foreign key is indexed.
- The schema is created and changed only by versioned Flyway migrations.

## 2. Entity overview

```text
 user_account ─1:1─ parent ─1:n─ child ─n:1─ (age group derived from date_of_birth)
      │               │           │
      │               │           ├─1:n─ program_enrolment ─n:1─ program ─n:1─ age_group
      │               │           │                                 └─n:m─ course (program_course)
      │               │           ├─1:n─ lesson_item_view ─n:1─ lesson_item ─n:1─ lesson ─n:1─ course
      │               │           ├─1:n─ lesson_completion ─n:1─ lesson
      │               │           ├─1:n─ quiz_allowance ─n:1─ quiz ─1:1─ course
      │               │           ├─1:n─ quiz_attempt ─1:n─ quiz_attempt_answer ─n:1─ quiz_option
      │               │           ├─1:n─ child_badge ─n:1─ badge
      │               │           └─1:n─ certificate ─n:1─ program
      │               ├─1:n─ parent_request (escalation inbox, per child)
      │               ├─1:n─ feedback
      │               └─1:n─ consent_record
      └─1:n─ audit_event (actor)
 system_setting · ui_message (age-group-specific wording)
```

**Roles (`DD-04`, `D58`):**

- `user_account.role` is `PARENT` or `SUPER_ADMIN`.
- **A child has no login.** `CHILD` is a session mode that a signed-in parent enters for one of their own
  children. The session then carries only the `CHILD` authority, so parent and admin endpoints are closed
  to it.

## 3. Tables

### 3.1 Accounts and people

| Table | Columns (type, constraint) | Notes |
|---|---|---|
| `user_account` | `id` PK · `email` VARCHAR(254) **UNIQUE**, lower-cased · `password_hash` VARCHAR(100) · `role` (`PARENT`, `SUPER_ADMIN`) · `status` (`ACTIVE`, `LOCKED`, `DISABLED`) · `failed_logins` INT · `locked_until` DATETIME NULL · `must_change_password` BOOL · `password_changed_at` · `last_login_at` NULL · `created_at` · `updated_at` | The only login table. The hash is bcrypt through `DelegatingPasswordEncoder` (`{bcrypt}$2a$12$…`, `DD-01`). The unique email fixes `SEC-E13` |
| `parent` | `id` PK · `account_id` FK **UNIQUE** → `user_account` · `full_name` VARCHAR(100) · `mobile` VARCHAR(20) NULL · `city` VARCHAR(80) NULL · `created_at` · `updated_at` | The fields in `DD-09`. No address, school, gender or photo |
| `child` | `id` PK · `parent_id` FK → `parent` ON DELETE CASCADE · `first_name` VARCHAR(40) · `display_name` VARCHAR(40) · `username` VARCHAR(20) **UNIQUE** · `date_of_birth` DATE · `avatar_code` VARCHAR(30), from a fixed set (`DD-06`) · `created_at` · `updated_at` | The age group is **derived** from `date_of_birth`, never stored, so it moves with birthdays (§5). Username rules are in `DD-08` |
| `consent_record` | `id` PK · `parent_id` FK · `consent_type` (`TERMS`, `PRIVACY`, `CHILD_DATA`) · `document_version` VARCHAR(20) · `accepted_at` | Records parental consent at registration (`D67`). A new document version requires new consent |

### 3.2 Content

| Table | Columns | Notes |
|---|---|---|
| `age_group` | `id` PK · `code` **UNIQUE** (`TINY`, `LITTLE`, `BIG`) · `name` ("Tiny Cubs") · `min_age` TINYINT · `max_age` TINYINT · `ui_profile` (`TODDLER`, `PRESCHOOL`, `EARLY_PRIMARY`) · `sort_order` | Seeded as 2–3, 4–5 and 6–8 (`D66`). A `CHECK` that `min_age ≤ max_age`, and a service check that bands do not overlap |
| `course` | `id` PK · `slug` **UNIQUE** · `title` · `description` VARCHAR(500) · `icon` VARCHAR(16) · `cover_image` NULL · `kind` (`TOPIC`, `MEDIA`) · `status` (`DRAFT`, `PUBLISHED`, `ARCHIVED`) · `sort_order` · timestamps | `TOPIC` = lessons and a quiz (Alphabets…); `MEDIA` = rhymes and stories, with no quiz |
| `lesson` | `id` PK · `course_id` FK · `title` · `sort_order` · `status` · timestamps · **UNIQUE** (`course_id`, `sort_order`) | About five items each (`D60`); one video for a rhyme or story |
| `lesson_item` | `id` PK · `lesson_id` FK · `sort_order` · `label` VARCHAR(40) ("A") · `word` VARCHAR(60) ("Apple") · `description` VARCHAR(300) NULL (body parts) · `image_path` NULL · `audio_path` NULL · `video_path` NULL · `alt_text` VARCHAR(150) · `lyrics` TEXT NULL · `status` (`READY`, `MEDIA_MISSING`) | Media paths are relative to the configured media root; a validator rejects `..` and absolute paths. `MEDIA_MISSING` covers `INF-09` and `INF-10` and is excluded from progress |
| `program` | `id` PK · `age_group_id` FK · `year_number` TINYINT · `title` · `description` · `status` · **UNIQUE** (`age_group_id`, `year_number`) | `D65` |
| `program_course` | `program_id` FK · `course_id` FK · `sort_order` · PK (`program_id`, `course_id`) | A course may belong to several programs |
| `ui_message` | `id` PK · `message_key` ("quiz.passed", "lesson.start", "encourage.retry") · `age_group_id` FK NULL (NULL = every group) · `text` VARCHAR(300) · `active` BOOL | Age-appropriate wording and encouraging messages (§5, §14). Several rows under one key form a rotating set |

### 3.3 Learning activity

| Table | Columns | Notes |
|---|---|---|
| `program_enrolment` | `id` PK · `child_id` FK · `program_id` FK · `status` (`ACTIVE`, `COMPLETED`) · `started_at` · `completed_at` NULL · `next_decision` (`CONTINUE`, `NOT_NOW`) NULL · `decided_at` NULL · **UNIQUE** (`child_id`, `program_id`) | Created at registration for the program of the child's age group. The decision belongs to the parent (§16) |
| `lesson_item_view` | `child_id` FK · `lesson_item_id` FK · `first_viewed_at` · PK (`child_id`, `lesson_item_id`) | Idempotent: viewing twice changes nothing. A video counts once it has played to the end or 90% of the way (`DD-17`) |
| `lesson_completion` | `child_id` FK · `lesson_id` FK · `completed_at` · PK (`child_id`, `lesson_id`) | Written by the server when every `READY` item of the lesson has been viewed |
| `quiz` | `id` PK · `course_id` FK **UNIQUE** · `title` · `pass_mark_percent` TINYINT default **70** (`D62`) · `required` BOOL default TRUE · `status` · timestamps | One quiz per `TOPIC` course. `CHECK pass_mark_percent BETWEEN 1 AND 100` |
| `quiz_question` | `id` PK · `quiz_id` FK · `sort_order` · `prompt` VARCHAR(200) · `image_path` NULL · `audio_path` NULL | Migrated from the baseline banks (`DD-18`) |
| `quiz_option` | `id` PK · `question_id` FK · `sort_order` · `label` VARCHAR(60) · `is_correct` BOOL | Exactly one correct option per question, enforced by the service on save. **`is_correct` is never sent to the browser before an answer** (fixes `SEC-E17`) |
| `quiz_allowance` | `child_id` FK · `quiz_id` FK · `attempts_allowed` TINYINT default 3 · `attempts_used` TINYINT default 0 · `updated_at` · PK (`child_id`, `quiz_id`) · `CHECK attempts_used ≤ attempts_allowed` | **The backend's attempt limit (§11).** Starting an attempt runs `UPDATE … SET attempts_used = attempts_used + 1 WHERE … AND attempts_used < attempts_allowed`; one row changed means allowed. This is atomic, so two simultaneous starts cannot exceed the limit. A parent grant adds 3 to `attempts_allowed` (`D63`) |
| `quiz_attempt` | `id` PK · `child_id` FK · `quiz_id` FK · `attempt_number` TINYINT · `status` (`IN_PROGRESS`, `SUBMITTED`) · `started_at` · `submitted_at` NULL · `correct_count` · `question_count` · `score_percent` TINYINT NULL · `passed` BOOL NULL · **UNIQUE** (`child_id`, `quiz_id`, `attempt_number`) | Leaving mid-quiz does not lose the attempt: reopening resumes the same `IN_PROGRESS` attempt (`DD-19`) |
| `quiz_attempt_answer` | `attempt_id` FK · `question_id` FK · `option_id` FK · `is_correct` BOOL · `answered_at` · PK (`attempt_id`, `question_id`) | One answer per question, never changed afterwards. The server scores it and returns the feedback |

### 3.4 Rewards

| Table | Columns | Notes |
|---|---|---|
| `badge` | `id` PK · `code` **UNIQUE** · `title` · `description` · `icon` · `criteria` (`QUIZ_BEST_SCORE`, `COURSE_COMPLETED`, `PROGRAM_COMPLETED`) · `course_id` FK NULL · `program_id` FK NULL · `active` | One `QUIZ_BEST_SCORE` badge per topic course. Its threshold is the single `reward.threshold_percent` setting, **80, compared with ≥** (`D64`) |
| `child_badge` | `child_id` FK · `badge_id` FK · `awarded_at` · `source_attempt_id` FK NULL · PK (`child_id`, `badge_id`) | Awarded once, by the server, when the rule is met; never requested by the browser |
| `certificate` | `id` PK · `child_id` FK · `program_id` FK · `issued_at` · `verification_code` CHAR(16) **UNIQUE**, random · **UNIQUE** (`child_id`, `program_id`) | Issued at program completion. Wording is `INF-07` |

### 3.5 Parent interaction

| Table | Columns | Notes |
|---|---|---|
| `parent_request` | `id` PK · `child_id` FK · `parent_id` FK · `type` (`QUIZ_ATTEMPTS`, `USERNAME_CHANGE`, `HELP`) · `quiz_id` FK NULL · `requested_value` VARCHAR(40) NULL · `status` (`PENDING`, `APPROVED`, `DECLINED`) · `created_at` · `resolved_at` NULL | The escalation inbox (`D59`). At most one `PENDING` request per child, type and quiz, enforced by the service. The child never sees parent data |
| `feedback` | `id` PK · `parent_id` FK ON DELETE SET NULL · `category` (`GENERAL`, `COURSE`, `USABILITY`, `SUGGESTION`, `PROBLEM`) · `course_id` FK NULL · `rating` TINYINT NULL `CHECK 1–5` · `message` VARCHAR(2000) · `status` (`NEW`, `READ`, `RESOLVED`) · `created_at` · `updated_at` | §15. Readable only by `SUPER_ADMIN` and its author. Stored as text and always output-encoded (fixes `SEC-E01`, `SEC-E18`) |

### 3.6 Operations

| Table | Columns | Notes |
|---|---|---|
| `audit_event` | `id` PK · `occurred_at` · `actor_account_id` NULL · `actor_role` · `action` VARCHAR(60) · `target_type` VARCHAR(40) NULL · `target_id` BIGINT NULL · `details` JSON NULL | **Append-only:** the application's database user has `INSERT` and `SELECT` only on this table (§7). No passwords, names or free text in `details` (`DD-14`) |
| `system_setting` | `setting_key` PK · `setting_value` VARCHAR(200) · `updated_at` · `updated_by` NULL | Seeded: `reward.threshold_percent=80`, `quiz.max_attempts=3`, `quiz.grant_attempts=3`, `progress.lesson_weight_percent=70`, `session.child_idle_minutes=30`, `parent.reauth_minutes=15` |

## 4. The rules the schema serves

These rules are implemented as plain Java domain classes and unit-tested without a database (`DD-15`).

| Rule | Formula or behaviour | Source |
|---|---|---|
| Age group | Whole years from `date_of_birth` to today, matched to `min_age ≤ age ≤ max_age`. Registration accepts ages 2–8 only (the configured bands) | `D66` |
| Course progress, topic course | `lesson_weight × completed ÷ total` + (`quiz passed` ? `100 − lesson_weight` : 0), with lessons counting only their `READY` items. With the defaults: 5 lessons done and the quiz not passed = **70%**; the quiz passed = **100%** | `D61`, §10 |
| Course progress, media course | `100 × completed ÷ total` | `D61` |
| Quiz start | Allowed if the lessons are complete (`DD-16`) and one allowance is free (atomic update). If an attempt is `IN_PROGRESS`, it is resumed and no allowance is used | §11, `D63` |
| Quiz result | `score_percent = round(100 × correct ÷ questions)`. `passed = score_percent ≥ pass_mark_percent` | `D62` |
| Quiz locked | `attempts_used = attempts_allowed` and no pass. The child is offered "Ask a grown-up", which creates a `parent_request` of type `QUIZ_ATTEMPTS` | `D63`, `D59` |
| Reward | After each submitted attempt, if `best score_percent ≥ reward.threshold_percent`, award the course's badge once | `D64` |
| Program complete | Every course in the enrolled program is at 100%. The enrolment becomes `COMPLETED`, the certificate is issued, and the parent sees the year summary | `D65` |

## 5. What the browser can and cannot send

| The browser sends | The server decides |
|---|---|
| "I viewed item 42" | Whether it belongs to this child's program, the lesson's completion, progress |
| "Start quiz 7" | Whether the lessons are done, whether an attempt is free, which attempt number |
| "Answer question 3 with option 12" | Whether it is correct, the score, pass or fail, badges, the lock |
| Nothing about progress, scores, badges or the child's identity | All of it, from the session's active child |

## 6. Mapping the baseline content

| Baseline | Becomes |
|---|---|
| 9 topic pages (175 items) | 9 `TOPIC` courses. Items are grouped into lessons of about five, in the baseline order (`D60`) |
| The lesson-linked quiz banks (`<topic>_quize.html`, `num_quiz.html`, 10 questions each) | One quiz per topic course (`DD-18`) |
| `poem_video2.html` (9 rhymes and lyrics), `story.html` (6 stories) | Two `MEDIA` courses; one lesson per video; the missing story is `MEDIA_MISSING` (`INF-09`) |
| `std3` subject columns | Nothing: replaced by the derived progress rules |
| `stds` users | Nothing is migrated. No real user data was uploaded, and the deck shows the old table held test and plain-text data (`SEC-E25`) |
| `stds2` feedback | Nothing is migrated |

## 7. Access by database user (least privilege, `DD-13`)

| User | Rights | Used by |
|---|---|---|
| `cc_migrator` | DDL on the `clevercubs` schema | Flyway, at startup or from the command line |
| `cc_app` | `SELECT`, `INSERT`, `UPDATE`, `DELETE` on the application tables; `SELECT`, `INSERT` only on `audit_event` | The running application |

Neither is `root`, and both passwords come from the environment (`.env`, never committed). This fixes
`SEC-E05`.

## 8. Changes made during the build (migration `V3__content_and_preferences.sql`)

| Change | Why |
|---|---|
| `course.diagram` JSON NULL | The body-parts course teaches with one picture and clickable areas, as the baseline page did. The geometry is presentation data for one course |
| `child.sound_effects`, `child.read_aloud` BOOLEAN, default TRUE | "Account preferences" (§12), set by the parent |
| `lesson_item.emoji` widened from VARCHAR(16) to VARCHAR(64) | The numbers course counts with pictures: "20" shows twenty sweets |
| Indexes on `lesson_item_view (child_id, first_viewed_at)` and `quiz_attempt (child_id, status)` | "Continue learning" and the open-try lookup |

No table was added, so the grants in `afterMigrate.sql` and the table list in `DatabaseSetupTests` are
unchanged.

## 9. Sessions in the database and a PostgreSQL copy (`V4__http_sessions.sql`, `D73`)

| Change | Why |
|---|---|
| `SPRING_SESSION`, `SPRING_SESSION_ATTRIBUTES` (Spring Session's own schema) | Server sessions survive a restart and work across several instances; the cloud host stops idle instances ([`07-deployment.md`](07-deployment.md)). `PRINCIPAL_NAME` holds the account id, never the email address |
| Grants for the two tables in both `afterMigrate.sql` callbacks | `cc_app` creates, refreshes and expires its own sessions |
| The migrations now live in `db/migration/mysql/` and `db/migration/postgresql/` | The hosted deployment runs on PostgreSQL. The MySQL files only moved folder (their checksums are unchanged), so existing databases validate |

**The PostgreSQL copy keeps every table, key, check and rule.** Its differences are mechanical:
identity keys for `AUTO_INCREMENT`, `TIMESTAMP(6)` for `DATETIME(6)`, `SMALLINT` for `TINYINT`, separate
`CREATE INDEX` statements, and an index on every foreign key (InnoDB creates those by itself).
`user_account.email` and `child.username` are `CITEXT`, because the application relies on MySQL's
case-insensitive comparison; the length limits the `VARCHAR`s gave are kept as checks. On PostgreSQL the
callback also creates the `cc_app` role, since a hosted database has no init script. A change to one copy
needs the same change to the other, and both test runs (`mvnw test`, `mvnw test -Dclevercubs.test.db=postgresql`)
must pass.

