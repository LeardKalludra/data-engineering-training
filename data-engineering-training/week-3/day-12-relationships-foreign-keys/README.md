# Day 12 Relationships, Foreign Keys, and JOINS

## Project Goal
Design and build a normalized relational database in SQLite for a Kosovo technology vendor[cite: 1]. The schema enforces data integrity through Primary Keys, Foreign Keys, and CHECK constraints while facilitating business reporting via SQL JOINs[cite: 1].

## Database Tables
1. **`customers`**: Stores customer profiles (`customer_id`, `customer_name`, `city`, `segment`)[cite: 1].
2. **`products`**: Stores catalog items (`product_id`, `product_name`, `category`, `price`)[cite: 1].
3. **`orders`**: Tracks order headers (`order_id`, `customer_id`, `order_date`, `status`, `channel`)[cite: 1].
4. **`order_items`**: Junction table bridging orders and products (`order_item_id`, `order_id`, `product_id`, `quantity`)[cite: 1].

## Primary Keys
A Primary Key uniquely identifies every individual record in a database table[cite: 1]. It prevents duplicate rows and guarantees fast indexing and retrieval[cite: 1].

## Foreign Keys
A Foreign Key links a column in a child table to the Primary Key of a parent table[cite: 1]. It enforces referential integrity, ensuring child rows cannot reference non-existent parent IDs[cite: 1].

## Auto Increment Answers
34. **Missing ID Insert**: SQLite automatically assigned an incremental integer (starting at 1) to `customer_id`[cite: 1].
35. **Why AUTOINCREMENT is Useful**: It prevents key collision errors and eliminates manual management of unique IDs across high-concurrency environments[cite: 1].
36. **Manual IDs in Production**: No[cite: 1]. Manual key generation leads to race conditions and duplicate key errors in distributed systems[cite: 1].
37. **Row Deletion Behaviour**: SQLite preserves internal sequence counters; deleting an ID will not cause `AUTOINCREMENT` to reassign that deleted integer[cite: 1].
38. **Unique ID vs Name**: Customer names are not guaranteed to be unique or permanent (e.g., name changes)[cite: 1]. Stable integer keys optimize join performance and avoid breaking foreign key constraints[cite: 1].

## Relationships
* **1:N (Customers $\rightarrow$ Orders)**: One customer places multiple orders[cite: 1].
* **M:N (Orders $\leftrightarrow$ Products)**: Implemented through `order_items`[cite: 1]. An order contains many products, and a product appears in many orders[cite: 1].

## Valid and Invalid Insert Tests
All constraint failure scenarios (Foreign Key breaches, negative price violations, invalid status codes) were verified in `relationship_tests.sql` and documented under `mistakes_and_fixes.md`[cite: 1].

## INNER JOIN vs LEFT JOIN
33. **Difference**: 
    * `INNER JOIN` returns only matched rows from both tables[cite: 1]. Unmatched rows are completely excluded[cite: 1].
    * `LEFT JOIN` returns **all** records from the left table regardless of matches, filling missing right-table fields with `NULL`[cite: 1].

## Business Reports
All financial revenue metrics filter strictly for `status = 'completed'` to avoid inflating financial performance with pending or canceled purchases[cite: 1].

## What I Can Explain Live
* Why junction tables are required for M:N relationships[cite: 1].
* The order of operations when executing `DROP TABLE IF EXISTS`[cite: 1].
* How referential integrity prevents orphan records in data pipelines[cite: 1].

## What I Would Improve Next
* Add automated database migration scripts.
* Implement indexes on frequently joined columns (`customer_id`, `product_id`).