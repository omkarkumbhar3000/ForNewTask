-- CleverCubs schema, version 1. The design and the reason for every table: docs/05-data-model.md.
-- Conventions: InnoDB, utf8mb4, BIGINT keys, UTC timestamps (DATETIME(6)), enums as VARCHAR + CHECK.
-- Never edit an applied migration; add a new V<n>__*.sql instead.

-- ---------------------------------------------------------------------------------------------------
-- 3.1 Accounts and people
-- ---------------------------------------------------------------------------------------------------
CREATE TABLE user_account (
    id                   BIGINT       NOT NULL AUTO_INCREMENT PRIMARY KEY,
    email                VARCHAR(254) NOT NULL,
    password_hash        VARCHAR(100) NOT NULL,
    role                 VARCHAR(20)  NOT NULL,
    status               VARCHAR(20)  NOT NULL DEFAULT 'ACTIVE',
    failed_logins        INT          NOT NULL DEFAULT 0,
    locked_until         DATETIME(6)  NULL,
    must_change_password BOOLEAN      NOT NULL DEFAULT FALSE,
    password_changed_at  DATETIME(6)  NOT NULL,
    last_login_at        DATETIME(6)  NULL,
    created_at           DATETIME(6)  NOT NULL,
    updated_at           DATETIME(6)  NOT NULL,
    CONSTRAINT uq_user_account_email UNIQUE (email),
    CONSTRAINT ck_user_account_role CHECK (role IN ('PARENT', 'SUPER_ADMIN')),
    CONSTRAINT ck_user_account_status CHECK (status IN ('ACTIVE', 'LOCKED', 'DISABLED')),
    CONSTRAINT ck_user_account_failed CHECK (failed_logins >= 0)
);

CREATE TABLE parent (
    id         BIGINT       NOT NULL AUTO_INCREMENT PRIMARY KEY,
    account_id BIGINT       NOT NULL,
    full_name  VARCHAR(100) NOT NULL,
    mobile     VARCHAR(20)  NULL,
    city       VARCHAR(80)  NULL,
    created_at DATETIME(6)  NOT NULL,
    updated_at DATETIME(6)  NOT NULL,
    CONSTRAINT uq_parent_account UNIQUE (account_id),
    CONSTRAINT fk_parent_account FOREIGN KEY (account_id) REFERENCES user_account (id) ON DELETE CASCADE
);

CREATE TABLE child (
    id            BIGINT      NOT NULL AUTO_INCREMENT PRIMARY KEY,
    parent_id     BIGINT      NOT NULL,
    first_name    VARCHAR(40) NOT NULL,
    display_name  VARCHAR(40) NOT NULL,
    username      VARCHAR(20) NOT NULL,
    date_of_birth DATE        NOT NULL,
    avatar_code   VARCHAR(30) NOT NULL,
    created_at    DATETIME(6) NOT NULL,
    updated_at    DATETIME(6) NOT NULL,
    CONSTRAINT uq_child_username UNIQUE (username),
    CONSTRAINT fk_child_parent FOREIGN KEY (parent_id) REFERENCES parent (id) ON DELETE CASCADE
);

CREATE TABLE consent_record (
    id               BIGINT      NOT NULL AUTO_INCREMENT PRIMARY KEY,
    parent_id        BIGINT      NOT NULL,
    consent_type     VARCHAR(20) NOT NULL,
    document_version VARCHAR(20) NOT NULL,
    accepted_at      DATETIME(6) NOT NULL,
    CONSTRAINT ck_consent_type CHECK (consent_type IN ('TERMS', 'PRIVACY', 'CHILD_DATA')),
    CONSTRAINT fk_consent_parent FOREIGN KEY (parent_id) REFERENCES parent (id) ON DELETE CASCADE
);

