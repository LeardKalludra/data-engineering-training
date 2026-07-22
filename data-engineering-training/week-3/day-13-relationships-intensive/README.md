# Day 13 - Intensive Relationships and Foreign Keys

## Project Goal
Design, construct, test, and query a relational database system enforcing primary keys, foreign keys, auto-increment fields, data integrity constraints, and bridge tables for Unity Tech Hub training management.

## Database Design
The schema uses 7 normalized tables to eliminate duplicate data, enforce referential integrity, and generate reliable analytics:
- `students`
- `instructors`
- `courses`
- `enrollments` (Bridge table)
- `attendance`
- `assignments`
- `submissions`

## Tables and Relationships
- **Instructors to Courses**: $1:N$
- **Students to Courses**: $M:N$ (via `enrollments`)
- **Enrollments to Attendance**: $1:N$
- **Courses to Assignments**: $1:N$
- **Assignments / Students to Submissions**: $1:N$

## Primary Keys, Foreign Keys, and Constraints
- **Primary Keys**: Assigned to every table (`INTEGER PRIMARY KEY AUTOINCREMENT`).
- **Foreign Keys**: Configured on all child tables with strict referential validation.
- **Constraints**:
  - `NOT NULL` for crucial metadata.
  - `UNIQUE(student_id, course_id)` in `enrollments` to prevent double-registration.
  - `UNIQUE(email)` in `students`.
  - `CHECK` constraints on `level`, `status`, `attended`, `minutes_attended >= 0`, and `score >= 0`.

## Seed Data
Includes realistic entity records representing students across Kosovo cities, instructors, active/completed courses, attendance logs, assignments, and submissions. Included intentional edge-cases like an unenrolled student (`Arta Shala`) and an unsubmitted assignment for `LEFT JOIN` testing.

## Constraint Tests
Verified database defenses against:
1. Non-existent foreign key references (instructors, students, courses, assignments).
2. Duplicate student course enrollments.
3. Invalid categorical check constraints (e.g., `level = 'Expert'`).
4. Negative values for numeric fields (e.g., negative scores or attendance minutes).
5. Duplicate user emails.

## JOIN Reports
Developed multi-level analytical reports:
- **Beginner**: Selects, basic joins across entities.
- **Intermediate**: Detailed enrollment, attendance, and assignment grading joins.
- **Advanced**: Aggregations (`COUNT`, `AVG`), `HAVING` filters, and `LEFT JOIN` checks for missing links.

## Manager Report
Built high-level operational metrics identifying highest-demand courses, active multi-course students, top attendance modules, problematic assignment completion, and instructor performance.

## Screenshots
Place screenshots in `screenshots/` directory:
- `01_schema_execution.png`: Clean execution of `schema.sql`.
- `02_seed_data.png`: Verification of populated records.
- `03_failed_constraints.png`: Foreign key and UNIQUE rejection errors.
- `04_join_reports.png`: Intermediate and Advanced JOIN execution outputs.
- `05_manager_report.png`: Master managerial consolidated query results.

## What I Can Explain Live
- Why $M:N$ relationships require a bridge table.
- Difference between `INNER JOIN` vs `LEFT JOIN` when reporting missing data.
- How relational integrity constraints protect downstream pipeline reliability in Data Engineering.

## What I Would Improve Next
- Implement SQLite triggers to dynamically enforce `submissions.score <= assignments.max_score`.
- Add index optimizations on foreign key columns (`student_id`, `course_id`) for higher query efficiency on large datasets.