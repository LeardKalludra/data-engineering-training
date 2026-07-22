-- Seed Instructors (3 instructors)
INSERT INTO instructors (full_name, specialization) VALUES
('Arben Krasniqi', 'Data Engineering & Databricks'),
('Elira Berisha', 'Python & Backend Systems'),
('Driton Hoxha', 'SQL & Relational Databases');

-- Seed Courses (5 courses)
INSERT INTO courses (course_name, level, instructor_id) VALUES
('SQL & Database Design', 'Beginner', 3),
('Python Data Logic', 'Intermediate', 2),
('Databricks Fundamentals', 'Intermediate', 1),
('PySpark Data Pipelines', 'Advanced', 1),
('Data Modeling & Engineering', 'Advanced', 3);

-- Seed Students (8 students, student 8 has no enrollment for LEFT JOIN testing)
INSERT INTO students (full_name, city, email) VALUES
('Leard Kalludra', 'Mitrovica', 'leard.kalludra@example.com'),
('Laurent Meholli', 'Prishtina', 'laurent.meholli@example.com'),
('Rijon Rirxy', 'Mitrovica', 'rijon.rirxy@example.com'),
('Andre Gashi', 'Peja', 'andre.gashi@example.com'),
('Erlis Kastrati', 'Prizren', 'erlis.kastrati@example.com'),
('Korab Rama', 'Ferizaj', 'korab.rama@example.com'),
('Yllza Azemi', 'Vushtrri', 'yllza.azemi@example.com'),
('Arta Shala', 'Gjakova', 'arta.shala@example.com'); -- Unenrolled student

-- Seed Enrollments (12 enrollments across students 1-7)
INSERT INTO enrollments (student_id, course_id, enrollment_date, status) VALUES
(1, 1, '2026-07-01', 'completed'),
(1, 3, '2026-07-10', 'active'),
(2, 1, '2026-07-01', 'completed'),
(2, 2, '2026-07-05', 'active'),
(2, 4, '2026-07-12', 'active'),
(3, 2, '2026-07-05', 'active'),
(3, 3, '2026-07-10', 'active'),
(4, 1, '2026-07-01', 'active'),
(5, 3, '2026-07-10', 'active'),
(5, 5, '2026-07-15', 'active'),
(6, 4, '2026-07-12', 'active'),
(7, 5, '2026-07-15', 'active');

-- Seed Attendance (18 records)
INSERT INTO attendance (enrollment_id, session_date, attended, minutes_attended) VALUES
(1, '2026-07-02', 1, 120),
(1, '2026-07-04', 1, 115),
(2, '2026-07-11', 1, 120),
(2, '2026-07-13', 0, 0),
(3, '2026-07-02', 1, 120),
(3, '2026-07-04', 1, 120),
(4, '2026-07-06', 1, 90),
(4, '2026-07-08', 1, 100),
(5, '2026-07-13', 1, 120),
(6, '2026-07-06', 1, 110),
(7, '2026-07-11', 1, 120),
(8, '2026-07-02', 0, 0),
(9, '2026-07-11', 1, 120),
(10, '2026-07-16', 1, 120),
(11, '2026-07-13', 1, 105),
(12, '2026-07-16', 1, 120),
(1, '2026-07-06', 1, 120),
(3, '2026-07-06', 1, 120);

-- Seed Assignments (6 assignments across courses 1-4; course 5 has no assignment for LEFT JOIN testing)
INSERT INTO assignments (course_id, title, max_score, due_date) VALUES
(1, 'SQL Joins & Aggregations', 100, '2026-07-08'),
(1, 'Relational Database Design', 100, '2026-07-15'),
(2, 'Python Data Structures', 50, '2026-07-12'),
(3, 'Databricks Lakehouse Setup', 100, '2026-07-18'),
(4, 'PySpark Pipeline Processing', 100, '2026-07-20'),
(5, 'Data Vault Modeling Task', 100, '2026-07-25'); -- Has no submissions

-- Seed Submissions (12 submissions with mixed statuses)
INSERT INTO submissions (assignment_id, student_id, score, status) VALUES
(1, 1, 98.5, 'submitted'),
(1, 2, 95.0, 'submitted'),
(1, 4, 88.0, 'submitted'),
(2, 1, 100.0, 'submitted'),
(2, 2, 92.0, 'submitted'),
(3, 2, 48.0, 'submitted'),
(3, 3, 40.0, 'late'),
(4, 1, 95.0, 'submitted'),
(4, 3, 0.0, 'missing'),
(4, 5, 89.0, 'submitted'),
(5, 2, 91.0, 'submitted'),
(5, 6, 0.0, 'missing');