-- ---------------------------------------------------------------------------------------------------
-- 3.2 Content
-- ---------------------------------------------------------------------------------------------------
CREATE TABLE age_group (
    id         BIGINT      NOT NULL AUTO_INCREMENT PRIMARY KEY,
    code       VARCHAR(20) NOT NULL,
    name       VARCHAR(40) NOT NULL,
    min_age    TINYINT     NOT NULL,
    max_age    TINYINT     NOT NULL,
    ui_profile VARCHAR(20) NOT NULL,
    sort_order INT         NOT NULL,
    CONSTRAINT uq_age_group_code UNIQUE (code),
    CONSTRAINT ck_age_group_range CHECK (min_age >= 0 AND min_age <= max_age),
    CONSTRAINT ck_age_group_profile CHECK (ui_profile IN ('TODDLER', 'PRESCHOOL', 'EARLY_PRIMARY'))
);

CREATE TABLE course (
    id          BIGINT       NOT NULL AUTO_INCREMENT PRIMARY KEY,
    slug        VARCHAR(40)  NOT NULL,
    title       VARCHAR(60)  NOT NULL,
    description VARCHAR(500) NOT NULL,
    icon        VARCHAR(16)  NULL,
    cover_image VARCHAR(200) NULL,
    kind        VARCHAR(10)  NOT NULL,
    status      VARCHAR(10)  NOT NULL DEFAULT 'PUBLISHED',
    sort_order  INT          NOT NULL,
    created_at  DATETIME(6)  NOT NULL,
    updated_at  DATETIME(6)  NOT NULL,
    CONSTRAINT uq_course_slug UNIQUE (slug),
    CONSTRAINT ck_course_kind CHECK (kind IN ('TOPIC', 'MEDIA')),
    CONSTRAINT ck_course_status CHECK (status IN ('DRAFT', 'PUBLISHED', 'ARCHIVED'))
);

CREATE TABLE lesson (
    id         BIGINT      NOT NULL AUTO_INCREMENT PRIMARY KEY,
    course_id  BIGINT      NOT NULL,
    title      VARCHAR(80) NOT NULL,
    sort_order INT         NOT NULL,
    status     VARCHAR(10) NOT NULL DEFAULT 'PUBLISHED',
    created_at DATETIME(6) NOT NULL,
    updated_at DATETIME(6) NOT NULL,
    CONSTRAINT uq_lesson_order UNIQUE (course_id, sort_order),
    CONSTRAINT ck_lesson_status CHECK (status IN ('DRAFT', 'PUBLISHED', 'ARCHIVED')),
    CONSTRAINT fk_lesson_course FOREIGN KEY (course_id) REFERENCES course (id) ON DELETE CASCADE
);

CREATE TABLE lesson_item (
    id          BIGINT       NOT NULL AUTO_INCREMENT PRIMARY KEY,
    lesson_id   BIGINT       NOT NULL,
    sort_order  INT          NOT NULL,
    label       VARCHAR(40)  NULL,
    word        VARCHAR(80)  NULL,
    emoji       VARCHAR(16)  NULL,
    description VARCHAR(300) NULL,
    image_path  VARCHAR(200) NULL,
    audio_path  VARCHAR(200) NULL,
    video_path  VARCHAR(200) NULL,
    alt_text    VARCHAR(150) NOT NULL,
    lyrics      TEXT         NULL,
    status      VARCHAR(15)  NOT NULL DEFAULT 'READY',
    CONSTRAINT uq_lesson_item_order UNIQUE (lesson_id, sort_order),
    CONSTRAINT ck_lesson_item_status CHECK (status IN ('READY', 'MEDIA_MISSING')),
    CONSTRAINT fk_lesson_item_lesson FOREIGN KEY (lesson_id) REFERENCES lesson (id) ON DELETE CASCADE
);

