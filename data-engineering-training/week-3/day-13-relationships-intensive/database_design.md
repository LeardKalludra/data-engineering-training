# Database Design Document - Day 13 Intensive Practice

## 1. Entity Descriptions & Relationship Logic

| Entity/Table | Represents | Relationship Logic |
| :--- | :--- | :--- |
| `students` | People attending training. | One student can have many enrollments and many assignment submissions. |
| `instructors` | Teachers assigned to courses. | One instructor can teach many courses. |
| `courses` | Training modules/courses offered. | One course is taught by one instructor and can have many enrollments and assignments. |
| `enrollments` | Bridge between students and courses. | Connects many students to many courses (Many-to-Many). |
| `attendance` | Attendance records per enrollment session. | One enrollment can have multiple attendance records. |
| `assignments` | Tasks created for a course. | One course can have many assignments. |
| `submissions` | Assignment work submitted by students. | Connects one student to one assignment (stores score and submission status). |

---

## 2. Primary Keys & Foreign Keys

### Primary Keys (PK)
- `students`: `student_id`
- `instructors`: `instructor_id`
- `courses`: `course_id`
- `enrollments`: `enrollment_id`
- `attendance`: `attendance_id`
- `assignments`: `assignment_id`
- `submissions`: `submission_id`

### Foreign Keys (FK)
- `courses.instructor_id` $\rightarrow$ References `instructors(instructor_id)`
- `enrollments.student_id` $\rightarrow$ References `students(student_id)`
- `enrollments.course_id` $\rightarrow$ References `courses(course_id)`
- `attendance.enrollment_id` $\rightarrow$ References `enrollments(enrollment_id)`
- `assignments.course_id` $\rightarrow$ References `courses(course_id)`
- `submissions.assignment_id` $\rightarrow$ References `assignments(assignment_id)`
- `submissions.student_id` $\rightarrow$ References `students(student_id)`

---

## 3. Relationship Definitions

### One-to-Many ($1:N$) Examples
1. **`instructors` to `courses`**: One instructor can teach multiple courses, but each course is assigned to exactly one instructor.
2. **`courses` to `assignments`**: One course can have multiple assignments, but an assignment belongs to a single course.
3. **`enrollments` to `attendance`**: One enrollment record can have multiple daily attendance tracking entries.

### Many-to-Many ($M:N$) Example & Bridge Table Explanation
- **`students` to `courses`**: A student can enroll in multiple courses, and a course can host multiple students. 
- **Bridge Table (`enrollments`)**: Relational databases cannot natively represent direct Many-to-Many links without massive data redundancy. The `enrollments` table acts as a bridge containing `student_id` and `course_id` as foreign keys, breaking the $M:N$ connection into two $1:N$ relationships (`students` $\rightarrow$ `enrollments` and `courses` $\rightarrow$ `enrollments`).

---

## 4. Normalization & Data Integrity

### Why `course_name` Should NOT Be Stored Inside `students`
If `course_name` were stored inside `students`:
1. **Redundancy & Storage Waste**: If 500 students enroll in "Databricks Fundamentals", the exact string `"Databricks Fundamentals"` is repeated 500 times.
2. **Update Anomalies**: If the course name changes to "Advanced Databricks", we would need to update 500 separate rows. Missing even one creates data inconsistency.
3. **Deletion Anomalies**: If a student leaves, deleting their row might delete the only record showing that a particular course exists.
4. **Multi-value Issues**: A student in 3 courses would require repeated student demographic details or messy comma-separated fields.

---

## 5. Visual Entity Relationship Text Diagram