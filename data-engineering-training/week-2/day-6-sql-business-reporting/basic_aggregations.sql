CREATE TABLE orders (
    order_id INT PRIMARY KEY,
    customer_id INT,
    product_id INT,
    order_date DATE,
    quantity INT,
    status VARCHAR(50)
);

INSERT INTO orders (order_id, customer_id, product_id, order_date, quantity, status) VALUES
(1, 1, 101, '2026-07-01', 1, 'completed'),
(2, 2, 102, '2026-07-01', 2, 'completed'),
(3, 1, 103, '2026-07-02', 1, 'cancelled'),
(4, 3, 104, '2026-07-02', 1, 'completed'),
(5, 4, 102, '2026-07-03', 1, 'completed'),
(6, 3, 101, '2026-07-03', 1, 'pending'),
(7, 5, 105, '2026-07-04', 1, 'completed'),
(8, 6, 104, '2026-07-04', 2, 'completed'),
(9, 7, 106, '2026-07-05', 1, 'completed'),
(10, 2, 107, '2026-07-05', 3, 'completed'),
(11, 8, 101, '2026-07-06', 1, 'cancelled'),
(12, 9, 108, '2026-07-06', 1, 'pending'),
(13, 10, 102, '2026-07-07', 4, 'completed'),
(14, 4, 105, '2026-07-07', 2, 'completed');

CREATE TABLE customers (
    customer_id INT PRIMARY KEY,
    customer_name VARCHAR(100),
    city VARCHAR(100)
);

INSERT INTO customers (customer_id, customer_name, city) VALUES
(1, 'Arta', 'Vushtrri'),
(2, 'Blend', 'Prishtina'),
(3, 'Dren', 'Mitrovica'),
(4, 'Elira', 'Prishtina'),
(5, 'Nora', 'Vushtrri'),
(6, 'Leart', 'Peja'),
(7, 'Faton', 'Prizren'),
(8, 'Rina', 'Vushtrri'),
(9, 'Arben', 'Ferizaj'),
(10, 'Gresa', 'Prishtina');

CREATE TABLE products (
    product_id INT PRIMARY KEY,
    product_name VARCHAR(100),
    category VARCHAR(100),
    price DECIMAL(10, 2)
);

INSERT INTO products (product_id, product_name, category, price) VALUES
(101, 'Laptop', 'Electronics', 700),
(102, 'Mouse', 'Accessories', 15),
(103, 'Keyboard', 'Accessories', 40),
(104, 'Monitor', 'Electronics', 180),
(105, 'Headphones', 'Accessories', 50),
(106, 'Desk Chair', 'Office', 120),
(107, 'USB Cable', 'Accessories', 8),
(108, 'Desk', 'Office', 220);

SELECT * FROM customers;
SELECT * FROM products;
SELECT * FROM orders;


-- ====================================================================
-- PART 2: BASIC METRICS & AGGREGATIONS
-- ====================================================================

-- Calculate the absolute total volume of orders logged within the system
SELECT COUNT(*) AS total_orders 
FROM orders;

-- Count how many orders were successfully processed and finalized
SELECT COUNT(*) AS completed_orders 
FROM orders 
WHERE status = 'completed';

-- Count how many orders are currently waiting to be processed
SELECT COUNT(*) AS pending_orders 
FROM orders 
WHERE status = 'pending';

-- Count how many orders were terminated or dropped before completion
SELECT COUNT(*) AS cancelled_orders 
FROM orders 
WHERE status = 'cancelled';

-- Calculate the total number of physical product items ordered across all accounts
SELECT SUM(quantity) AS total_quantity_ordered 
FROM orders;

-- Calculate the total number of physical product items ordered only within completed deals
SELECT SUM(quantity) AS completed_quantity_ordered 
FROM orders 
WHERE status = 'completed';

-- Calculate the baseline average pricing index across our entire product line
SELECT AVG(price) AS average_product_price 
FROM products;

-- Find the lowest entry-level product price point in our catalog
SELECT MIN(price) AS cheapest_product_price 
FROM products;

-- Find the premium maximum product price point in our catalog
SELECT MAX(price) AS most_expensive_product_price 
FROM products;

-- Calculate actual total net revenue realized from successfully completed transactions
SELECT SUM(o.quantity * p.price) AS total_completed_revenue
FROM orders o
JOIN products p ON o.product_id = p.product_id
WHERE o.status = 'completed';

-- Calculate total potential financial pipeline value currently locked up in pending or cancelled orders
SELECT SUM(o.quantity * p.price) AS non_completed_potential_value
FROM orders o
JOIN products p ON o.product_id = p.product_id
WHERE o.status IN ('pending', 'cancelled');


