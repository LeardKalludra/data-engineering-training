PRAGMA foreign_keys = ON;

-- 1. Test: Invalid course instructor (Foreign Key Violation)
-- Expected Result: FAILS because instructor_id 999 does not exist in instructors.
-- INSERT INTO courses (course_name, level, instructor_id) VALUES ('Invalid Course', 'Beginner', 999);

-- 2. Test: Invalid enrollment student (Foreign Key Violation)
-- Expected Result: FAILS because student_id 999 does not exist in students.
-- INSERT INTO enrollments (student_id, course_id, status) VALUES (999, 1, 'active');

-- 3. Test: Invalid enrollment course (Foreign Key Violation)
-- Expected Result: FAILS because course_id 999 does not exist in courses.
-- INSERT INTO enrollments (student_id, course_id, status) VALUES (1, 999, 'active');

-- 4. Test: Duplicate enrollment (UNIQUE Constraint Violation)
-- Expected Result: FAILS because student 1 is already enrolled in course 1.
-- INSERT INTO enrollments (student_id, course_id, status) VALUES (1, 1, 'active');

-- 5. Test: Invalid attendance enrollment (Foreign Key Violation)
-- Expected Result: FAILS because enrollment_id 999 does not exist.
-- INSERT INTO attendance (enrollment_id, session_date, attended, minutes_attended) VALUES (999, '2026-07-20', 1, 120);

-- 6. Test: Invalid attendance minutes (CHECK Constraint Violation)
-- Expected Result: FAILS because minutes_attended must be >= 0.
-- INSERT INTO attendance (enrollment_id, session_date, attended, minutes_attended) VALUES (1, '2026-07-20', 1, -10);

-- 7. Test: Invalid course level (CHECK Constraint Violation)
-- Expected Result: FAILS because level 'Expert' is not allowed by CHECK constraint.
-- INSERT INTO courses (course_name, level, instructor_id) VALUES ('Advanced ML', 'Expert', 1);

-- 8. Test: Invalid submission assignment (Foreign Key Violation)
-- Expected Result: FAILS because assignment_id 999 does not exist.
-- INSERT INTO submissions (assignment_id, student_id, score, status) VALUES (999, 1, 90.0, 'submitted');

-- 9. Test: Invalid submission score (Negative score)
-- Expected Result: FAILS because score CHECK constraint specifies score >= 0.
-- INSERT INTO submissions (assignment_id, student_id, score, status) VALUES (1, 1, -15.0, 'submitted');

-- Note on Max Score Check: Basic SQLite constraints on submissions cannot easily validate dynamically
-- against assignments.max_score without a trigger. However, negative scores are strictly rejected.

-- 10. Test: Duplicate email (UNIQUE Constraint Violation)
-- Expected Result: FAILS because email 'leard.kalludra@example.com' already exists.
-- INSERT INTO students (full_name, city, email) VALUES ('Another Leard', 'Mitrovica', 'leard.kalludra@example.com');