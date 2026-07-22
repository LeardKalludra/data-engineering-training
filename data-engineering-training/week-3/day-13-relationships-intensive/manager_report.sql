-- 1. Which courses have the most enrollments?
SELECT c.course_name, COUNT(e.enrollment_id) AS total_enrollments
FROM courses c
LEFT JOIN enrollments e ON c.course_id = e.course_id
GROUP BY c.course_id, c.course_name
ORDER BY total_enrollments DESC;

-- 2. Which students are active in more than one course?
SELECT s.full_name AS student_name, COUNT(e.course_id) AS active_courses_count
FROM students s
INNER JOIN enrollments e ON s.student_id = e.student_id
WHERE e.status = 'active'
GROUP BY s.student_id, s.full_name
HAVING COUNT(e.course_id) > 1;

-- 3. Which course has the strongest average attendance?
SELECT c.course_name, ROUND(AVG(att.minutes_attended), 2) AS avg_minutes
FROM courses c
INNER JOIN enrollments e ON c.course_id = e.course_id
INNER JOIN attendance att ON e.enrollment_id = att.enrollment_id
GROUP BY c.course_id, c.course_name
ORDER BY avg_minutes DESC
LIMIT 1;

-- 4. Which course has the weakest assignment completion (most missing/late submissions)?
SELECT c.course_name, COUNT(sub.submission_id) AS problematic_submissions_count
FROM courses c
INNER JOIN assignments a ON c.course_id = a.course_id
INNER JOIN submissions sub ON a.assignment_id = sub.assignment_id
WHERE sub.status IN ('missing', 'late')
GROUP BY c.course_id, c.course_name
ORDER BY problematic_submissions_count DESC;

-- 5. Which students need attention because of missing/late submissions?
SELECT s.full_name AS student_name, s.email, c.course_name, a.title AS assignment_title, sub.status
FROM submissions sub
INNER JOIN students s ON sub.student_id = s.student_id
INNER JOIN assignments a ON sub.assignment_id = a.assignment_id
INNER JOIN courses c ON a.course_id = c.course_id
WHERE sub.status IN ('missing', 'late');

-- 6. Which instructor is responsible for the highest number of active enrollments?
SELECT i.full_name AS instructor_name, COUNT(e.enrollment_id) AS active_enrollments_count
FROM instructors i
INNER JOIN courses c ON i.instructor_id = c.instructor_id
INNER JOIN enrollments e ON c.course_id = e.course_id
WHERE e.status = 'active'
GROUP BY i.instructor_id, i.full_name
ORDER BY active_enrollments_count DESC
LIMIT 1;

-- 7. Final Combined Master Management Report
SELECT 
    s.full_name AS student_name,
    c.course_name,
    i.full_name AS instructor_name,
    e.status AS enrollment_status,
    COUNT(DISTINCT att.attendance_id) AS total_sessions,
    SUM(CASE WHEN att.attended = 1 THEN 1 ELSE 0 END) AS attended_sessions,
    COALESCE(SUM(att.minutes_attended), 0) AS total_minutes,
    COALESCE(ROUND(AVG(sub.score), 2), 0) AS average_score
FROM enrollments e
INNER JOIN students s ON e.student_id = s.student_id
INNER JOIN courses c ON e.course_id = c.course_id
INNER JOIN instructors i ON c.instructor_id = i.instructor_id
LEFT JOIN attendance att ON e.enrollment_id = att.enrollment_id
LEFT JOIN assignments a ON c.course_id = a.course_id
LEFT JOIN submissions sub ON a.assignment_id = sub.assignment_id AND sub.student_id = s.student_id
GROUP BY e.enrollment_id, s.full_name, c.course_name, i.full_name, e.status;