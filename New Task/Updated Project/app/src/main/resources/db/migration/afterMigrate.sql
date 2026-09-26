-- Flyway callback: runs after every migrate, as cc_migrator. Grants the application user exactly the
-- table rights it needs (least privilege, docs/05-data-model.md section 7). Idempotent.
-- A test (DatabaseSetupTests) proves that cc_app can write the application tables and CANNOT update
-- or delete audit_event. When a migration adds a table, add its grant here.

GRANT SELECT, INSERT, UPDATE, DELETE ON user_account        TO 'cc_app'@'%';
GRANT SELECT, INSERT, UPDATE, DELETE ON parent              TO 'cc_app'@'%';
GRANT SELECT, INSERT, UPDATE, DELETE ON child               TO 'cc_app'@'%';
GRANT SELECT, INSERT, UPDATE, DELETE ON consent_record      TO 'cc_app'@'%';
GRANT SELECT, INSERT, UPDATE, DELETE ON age_group           TO 'cc_app'@'%';
GRANT SELECT, INSERT, UPDATE, DELETE ON course              TO 'cc_app'@'%';
GRANT SELECT, INSERT, UPDATE, DELETE ON lesson              TO 'cc_app'@'%';
GRANT SELECT, INSERT, UPDATE, DELETE ON lesson_item         TO 'cc_app'@'%';
GRANT SELECT, INSERT, UPDATE, DELETE ON program             TO 'cc_app'@'%';
GRANT SELECT, INSERT, UPDATE, DELETE ON program_course      TO 'cc_app'@'%';
GRANT SELECT, INSERT, UPDATE, DELETE ON ui_message          TO 'cc_app'@'%';
GRANT SELECT, INSERT, UPDATE, DELETE ON program_enrolment   TO 'cc_app'@'%';
GRANT SELECT, INSERT, UPDATE, DELETE ON lesson_item_view    TO 'cc_app'@'%';
GRANT SELECT, INSERT, UPDATE, DELETE ON lesson_completion   TO 'cc_app'@'%';
GRANT SELECT, INSERT, UPDATE, DELETE ON quiz                TO 'cc_app'@'%';
GRANT SELECT, INSERT, UPDATE, DELETE ON quiz_question       TO 'cc_app'@'%';
GRANT SELECT, INSERT, UPDATE, DELETE ON quiz_option         TO 'cc_app'@'%';
GRANT SELECT, INSERT, UPDATE, DELETE ON quiz_allowance      TO 'cc_app'@'%';
GRANT SELECT, INSERT, UPDATE, DELETE ON quiz_attempt        TO 'cc_app'@'%';
GRANT SELECT, INSERT, UPDATE, DELETE ON quiz_attempt_answer TO 'cc_app'@'%';
GRANT SELECT, INSERT, UPDATE, DELETE ON badge               TO 'cc_app'@'%';
GRANT SELECT, INSERT, UPDATE, DELETE ON child_badge         TO 'cc_app'@'%';
GRANT SELECT, INSERT, UPDATE, DELETE ON certificate         TO 'cc_app'@'%';
GRANT SELECT, INSERT, UPDATE, DELETE ON parent_request      TO 'cc_app'@'%';
GRANT SELECT, INSERT, UPDATE, DELETE ON feedback            TO 'cc_app'@'%';
GRANT SELECT, UPDATE                 ON system_setting      TO 'cc_app'@'%';
-- Append-only audit trail: no UPDATE, no DELETE.
GRANT SELECT, INSERT                 ON audit_event         TO 'cc_app'@'%';