CREATE TABLE program (
    id           BIGINT       NOT NULL AUTO_INCREMENT PRIMARY KEY,
    age_group_id BIGINT       NOT NULL,
    year_number  TINYINT      NOT NULL,
    title        VARCHAR(80)  NOT NULL,
    description  VARCHAR(500) NOT NULL,
    status       VARCHAR(10)  NOT NULL DEFAULT 'PUBLISHED',
    created_at   DATETIME(6)  NOT NULL,
    updated_at   DATETIME(6)  NOT NULL,
    CONSTRAINT uq_program_year UNIQUE (age_group_id, year_number),
    CONSTRAINT ck_program_status CHECK (status IN ('DRAFT', 'PUBLISHED', 'ARCHIVED')),
    CONSTRAINT ck_program_year CHECK (year_number >= 1),
    CONSTRAINT fk_program_age_group FOREIGN KEY (age_group_id) REFERENCES age_group (id)
);

CREATE TABLE program_course (
    program_id BIGINT NOT NULL,
    course_id  BIGINT NOT NULL,
    sort_order INT    NOT NULL,
    PRIMARY KEY (program_id, course_id),
    CONSTRAINT fk_program_course_program FOREIGN KEY (program_id) REFERENCES program (id) ON DELETE CASCADE,
    CONSTRAINT fk_program_course_course FOREIGN KEY (course_id) REFERENCES course (id) ON DELETE CASCADE
);

CREATE TABLE ui_message (
    id           BIGINT       NOT NULL AUTO_INCREMENT PRIMARY KEY,
    message_key  VARCHAR(60)  NOT NULL,
    age_group_id BIGINT       NULL,
    text         VARCHAR(300) NOT NULL,
    active       BOOLEAN      NOT NULL DEFAULT TRUE,
    INDEX ix_ui_message_key (message_key),
    CONSTRAINT fk_ui_message_age_group FOREIGN KEY (age_group_id) REFERENCES age_group (id) ON DELETE CASCADE
);

-- ---------------------------------------------------------------------------------------------------
-- 3.3 Learning activity
-- ---------------------------------------------------------------------------------------------------
CREATE TABLE program_enrolment (
    id            BIGINT      NOT NULL AUTO_INCREMENT PRIMARY KEY,
    child_id      BIGINT      NOT NULL,
    program_id    BIGINT      NOT NULL,
    status        VARCHAR(10) NOT NULL DEFAULT 'ACTIVE',
    started_at    DATETIME(6) NOT NULL,
    completed_at  DATETIME(6) NULL,
    next_decision VARCHAR(10) NULL,
    decided_at    DATETIME(6) NULL,
    CONSTRAINT uq_enrolment UNIQUE (child_id, program_id),
    CONSTRAINT ck_enrolment_status CHECK (status IN ('ACTIVE', 'COMPLETED')),
    CONSTRAINT ck_enrolment_decision CHECK (next_decision IS NULL OR next_decision IN ('CONTINUE', 'NOT_NOW')),
    CONSTRAINT fk_enrolment_child FOREIGN KEY (child_id) REFERENCES child (id) ON DELETE CASCADE,
    CONSTRAINT fk_enrolment_program FOREIGN KEY (program_id) REFERENCES program (id)
);

CREATE TABLE lesson_item_view (
    child_id        BIGINT      NOT NULL,
    lesson_item_id  BIGINT      NOT NULL,
    first_viewed_at DATETIME(6) NOT NULL,
    PRIMARY KEY (child_id, lesson_item_id),
    CONSTRAINT fk_item_view_child FOREIGN KEY (child_id) REFERENCES child (id) ON DELETE CASCADE,
    CONSTRAINT fk_item_view_item FOREIGN KEY (lesson_item_id) REFERENCES lesson_item (id) ON DELETE CASCADE
);

CREATE TABLE lesson_completion (
    child_id     BIGINT      NOT NULL,
    lesson_id    BIGINT      NOT NULL,
    completed_at DATETIME(6) NOT NULL,
    PRIMARY KEY (child_id, lesson_id),
    CONSTRAINT fk_completion_child FOREIGN KEY (child_id) REFERENCES child (id) ON DELETE CASCADE,
    CONSTRAINT fk_completion_lesson FOREIGN KEY (lesson_id) REFERENCES lesson (id) ON DELETE CASCADE
);

