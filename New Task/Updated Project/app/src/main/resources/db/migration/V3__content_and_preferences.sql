-- Version 3: two small additions found while building B2-B4 (docs/05-data-model.md section 3).
--
-- course.diagram: the body-parts course teaches with one labelled picture and clickable hotspots, as the
-- baseline page did (body_parts_voice.html). The hotspot geometry is presentation data for one course, so
-- it is kept as JSON on the course rather than as a table of its own.
ALTER TABLE course ADD COLUMN diagram JSON NULL AFTER cover_image;

-- child preferences (requirement section 12, "account preferences"): sound effects and read-aloud, both on
-- by default. Set by the parent; nothing here is personal data.
ALTER TABLE child
    ADD COLUMN sound_effects BOOLEAN NOT NULL DEFAULT TRUE AFTER avatar_code,
    ADD COLUMN read_aloud    BOOLEAN NOT NULL DEFAULT TRUE AFTER sound_effects;

-- The numbers course counts with pictures: "7" shows seven moons, "20" shows twenty sweets (baseline
-- number_voice.html). VARCHAR(16) cannot hold them.
ALTER TABLE lesson_item MODIFY COLUMN emoji VARCHAR(64) NULL;

-- Resume and "recently active" queries read a child's latest views and attempts.
CREATE INDEX ix_item_view_child_time ON lesson_item_view (child_id, first_viewed_at);
CREATE INDEX ix_attempt_child_status ON quiz_attempt (child_id, status);
