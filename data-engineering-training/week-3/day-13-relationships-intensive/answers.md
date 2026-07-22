# Day 13 - Answers & Theoretical Explanations

### 1. What problem does a primary key solve?
A primary key provides a unique identity for every row in a table. It guarantees that no two rows are identical and allows precise retrieval, modification, or referencing of individual records without accidental updates to unrelated data.

### 2. What problem does AUTOINCREMENT solve?
AUTOINCREMENT automates ID assignment, preventing race conditions or duplicate ID generation when multiple records are created. It removes the need to manually compute the next ID integer.

### 3. What problem does a foreign key solve?
A foreign key establishes referential integrity. It guarantees that child tables can only reference records that exist in the parent table, preventing orphaned records and invalid relation mappings.

### 4. Why is `enrollments` a bridge table?
Because students and courses have a Many-to-Many ($M:N$) relationship. One student can take many courses, and one course can have many students. Relational databases require breaking $M:N$ into two One-to-Many ($1:N$) relationships using `enrollments`.

### 5. Why is `submissions` also a relationship table?
`submissions` acts as an associative entity connecting a `student` to an `assignment` while storing submission metadata such as score, timestamp, and status.

### 6. What is one-to-many in your project? Give two examples.
1. `instructors` $\rightarrow$ `courses`: One instructor teaches multiple courses, but each course has only one assigned instructor.
2. `courses` $\rightarrow$ `assignments`: One course hosts multiple assignments, but each assignment belongs to one specific course.

### 7. What is many-to-many in your project? Give one example.
`students` $\leftrightarrow$ `courses`: A student can take multiple courses, and a course hosts multiple students (handled through `enrollments`).

### 8. Why should we not store `instructor_name` directly inside every course report table?
Storing `instructor_name` directly creates data redundancy and update anomalies. If an instructor updates their legal name, changing it across multiple course/report entries is error-prone. Normalizing it in `instructors` ensures a single source of truth.

### 9. What is the difference between INNER JOIN and LEFT JOIN?
- **`INNER JOIN`**: Returns only rows where matching values exist in both connected tables.
- **`LEFT JOIN`**: Returns all records from the left table, along with matching rows from the right table. If no match exists, `NULL` values are returned for the right table's columns.

### 10. Which constraint test was most important and why?
The `FOREIGN KEY` constraints (`enrollments.student_id` and `enrollments.course_id`) and the `UNIQUE(student_id, course_id)` constraint were most vital. They prevent corrupted relational links and stop duplicate enrollment entries from skewing attendance and scoring metrics.

### 11. How does this prepare you for Databricks tables and reporting?
In Databricks (Delta Lake / Unity Catalog), designing structured star schemas, dimensional models, and primary/foreign key logical models guarantees high data quality. Understanding joins, grouping, and integrity rules directly translates to building optimized Databricks Spark SQL pipelines.