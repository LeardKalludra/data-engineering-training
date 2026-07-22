-- ============================================================================
-- BEGINNER REPORTS
-- ============================================================================

-- Beginner 1: Show all students with their city and email
SELECT full_name, city, email 
FROM students;

-- Beginner 2: Show all courses with instructor name and specialization
SELECT c.course_name, c.level, i.full_name AS instructor_name, i.specialization
FROM courses c
INNER JOIN instructors i ON c.instructor_id = i.instructor_id;

-- Beginner 3: Show all assignments with course name and due date
SELECT a.title AS assignment_title, c.course_name, a.due_date, a.max_score
FROM assignments a
INNER JOIN courses c ON a.course_id = c.course_id;


-- ============================================================================
-- INTERMEDIATE REPORTS
-- ============================================================================

-- Intermediate 1: Show all enrollments with student name, course name, enrollment date, and status
SELECT s.full_name AS student_name, c.course_name, e.enrollment_date, e.status
FROM enrollments e
INNER JOIN students s ON e.student_id = s.student_id
INNER JOIN courses c ON e.course_id = c.course_id;

-- Intermediate 2: Show only active enrollments
SELECT s.full_name AS student_name, c.course_name, e.enrollment_date, e.status
FROM enrollments e
INNER JOIN students s ON e.student_id = s.student_id
INNER JOIN courses c ON e.course_id = c.course_id
WHERE e.status = 'active';

-- Intermediate 3: Show attendance records with student, course, session date, attended, and minutes
SELECT s.full_name AS student_name, c.course_name, att.session_date, att.attended, att.minutes_attended
FROM attendance att
INNER JOIN enrollments e ON att.enrollment_id = e.enrollment_id
INNER JOIN students s ON e.student_id = s.student_id
INNER JOIN courses c ON e.course_id = c.course_id;

-- Intermediate 4: Show submissions with student name, assignment title, course name, score, and status
SELECT s.full_name AS student_name, a.title AS assignment_title, c.course_name, sub.score, sub.status
FROM submissions sub
INNER JOIN students s ON sub.student_id = s.student_id
INNER JOIN assignments a ON sub.assignment_id = a.assignment_id
INNER JOIN courses c ON a.course_id = c.course_id;


-- ============================================================================
-- ADVANCED REPORTS
-- ============================================================================

-- Advanced 1: Count students enrolled in each course
SELECT c.course_name, COUNT(e.enrollment_id) AS total_enrolled_students
FROM courses c
LEFT JOIN enrollments e ON c.course_id = e.course_id
GROUP BY c.course_id, c.course_name;

-- Advanced 2: Show students enrolled in more than one course
SELECT s.full_name AS student_name, COUNT(e.course_id) AS enrolled_courses_count
FROM students s
INNER JOIN enrollments e ON s.student_id = e.student_id
GROUP BY s.student_id, s.full_name
HAVING COUNT(e.course_id) > 1;

-- Advanced 3: Show average attendance minutes by course
SELECT c.course_name, ROUND(AVG(att.minutes_attended), 2) AS avg_attendance_minutes
FROM courses c
INNER JOIN enrollments e ON c.course_id = e.course_id
INNER JOIN attendance att ON e.enrollment_id = att.enrollment_id
GROUP BY c.course_id, c.course_name;

-- Advanced 4: Show average score by course
SELECT c.course_name, ROUND(AVG(sub.score), 2) AS avg_course_score
FROM courses c
INNER JOIN assignments a ON c.course_id = a.course_id
INNER JOIN submissions sub ON a.assignment_id = sub.assignment_id
GROUP BY c.course_id, c.course_name;

-- Advanced 5: Show missing or late submissions with student and course context
SELECT s.full_name AS student_name, c.course_name, a.title AS assignment_title, sub.status, sub.score
FROM submissions sub
INNER JOIN students s ON sub.student_id = s.student_id
INNER JOIN assignments a ON sub.assignment_id = a.assignment_id
INNER JOIN courses c ON a.course_id = c.course_id
WHERE sub.status IN ('missing', 'late');

-- Advanced 6: Use LEFT JOIN to show students with no enrollments
SELECT s.student_id, s.full_name, s.email, s.city
FROM students s
LEFT JOIN enrollments e ON s.student_id = e.student_id
WHERE e.enrollment_id IS NULL;

-- Advanced 7: Use LEFT JOIN to show assignments with no submissions
SELECT a.assignment_id, a.title AS assignment_title, c.course_name, a.due_date
FROM assignments a
INNER JOIN courses c ON a.course_id = c.course_id
LEFT JOIN submissions sub ON a.assignment_id = sub.assignment_id
WHERE sub.submission_id IS NULL;