CREATE TABLE quiz (
    id                BIGINT      NOT NULL AUTO_INCREMENT PRIMARY KEY,
    course_id         BIGINT      NOT NULL,
    title             VARCHAR(80) NOT NULL,
    pass_mark_percent TINYINT     NOT NULL DEFAULT 70,
    required          BOOLEAN     NOT NULL DEFAULT TRUE,
    status            VARCHAR(10) NOT NULL DEFAULT 'PUBLISHED',
    created_at        DATETIME(6) NOT NULL,
    updated_at        DATETIME(6) NOT NULL,
    CONSTRAINT uq_quiz_course UNIQUE (course_id),
    CONSTRAINT ck_quiz_pass_mark CHECK (pass_mark_percent BETWEEN 1 AND 100),
    CONSTRAINT ck_quiz_status CHECK (status IN ('DRAFT', 'PUBLISHED', 'ARCHIVED')),
    CONSTRAINT fk_quiz_course FOREIGN KEY (course_id) REFERENCES course (id) ON DELETE CASCADE
);

CREATE TABLE quiz_question (
    id         BIGINT       NOT NULL AUTO_INCREMENT PRIMARY KEY,
    quiz_id    BIGINT       NOT NULL,
    pool       VARCHAR(10)  NOT NULL DEFAULT 'MAIN',
    sort_order INT          NOT NULL,
    prompt     VARCHAR(200) NOT NULL,
    image_path VARCHAR(200) NULL,
    audio_path VARCHAR(200) NULL,
    CONSTRAINT uq_question_order UNIQUE (quiz_id, pool, sort_order),
    CONSTRAINT ck_question_pool CHECK (pool IN ('MAIN', 'RESERVE')),
    CONSTRAINT fk_question_quiz FOREIGN KEY (quiz_id) REFERENCES quiz (id) ON DELETE CASCADE
);

CREATE TABLE quiz_option (
    id          BIGINT      NOT NULL AUTO_INCREMENT PRIMARY KEY,
    question_id BIGINT      NOT NULL,
    sort_order  INT         NOT NULL,
    label       VARCHAR(80) NOT NULL,
    is_correct  BOOLEAN     NOT NULL,
    CONSTRAINT uq_option_order UNIQUE (question_id, sort_order),
    CONSTRAINT fk_option_question FOREIGN KEY (question_id) REFERENCES quiz_question (id) ON DELETE CASCADE
);

CREATE TABLE quiz_allowance (
    child_id         BIGINT      NOT NULL,
    quiz_id          BIGINT      NOT NULL,
    attempts_allowed TINYINT     NOT NULL DEFAULT 3,
    attempts_used    TINYINT     NOT NULL DEFAULT 0,
    updated_at       DATETIME(6) NOT NULL,
    PRIMARY KEY (child_id, quiz_id),
    CONSTRAINT ck_allowance_used CHECK (attempts_used >= 0 AND attempts_used <= attempts_allowed),
    CONSTRAINT fk_allowance_child FOREIGN KEY (child_id) REFERENCES child (id) ON DELETE CASCADE,
    CONSTRAINT fk_allowance_quiz FOREIGN KEY (quiz_id) REFERENCES quiz (id) ON DELETE CASCADE
);

CREATE TABLE quiz_attempt (
    id             BIGINT      NOT NULL AUTO_INCREMENT PRIMARY KEY,
    child_id       BIGINT      NOT NULL,
    quiz_id        BIGINT      NOT NULL,
    attempt_number TINYINT     NOT NULL,
    status         VARCHAR(12) NOT NULL DEFAULT 'IN_PROGRESS',
    started_at     DATETIME(6) NOT NULL,
    submitted_at   DATETIME(6) NULL,
    correct_count  INT         NOT NULL DEFAULT 0,
    question_count INT         NOT NULL,
    score_percent  TINYINT     NULL,
    passed         BOOLEAN     NULL,
    CONSTRAINT uq_attempt_number UNIQUE (child_id, quiz_id, attempt_number),
    CONSTRAINT ck_attempt_status CHECK (status IN ('IN_PROGRESS', 'SUBMITTED')),
    CONSTRAINT fk_attempt_child FOREIGN KEY (child_id) REFERENCES child (id) ON DELETE CASCADE,
    CONSTRAINT fk_attempt_quiz FOREIGN KEY (quiz_id) REFERENCES quiz (id) ON DELETE CASCADE
);