-- ====================================================================
-- PART 3: GRANULAR GROUP BY AND HAVING REPORTS
-- ====================================================================

-- View the breakdown distribution volume of all orders across their respective statuses
SELECT 
    status,
    COUNT(*) AS order_count
FROM orders
GROUP BY status;

-- Count total order volumes broken down chronologically by operational status
SELECT 
    order_date,
    COUNT(*) AS order_date_count
FROM orders
GROUP BY order_date;

-- Track active order placement volumes grouped by unique customer identifiers
SELECT 
    customer_id,
    COUNT(*) AS order_count_customer_id
FROM orders
GROUP BY customer_id;

-- Track active order placement volumes grouped by unique product catalog numbers
SELECT 
    product_id,
    COUNT(*) AS order_count_product_id
FROM orders
GROUP BY product_id;

-- Sum the total item units moved for each product ID only on cleared sales
SELECT 
    product_id,
    SUM(quantity) AS total_quantity
FROM orders
WHERE status = 'completed'
GROUP BY product_id;

-- Duplicate query verification check: Sum total item units moved for each product ID on cleared sales
SELECT 
    product_id,
    SUM(quantity) AS total_quantity
FROM orders
WHERE status = 'completed'
GROUP BY product_id;

-- Track incoming revenue streams grouped directly by product identification codes
SELECT 
    o.product_id,
    SUM(o.quantity * p.price) AS completed_revenue
FROM orders o
JOIN products p ON o.product_id = p.product_id
WHERE o.status = 'completed'
GROUP BY o.product_id;

-- Calculate completed revenue by status and explain why the result is not always a good business report.
-- The metric column is named completed_revenue, but grouping by status means the report will only ever 
-- display a single row for the "completed" status, making the GROUP BY function entirely useless.
SELECT 
    status,
    SUM(o.quantity * p.price) AS completed_revenue
FROM orders o
JOIN products p ON o.product_id = p.product_id
WHERE o.status = 'completed'
GROUP BY status;

-- Identify frequent buyers who have created more than one order log entry, ranked highest to lowest
SELECT 
    customer_id,
    COUNT(*) AS order_count
FROM orders
GROUP BY customer_id
HAVING COUNT(*) > 1
ORDER BY order_count DESC;

-- Filter out and isolate products that have moved more than 2 total clear units, ranked by units sold
SELECT 
    product_id,
    SUM(quantity) AS completed_quantity
FROM orders
WHERE status = 'completed'
GROUP BY product_id
HAVING SUM(quantity) > 2
ORDER BY completed_quantity DESC;

-- 1. What is the distribution of our transactions across different order statuses (Sorted)?
SELECT 
    status,
    COUNT(*) AS order_count
FROM orders
GROUP BY status
ORDER BY order_count DESC;

-- 2. How many orders has each customer placed (Sorted)?
SELECT 
    customer_id,
    COUNT(*) AS order_count
FROM orders
GROUP BY customer_id
ORDER BY order_count DESC;

-- 3. What is the total volume of items sold for each product (completed orders only, Sorted)?
SELECT 
    product_id,
    SUM(quantity) AS total_quantity
FROM orders
WHERE status = 'completed'
GROUP BY product_id
ORDER BY total_quantity DESC;

-- 4. What is the total revenue generated by each product from completed orders (Sorted)?
SELECT 
    o.product_id,
    SUM(o.quantity * p.price) AS completed_revenue
FROM orders o
JOIN products p ON o.product_id = p.product_id
WHERE o.status = 'completed'
GROUP BY o.product_id
ORDER BY completed_revenue DESC;

-- 5. What is the total revenue generated by each customer from completed orders (Sorted)?
SELECT 
    o.customer_id,
    SUM(o.quantity * p.price) AS completed_revenue
FROM orders o
JOIN products p ON o.product_id = p.product_id
WHERE o.status = 'completed'
GROUP BY o.customer_id
ORDER BY completed_revenue DESC;

-- 6. What is the total completed revenue grouped by order status (Duplicate validation check)?
-- Note: Sorting is omitted here because the query only yields a single row for 'completed'.
SELECT 
    status,
    SUM(o.quantity * p.price) AS completed_revenue
FROM orders o
JOIN products p ON o.product_id = p.product_id
WHERE o.status = 'completed'
GROUP BY status;

-- 7. Which customers have placed more than one order in total (Duplicate validation check)? 
SELECT 
    customer_id,
    COUNT(*) AS order_count
FROM orders
GROUP BY customer_id
HAVING COUNT(*) > 1
ORDER BY order_count DESC;

-- 8. Which products have a total completed sales quantity greater than 2 items (Duplicate validation check)? 
SELECT 
    product_id,
    SUM(quantity) AS completed_quantity
