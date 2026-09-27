-- Flyway callback for PostgreSQL (D73): runs after every migrate, as the schema owner. The same least
-- privilege as ../mysql/afterMigrate.sql (docs/05-data-model.md section 7). Idempotent.
--
-- A hosted PostgreSQL has no init script to create the application user (MySQL's is db/init/01-users.sh),
-- so this callback creates the cc_app login role itself, and resets its password on every start so that
-- the role always matches the configured secret. The password is a Flyway placeholder filled from the
-- environment (CC_DB_APP_PASSWORD); it is never written in this file. When a migration adds a table,
-- add its grant here and in the MySQL callback.

DO $$
BEGIN
    IF length('${appPassword}') < 16 THEN
        RAISE EXCEPTION 'CC_DB_APP_PASSWORD must be set, at least 16 characters';
    END IF;
    IF NOT EXISTS (SELECT 1 FROM pg_roles WHERE rolname = 'cc_app') THEN
        CREATE ROLE cc_app LOGIN PASSWORD '${appPassword}';
    ELSE
        ALTER ROLE cc_app WITH LOGIN PASSWORD '${appPassword}';
    END IF;
END
$$;

GRANT USAGE ON SCHEMA public TO cc_app;

GRANT SELECT, INSERT, UPDATE, DELETE ON
    user_account, parent, child, consent_record, age_group, course, lesson, lesson_item, program,
    program_course, ui_message, program_enrolment, lesson_item_view, lesson_completion, quiz, quiz_question,
    quiz_option, quiz_allowance, quiz_attempt, quiz_attempt_answer, badge, child_badge, certificate,
    parent_request, feedback
    TO cc_app;
GRANT SELECT, UPDATE ON system_setting TO cc_app;
-- Append-only audit trail: no UPDATE, no DELETE.
GRANT SELECT, INSERT ON audit_event TO cc_app;
-- Server sessions (V4).
GRANT SELECT, INSERT, UPDATE, DELETE ON spring_session, spring_session_attributes TO cc_app;
-- New rows take their ids from the identity sequences.
GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA public TO cc_app;
