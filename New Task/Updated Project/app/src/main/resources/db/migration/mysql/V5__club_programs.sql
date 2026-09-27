-- D78: each club gets its own course set. Until now every Year-1 program held every published course
-- (DD-20), so a Tiny Cub saw the whole catalogue. This clears those rows; at the next start ContentSeeder
-- fills each program from resources/programs/year-1.json (it seeds programs whenever program_course is
-- empty). Progress, quiz tries, badges and enrolments are untouched. The same file exists for PostgreSQL.
DELETE FROM program_course;
