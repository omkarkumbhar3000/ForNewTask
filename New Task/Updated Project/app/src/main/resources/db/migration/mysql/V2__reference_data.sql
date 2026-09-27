-- Reference data that the owner decided (docs/03-decisions.md) or that the Super Admin may later edit.
-- Courses, lessons, quizzes and badges are NOT seeded here: they come from the content JSON files
-- (src/main/resources/content/), loaded by ContentSeeder on first start.

-- Age groups: D66 (2-3, 4-5, 6-8). Editable data, never hard-coded in the application.
INSERT INTO age_group (code, name, min_age, max_age, ui_profile, sort_order) VALUES
    ('TINY',   'Tiny Cubs',   2, 3, 'TODDLER',       1),
    ('LITTLE', 'Little Cubs', 4, 5, 'PRESCHOOL',     2),
    ('BIG',    'Big Cubs',    6, 8, 'EARLY_PRIMARY', 3);

-- Year-1 programs, one per age group (D65). Their course lists are filled by ContentSeeder (DD-20).
INSERT INTO program (age_group_id, year_number, title, description, status, created_at, updated_at)
SELECT id, 1, CONCAT(name, ' - Year 1'),
       'The first year of CleverCubs: letters, numbers, colours, the natural world, rhymes and stories.',
       'PUBLISHED', UTC_TIMESTAMP(6), UTC_TIMESTAMP(6)
FROM age_group;

-- Settings the Super Admin can change (D61-D64, DD-02). One place, so every rule reads the same value.
INSERT INTO system_setting (setting_key, setting_value, updated_at) VALUES
    ('progress.lesson_weight_percent', '70', UTC_TIMESTAMP(6)),
    ('quiz.max_attempts',              '3',  UTC_TIMESTAMP(6)),
    ('quiz.grant_attempts',            '3',  UTC_TIMESTAMP(6)),
    ('quiz.default_pass_mark_percent', '70', UTC_TIMESTAMP(6)),
    ('reward.threshold_percent',       '80', UTC_TIMESTAMP(6)),
    ('session.child_idle_minutes',     '30', UTC_TIMESTAMP(6)),
    ('parent.reauth_minutes',          '15', UTC_TIMESTAMP(6)),
    ('consent.document_version',       '2026-09-draft', UTC_TIMESTAMP(6));

-- Age-appropriate wording (requirement 5 and 14): encouraging, never shaming, never comparing children.
-- A NULL age group means "any group"; a group-specific row wins over it. Several rows under one key form
-- a rotating set. {name} is replaced with the child's display name, escaped as text.
INSERT INTO ui_message (message_key, age_group_id, text) VALUES
    ('home.greeting', NULL, 'Hello, {name}! What shall we learn today?'),
    ('home.greeting', (SELECT id FROM age_group WHERE code = 'TINY'), 'Hi {name}! Let''s play and learn!'),
    ('home.greeting', (SELECT id FROM age_group WHERE code = 'BIG'), 'Welcome back, {name}. Pick up where you left off, or try something new.'),

    ('lesson.start', NULL, 'Tap each card to see and hear it.'),
    ('lesson.start', (SELECT id FROM age_group WHERE code = 'TINY'), 'Tap a picture!'),
    ('lesson.start', (SELECT id FROM age_group WHERE code = 'BIG'), 'Open every card in this lesson to complete it.'),

    ('lesson.done', NULL, 'You finished this lesson. Well done!'),
    ('lesson.done', (SELECT id FROM age_group WHERE code = 'TINY'), 'Yay! All done!'),

    ('quiz.intro', NULL, 'Ready for a little quiz? Take your time.'),
    ('quiz.intro', (SELECT id FROM age_group WHERE code = 'TINY'), 'Let''s play a guessing game!'),
    ('quiz.intro', (SELECT id FROM age_group WHERE code = 'BIG'), 'Answer each question. You can take your time - there is no clock.'),

    ('quiz.correct', NULL, 'That''s right!'),
    ('quiz.correct', NULL, 'Great thinking!'),
    ('quiz.correct', NULL, 'Yes, well done!'),

    ('quiz.incorrect', NULL, 'Nice try! This one is {answer}.'),
    ('quiz.incorrect', (SELECT id FROM age_group WHERE code = 'TINY'), 'Oops! It''s {answer}.'),

    ('quiz.passed', NULL, 'You did it! You finished the quiz.'),
    ('quiz.not_passed', NULL, 'Good effort! Let''s look at the lessons again and try once more.'),
    ('quiz.not_passed', (SELECT id FROM age_group WHERE code = 'TINY'), 'Good try! Let''s play the lessons again.'),
    ('quiz.locked', NULL, 'You''ve used all your tries for now. Let''s practise the lessons, and ask a grown-up when you''re ready to try again.'),
    ('quiz.locked', (SELECT id FROM age_group WHERE code = 'TINY'), 'Time to practise! Ask a grown-up to help.'),

    ('badge.earned', NULL, 'You earned a new badge!'),
    ('course.done', NULL, 'You finished the whole course. Amazing work!'),
    ('program.done', NULL, 'You completed the whole year of learning. We are so proud of your effort!'),

    ('encourage', NULL, 'Every time you practise, you learn something new.'),
    ('encourage', NULL, 'Mistakes help us learn.'),
    ('encourage', NULL, 'Keep going - you''re doing great!'),
    ('encourage', NULL, 'Learning is an adventure.'),
    ('encourage', (SELECT id FROM age_group WHERE code = 'TINY'), 'You are learning so much!'),
    ('encourage', (SELECT id FROM age_group WHERE code = 'BIG'), 'Curious minds find the best answers.');