CREATE TABLE quiz_attempt_answer (
    attempt_id  BIGINT      NOT NULL,
    question_id BIGINT      NOT NULL,
    option_id   BIGINT      NOT NULL,
    is_correct  BOOLEAN     NOT NULL,
    answered_at DATETIME(6) NOT NULL,
    PRIMARY KEY (attempt_id, question_id),
    CONSTRAINT fk_answer_attempt FOREIGN KEY (attempt_id) REFERENCES quiz_attempt (id) ON DELETE CASCADE,
    CONSTRAINT fk_answer_question FOREIGN KEY (question_id) REFERENCES quiz_question (id) ON DELETE CASCADE,
    CONSTRAINT fk_answer_option FOREIGN KEY (option_id) REFERENCES quiz_option (id) ON DELETE CASCADE
);

-- ---------------------------------------------------------------------------------------------------
-- 3.4 Rewards
-- ---------------------------------------------------------------------------------------------------
CREATE TABLE badge (
    id          BIGINT       NOT NULL AUTO_INCREMENT PRIMARY KEY,
    code        VARCHAR(60)  NOT NULL,
    title       VARCHAR(60)  NOT NULL,
    description VARCHAR(200) NOT NULL,
    icon        VARCHAR(16)  NULL,
    criteria    VARCHAR(20)  NOT NULL,
    course_id   BIGINT       NULL,
    program_id  BIGINT       NULL,
    active      BOOLEAN      NOT NULL DEFAULT TRUE,
    CONSTRAINT uq_badge_code UNIQUE (code),
    CONSTRAINT ck_badge_criteria CHECK (criteria IN ('QUIZ_BEST_SCORE', 'COURSE_COMPLETED', 'PROGRAM_COMPLETED')),
    CONSTRAINT fk_badge_course FOREIGN KEY (course_id) REFERENCES course (id) ON DELETE CASCADE,
    CONSTRAINT fk_badge_program FOREIGN KEY (program_id) REFERENCES program (id) ON DELETE CASCADE
);

CREATE TABLE child_badge (
    child_id          BIGINT      NOT NULL,
    badge_id          BIGINT      NOT NULL,
    awarded_at        DATETIME(6) NOT NULL,
    source_attempt_id BIGINT      NULL,
    PRIMARY KEY (child_id, badge_id),
    CONSTRAINT fk_child_badge_child FOREIGN KEY (child_id) REFERENCES child (id) ON DELETE CASCADE,
    CONSTRAINT fk_child_badge_badge FOREIGN KEY (badge_id) REFERENCES badge (id) ON DELETE CASCADE,
    CONSTRAINT fk_child_badge_attempt FOREIGN KEY (source_attempt_id) REFERENCES quiz_attempt (id) ON DELETE SET NULL
);

CREATE TABLE certificate (
    id                BIGINT      NOT NULL AUTO_INCREMENT PRIMARY KEY,
    child_id          BIGINT      NOT NULL,
    program_id        BIGINT      NOT NULL,
    issued_at         DATETIME(6) NOT NULL,
    verification_code CHAR(16)    NOT NULL,
    CONSTRAINT uq_certificate_code UNIQUE (verification_code),
    CONSTRAINT uq_certificate_child_program UNIQUE (child_id, program_id),
    CONSTRAINT fk_certificate_child FOREIGN KEY (child_id) REFERENCES child (id) ON DELETE CASCADE,
    CONSTRAINT fk_certificate_program FOREIGN KEY (program_id) REFERENCES program (id)
);

