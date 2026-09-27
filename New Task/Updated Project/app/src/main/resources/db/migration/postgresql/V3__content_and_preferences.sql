-- PostgreSQL copy of ../mysql/V3__content_and_preferences.sql (D73). The reasons are in that file.
-- PostgreSQL has no AFTER clause: the new columns go at the end, and every query names its columns.

ALTER TABLE course ADD COLUMN diagram JSON NULL;

ALTER TABLE child
    ADD COLUMN sound_effects BOOLEAN NOT NULL DEFAULT TRUE,
    ADD COLUMN read_aloud    BOOLEAN NOT NULL DEFAULT TRUE;

ALTER TABLE lesson_item ALTER COLUMN emoji TYPE VARCHAR(64);

CREATE INDEX ix_item_view_child_time ON lesson_item_view (child_id, first_viewed_at);
CREATE INDEX ix_attempt_child_status ON quiz_attempt (child_id, status);
