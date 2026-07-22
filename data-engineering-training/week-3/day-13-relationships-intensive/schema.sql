-- Enable foreign key enforcement in SQLite
PRAGMA foreign_keys = ON;

-- Drop tables if they already exist to ensure a clean setup
DROP TABLE IF EXISTS submissions;
DROP TABLE IF EXISTS assignments;
DROP TABLE IF EXISTS attendance;
DROP TABLE IF EXISTS enrollments;
DROP TABLE IF EXISTS courses;
DROP TABLE IF EXISTS instructors;
DROP TABLE IF EXISTS students;

-- 1. Students Table
CREATE TABLE students (
    student_id INTEGER PRIMARY KEY AUTOINCREMENT,
    full_name TEXT NOT NULL,
    city TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- 2. Instructors Table
CREATE TABLE instructors (
    instructor_id INTEGER PRIMARY KEY AUTOINCREMENT,
    full_name TEXT NOT NULL,
    specialization TEXT NOT NULL
);

-- 3. Courses Table
CREATE TABLE courses (
    course_id INTEGER PRIMARY KEY AUTOINCREMENT,
    course_name TEXT NOT NULL,
    level TEXT CHECK(level IN ('Beginner', 'Intermediate', 'Advanced')),
    instructor_id INTEGER NOT NULL,
    FOREIGN KEY (instructor_id) REFERENCES instructors(instructor_id)
);

-- 4. Enrollments Table (Bridge Table for Students <-> Courses)
CREATE TABLE enrollments (
    enrollment_id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER NOT NULL,
    course_id INTEGER NOT NULL,
    enrollment_date DATE DEFAULT CURRENT_DATE,
    status TEXT CHECK(status IN ('active', 'completed', 'dropped')),
    FOREIGN KEY (student_id) REFERENCES students(student_id),
    FOREIGN KEY (course_id) REFERENCES courses(course_id),
    CONSTRAINT unique_student_course UNIQUE (student_id, course_id)
);

-- 5. Attendance Table
CREATE TABLE attendance (
    attendance_id INTEGER PRIMARY KEY AUTOINCREMENT,
    enrollment_id INTEGER NOT NULL,
    session_date DATE NOT NULL,
    attended INTEGER CHECK(attended IN (0, 1)),
    minutes_attended INTEGER CHECK(minutes_attended >= 0),
    FOREIGN KEY (enrollment_id) REFERENCES enrollments(enrollment_id)
);

-- 6. Assignments Table
CREATE TABLE assignments (
    assignment_id INTEGER PRIMARY KEY AUTOINCREMENT,
    course_id INTEGER NOT NULL,
    title TEXT NOT NULL,
    max_score REAL CHECK(max_score > 0),
    due_date DATE NOT NULL,
    FOREIGN KEY (course_id) REFERENCES courses(course_id)
);

-- 7. Submissions Table
CREATE TABLE submissions (
    submission_id INTEGER PRIMARY KEY AUTOINCREMENT,
    assignment_id INTEGER NOT NULL,
    student_id INTEGER NOT NULL,
    submitted_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    score REAL CHECK(score >= 0),
    status TEXT CHECK(status IN ('submitted', 'missing', 'late')),
    FOREIGN KEY (assignment_id) REFERENCES assignments(assignment_id),
    FOREIGN KEY (student_id) REFERENCES students(student_id)
);