-- ---------------------------------------------------------------------------------------------------
-- 3.5 Parent interaction
-- ---------------------------------------------------------------------------------------------------
CREATE TABLE parent_request (
    id              BIGINT      NOT NULL AUTO_INCREMENT PRIMARY KEY,
    child_id        BIGINT      NOT NULL,
    parent_id       BIGINT      NOT NULL,
    type            VARCHAR(20) NOT NULL,
    quiz_id         BIGINT      NULL,
    requested_value VARCHAR(40) NULL,
    status          VARCHAR(10) NOT NULL DEFAULT 'PENDING',
    created_at      DATETIME(6) NOT NULL,
    resolved_at     DATETIME(6) NULL,
    INDEX ix_parent_request_parent_status (parent_id, status),
    CONSTRAINT ck_request_type CHECK (type IN ('QUIZ_ATTEMPTS', 'USERNAME_CHANGE', 'HELP')),
    CONSTRAINT ck_request_status CHECK (status IN ('PENDING', 'APPROVED', 'DECLINED')),
    CONSTRAINT fk_request_child FOREIGN KEY (child_id) REFERENCES child (id) ON DELETE CASCADE,
    CONSTRAINT fk_request_parent FOREIGN KEY (parent_id) REFERENCES parent (id) ON DELETE CASCADE,
    CONSTRAINT fk_request_quiz FOREIGN KEY (quiz_id) REFERENCES quiz (id) ON DELETE CASCADE
);

CREATE TABLE feedback (
    id         BIGINT        NOT NULL AUTO_INCREMENT PRIMARY KEY,
    parent_id  BIGINT        NOT NULL,
    category   VARCHAR(20)   NOT NULL,
    course_id  BIGINT        NULL,
    rating     TINYINT       NULL,
    message    VARCHAR(2000) NOT NULL,
    status     VARCHAR(10)   NOT NULL DEFAULT 'NEW',
    created_at DATETIME(6)   NOT NULL,
    updated_at DATETIME(6)   NOT NULL,
    INDEX ix_feedback_status (status, created_at),
    CONSTRAINT ck_feedback_category CHECK (category IN ('GENERAL', 'COURSE', 'USABILITY', 'SUGGESTION', 'PROBLEM')),
    CONSTRAINT ck_feedback_rating CHECK (rating IS NULL OR rating BETWEEN 1 AND 5),
    CONSTRAINT ck_feedback_status CHECK (status IN ('NEW', 'READ', 'RESOLVED')),
    CONSTRAINT fk_feedback_parent FOREIGN KEY (parent_id) REFERENCES parent (id) ON DELETE CASCADE,
    CONSTRAINT fk_feedback_course FOREIGN KEY (course_id) REFERENCES course (id) ON DELETE SET NULL
);

-- ---------------------------------------------------------------------------------------------------
-- 3.6 Operations
-- ---------------------------------------------------------------------------------------------------
-- Append-only: the application user gets INSERT and SELECT only (afterMigrate.sql). No foreign key to
-- user_account, so that deleting an account keeps its audit trail (the trail holds IDs, never names).
CREATE TABLE audit_event (
    id               BIGINT      NOT NULL AUTO_INCREMENT PRIMARY KEY,
    occurred_at      DATETIME(6) NOT NULL,
    actor_account_id BIGINT      NULL,
    actor_role       VARCHAR(20) NOT NULL,
    action           VARCHAR(60) NOT NULL,
    target_type      VARCHAR(40) NULL,
    target_id        BIGINT      NULL,
    details          JSON        NULL,
    INDEX ix_audit_occurred (occurred_at),
    INDEX ix_audit_actor (actor_account_id, occurred_at),
    INDEX ix_audit_action (action, occurred_at)
);

CREATE TABLE system_setting (
    setting_key   VARCHAR(60)  NOT NULL PRIMARY KEY,
    setting_value VARCHAR(200) NOT NULL,
    updated_at    DATETIME(6)  NOT NULL,
    updated_by    BIGINT       NULL
);
