-- Task S1: Show all orders
SELECT * FROM orders;

-- Task S1: Show only customer_name and product
SELECT customer_name, product FROM orders;

-- Task S1: Show order_id, customer_name, city, and status
SELECT order_id, customer_name, city, status FROM orders;

-- Task S1: Show product, category, quantity, and price
SELECT product, category, quantity, price FROM orders;


-- Task S2: Show only completed orders
SELECT * FROM orders WHERE status = "completed";

-- Task S2: Show only pending orders
SELECT * FROM orders WHERE status = "pending";

-- Task S2: Show only cancelled orders
SELECT * FROM orders WHERE status = "cancelled";

-- Task S2: Show orders where price is greater than 100
SELECT * FROM orders WHERE price > 100;

-- Task S2: Show orders from Vushtrri
SELECT * FROM orders WHERE city = "Vushtrri";

-- Task S2: Show orders where category is Accessories
SELECT * FROM orders WHERE category = "Accessories";


-- Task S3: Show completed orders where price is greater than 100
SELECT * FROM orders WHERE status = "completed" AND price > 100;

-- Task S3: Show completed orders from Prishtina
SELECT * FROM orders WHERE status = "completed" AND city = "Prishtina";

-- Task S3: Show orders where status is pending OR cancelled
SELECT * FROM orders WHERE status = "pending" OR status = "cancelled";

-- Task S3: Show Accessories orders where price is less than 50
SELECT * FROM orders WHERE category = "Accessories" AND price < 50;


-- Task S4: Show orders from cheapest to most expensive
SELECT * FROM orders ORDER BY price ASC;

-- Task S4: Show orders from most expensive to cheapest
SELECT * FROM orders ORDER BY price DESC;

-- Task S4: Show top 3 most expensive orders by price
SELECT * FROM orders ORDER BY price DESC LIMIT 3;

-- Task S4: Show top 3 orders by total_amount
SELECT * FROM orders ORDER BY (quantity * price) DESC LIMIT 3;


-- Task S5: Show customer_name, product, quantity, price, and total_amount
SELECT customer_name, product, quantity, price, (quantity * price) AS total_amount FROM orders;

-- Task S5: Show only completed orders with total_amount
SELECT *, (quantity * price) AS total_amount FROM orders WHERE status = "completed";

-- Task S5: Show completed orders with total_amount sorted from highest to lowest
SELECT *, (quantity * price) AS total_amount FROM orders WHERE status = "completed" ORDER BY total_amount DESC;


-- Part 4: Find the customer with the most expensive single order
SELECT customer_name, price FROM orders ORDER BY price DESC LIMIT 1;

-- Part 4: Find the highest total_amount order
SELECT customer_name, product, (quantity * price) AS total_amount FROM orders ORDER BY total_amount DESC LIMIT 1;

-- Part 4: Find all orders that should NOT be counted as real revenue because they are pending or cancelled
SELECT * FROM orders WHERE status = "pending" OR status = "cancelled";

-- Part 4: Calculate completed revenue only
SELECT SUM(quantity * price) AS completed_revenue FROM orders WHERE status = "completed";


-- Bonus: Insert two new rows into the dataset
INSERT INTO orders (order_id, customer_name, city, product, category, quantity, price, status, order_date) VALUES
(13, "Agon", "Prishtina", "Tablet", "Electronics", 1, 300, "completed", "2026-07-07"),
(14, "Vala", "Peja", "Paper", "Office", 5, 5, "cancelled", "2026-07-07");

-- Bonus: Use COUNT(*) to count all orders
SELECT COUNT(*) AS total_order_count FROM orders;

-- Bonus: Use SUM(quantity * price) for completed orders only
SELECT SUM(quantity * price) AS total_completed_revenue FROM orders WHERE status = "completed";

-- Bonus: Try GROUP BY status
SELECT status, COUNT(*) AS count_by_status FROM orders GROUP BY status;

-- Bonus: Try GROUP BY city
SELECT city, COUNT(*) AS count_by_city FROM orders GROUP BY city;