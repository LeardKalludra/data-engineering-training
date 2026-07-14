-- =====================================================
-- Fixed Query 1
-- Purpose: Count the number of orders for each city.
-- Fix: The city column belongs to the customers table,
-- so a JOIN is required before grouping by city.
-- Business Meaning: Shows which cities have the most orders.
-- =====================================================

SELECT customers.city, COUNT(*) AS order_count
FROM orders
JOIN customers
    ON orders.customer_id = customers.customer_id
GROUP BY customers.city;


-- =====================================================
-- Fixed Query 2
-- Purpose: Calculate completed revenue for each product.
-- Fix: Added the missing comma after product_name.
-- Business Meaning: Shows how much revenue each product generated.
-- =====================================================

SELECT product_name, SUM(quantity * price) AS revenue
FROM orders
JOIN products
    ON orders.product_id = products.product_id
WHERE status = 'completed'
GROUP BY product_name;


-- =====================================================
-- Fixed Query 3
-- Purpose: Count orders by status.
-- Fix: ORDER BY must come before the semicolon and be
-- part of the same SQL statement.
-- Business Meaning: Shows how many orders are completed,
-- pending, and cancelled.
-- =====================================================

SELECT status, COUNT(*) AS order_count
FROM orders
GROUP BY status
ORDER BY order_count DESC;


-- =====================================================
-- Fixed Query 4
-- Purpose: Calculate the total amount for every order.
-- Fix: The price column belongs to the products table,
-- so a JOIN is required.
-- Business Meaning: Shows the value of each order.
-- =====================================================

SELECT order_id,
       quantity,
       price,
       quantity * price AS total_amount
FROM orders
JOIN products
    ON orders.product_id = products.product_id;


-- =====================================================
-- Fixed Query 5
-- Purpose: Calculate completed quantity sold by category.
-- Fix: Category belongs to the products table, so a JOIN
-- is required.
-- Business Meaning: Shows which product categories sold
-- the most completed items.
-- =====================================================

SELECT category,
       SUM(quantity) AS total_quantity
FROM orders
JOIN products
    ON orders.product_id = products.product_id
WHERE status = 'completed'
GROUP BY category;


-- =====================================================
-- Fixed Query 6
-- Purpose: Calculate total completed revenue.
-- Fix: Added a WHERE clause to include only completed
-- orders.
-- Business Meaning: Shows the actual completed revenue.
-- =====================================================

SELECT SUM(quantity * price) AS total_revenue
FROM orders
JOIN products
    ON orders.product_id = products.product_id
WHERE status = 'completed';


-- =====================================================
-- Fixed Query 7
-- Purpose: Find customers with more than one order.
-- Fix: HAVING must come after GROUP BY.
-- Business Meaning: Identifies repeat customers.
-- =====================================================

SELECT customer_id,
       COUNT(*) AS order_count
FROM orders
GROUP BY customer_id
HAVING COUNT(*) > 1;


-- =====================================================
-- Fixed Query 8
-- Purpose: Display each order with the customer name.
-- Fix: Added the missing JOIN condition using the
-- customer_id column.
-- Business Meaning: Matches every order to its customer.
-- =====================================================

SELECT orders.order_id,
       customers.customer_name
FROM orders
JOIN customers
    ON orders.customer_id = customers.customer_id;


-- =====================================================
-- Fixed Query 9
-- Purpose: Display customer, product, and price.
-- Fix: Qualified customer_id with the table name to avoid
-- ambiguity.
-- Business Meaning: Shows which customer ordered which
-- product and its price.
-- =====================================================

SELECT orders.customer_id,
       orders.product_id,
       products.price
FROM orders
JOIN products
    ON orders.product_id = products.product_id;


-- =====================================================
-- Fixed Query 10
-- Purpose: Show orders that should NOT count as revenue.
-- Fix: The original query returned completed orders.
-- It should instead return non-completed orders.
-- Business Meaning: Displays pending and cancelled orders
-- that are excluded from revenue calculations.
-- =====================================================

SELECT *
FROM orders
WHERE status <> 'completed';