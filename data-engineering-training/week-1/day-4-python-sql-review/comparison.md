# Part 3 - Python vs SQL Comparison

### Task 1: Show completed orders
**Python approach:**
- Loop through the orders list.
- Check if order["status"] == "completed".
- Print matching orders.

**SQL approach:**
- SELECT the columns we need.
- FROM the orders table.
- Use WHERE status = "completed".

**What I understood:**
Both approaches filter rows. Python uses an explicit for loop and if statement to look through records one by one in memory. SQL filters directly from the table using its engine rules with WHERE.

---

### Task 2: Show orders with price > 100
**Python approach:**
- Loop through the orders list.
- Check if order["price"] > 100 using an if statement.
- Print matching orders.

**SQL approach:**
- SELECT the columns we need.
- FROM the orders table.
- Use WHERE price > 100.

**What I understood:**
Both systems check a condition on an attribute. Python evaluates the condition dynamically inside an iteration pass, while SQL scans the table data blocks and discards records that do not match the WHERE condition.

---

### Task 3: Calculate total_amount
**Python approach:**
- Loop through the orders list.
- Multiply quantity * price inside the loop body.
- Store it in a variable or print it directly.

**SQL approach:**
- SELECT the columns we need.
- Use quantity * price AS total_amount to calculate on the fly.
- FROM the orders table.

**What I understood:**
Both approaches create temporary calculated values. Python requires manual multiplication math for every single step of the loop, while SQL creates a temporary calculated column for the entire result set at once using aliases.

---

### Task 4: Sort by price descending
**Python approach:**
- Use the built-in sorted() function.
- Pass a dedicated helper function (like get_price) as the sorting key.
- Set reverse=True for descending order.

**SQL approach:**
- SELECT the columns we need.
- FROM the orders table.
- Use ORDER BY price DESC.

**What I understood:**
Both operations reorder datasets. Python requires an external sorting function and an explicit key extraction utility to sort objects in RAM, while SQL handles sorting natively with the declarative ORDER BY clause.

---

### Task 5: Show top 3 orders
**Python approach:**
- Sort the orders list first by total amount.
- Use list slicing syntax [:3] to take the first three items.
- Print the sliced collection.

**SQL approach:**
- SELECT the columns we need.
- FROM the orders table.
- Use ORDER BY (quantity * price) DESC.
- Use LIMIT 3.

**What I understood:**
Both methods restrict the final record count after sorting. Python relies on collection index slicing to extract a structural subset from an array, while SQL uses the LIMIT clause to truncate the final database engine output directly.