FROM orders
WHERE status = 'completed'
GROUP BY product_id
HAVING SUM(quantity) > 2
ORDER BY completed_quantity DESC;


-- ====================================================================
-- PART 4: DATA WAREHOUSE JOIN REPORTS
-- ====================================================================

-- Pull clear human-readable names and home cities for orders by joining customers metrics
SELECT 
    o.order_id,
    c.customer_name,
    c.city,
    o.order_date,
    o.status
FROM orders o
JOIN customers c ON o.customer_id = c.customer_id;

-- Expose individual order lines alongside detailed product specs, unit costs, and row valuations
SELECT 
    o.order_id,
    p.product_name,
    p.category,
    o.quantity,
    p.price,
    (o.quantity * p.price) AS total_amount,
    o.status
FROM orders o
JOIN products p ON o.product_id = p.product_id;

-- Generate a global order log joining orders, customers, and products metadata seamlessly
SELECT 
    c.customer_name,
    c.city,
    p.product_name,
    p.category,
    o.quantity,
    p.price,
    (o.quantity * p.price) AS total_amount,
    o.status,
    o.order_date
FROM orders o
JOIN customers c ON o.customer_id = c.customer_id
JOIN products p ON o.product_id = p.product_id;

-- Review total generated earnings mapped directly out by official product catalog names
SELECT 
    p.product_name,
    SUM(o.quantity * p.price) AS completed_revenue
FROM orders o
JOIN products p ON o.product_id = p.product_id
WHERE o.status = 'completed'
GROUP BY p.product_name
ORDER BY completed_revenue DESC;

-- Review total generated earnings mapped directly out by structural product inventory categories
SELECT 
    p.category,
    SUM(o.quantity * p.price) AS completed_revenue
FROM orders o
JOIN products p ON o.product_id = p.product_id
WHERE o.status = 'completed'
GROUP BY p.category
ORDER BY completed_revenue DESC;

-- Track dynamic customer traffic density levels by monitoring order intake velocity per city
SELECT 
    c.city,
    COUNT(o.order_id) AS order_count
FROM orders o
JOIN customers c ON o.customer_id = c.customer_id
GROUP BY c.city
ORDER BY order_count DESC;

-- Isolate and display financial revenue contributions organized explicitly by customer home city location
SELECT 
    c.city,
    SUM(o.quantity * p.price) AS completed_revenue
FROM orders o
JOIN customers c ON o.customer_id = c.customer_id
JOIN products p ON o.product_id = p.product_id
WHERE o.status = 'completed'
GROUP BY c.city
ORDER BY completed_revenue DESC;

-- Map overall account value scores by summing actual revenue generated per customer name
SELECT 
    c.customer_name,
    SUM(o.quantity * p.price) AS completed_revenue
FROM orders o
JOIN customers c ON o.customer_id = c.customer_id
JOIN products p ON o.product_id = p.product_id
WHERE o.status = 'completed'
GROUP BY c.customer_name
ORDER BY completed_revenue DESC;

-- List all active customers who have initiated more than one separate order across our database
SELECT 
    c.customer_name,
    COUNT(o.order_id) AS order_count
FROM orders o
JOIN customers c ON o.customer_id = c.customer_id
GROUP BY c.customer_name
HAVING COUNT(o.order_id) > 1
ORDER BY order_count DESC;

-- Highlight our absolute top 3 highest-spending consumers according to completed cash flow parameters
SELECT 
    c.customer_name,
    SUM(o.quantity * p.price) AS completed_revenue
FROM orders o
JOIN customers c ON o.customer_id = c.customer_id
JOIN products p ON o.product_id = p.product_id
WHERE o.status = 'completed'
GROUP BY c.customer_name
ORDER BY completed_revenue DESC
LIMIT 3;

-- Highlight our absolute top 3 highest-earning product lines according to completed cash flow parameters
SELECT 
    p.product_name,
    SUM(o.quantity * p.price) AS completed_revenue
FROM orders o
JOIN products p ON o.product_id = p.product_id
WHERE o.status = 'completed'
GROUP BY p.product_name
ORDER BY completed_revenue DESC
LIMIT 3;

-- Isolate all transactions categorized as pending or cancelled alongside details on potential values lost or delayed
SELECT 
    c.customer_name,
    c.city,
    p.product_name,
    (o.quantity * p.price) AS potential_amount,
    o.status
FROM orders o
JOIN customers c ON o.customer_id = c.customer_id
JOIN products p ON o.product_id = p.product_id
WHERE o.status IN ('pending', 'cancelled')
ORDER BY potential_amount DESC;