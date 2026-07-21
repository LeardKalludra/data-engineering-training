PRAGMA foreign_keys = ON;

-- ============================================================================
-- Level 1 - Basic SELECT and Relationship Checks
-- ============================================================================

-- 9. Show all customers
SELECT * FROM customers;

-- 10. Show all products
SELECT * FROM products;

-- 11. Show all orders
SELECT * FROM orders;

-- 12. Show all order items
SELECT * FROM order_items;

-- 13. Show only completed orders
SELECT * FROM orders WHERE status = 'completed';

-- 14. Show only pending or cancelled orders
SELECT * FROM orders WHERE status IN ('pending', 'cancelled');


-- ============================================================================
-- Level 2 - First INNER JOINs
-- ============================================================================

-- 15. Show each order with customer_name, city, order_date, status, and channel
SELECT 
    orders.order_id,
    customers.customer_name,
    customers.city,
    orders.order_date,
    orders.status,
    orders.channel
FROM orders
JOIN customers ON orders.customer_id = customers.customer_id;

-- 16. Show each order_item with product_name, category, price, and quantity
SELECT 
    order_items.order_item_id,
    order_items.order_id,
    products.product_name,
    products.category,
    products.price,
    order_items.quantity
FROM order_items
JOIN products ON order_items.product_id = products.product_id;

-- 17. Show order_id, customer_name, product_name, quantity, price, and total_amount
SELECT 
    orders.order_id,
    customers.customer_name,
    products.product_name,
    order_items.quantity,
    products.price,
    (order_items.quantity * products.price) AS total_amount
FROM orders
JOIN customers ON orders.customer_id = customers.customer_id
JOIN order_items ON orders.order_id = order_items.order_id
JOIN products ON order_items.product_id = products.product_id;

-- 18. Show only completed orders with their customer and product details
SELECT 
    orders.order_id,
    customers.customer_name,
    customers.city,
    products.product_name,
    products.category,
    products.price,
    order_items.quantity,
    orders.order_date,
    orders.status
FROM orders
JOIN customers ON orders.customer_id = customers.customer_id
JOIN order_items ON orders.order_id = order_items.order_id
JOIN products ON order_items.product_id = products.product_id
WHERE orders.status = 'completed';


-- ============================================================================
-- Level 3 - Multi-table JOINs
-- ============================================================================

-- 19, 20, 21. Multi-table JOIN with sorting by order_id and product_name
SELECT 
    customers.customer_name,
    customers.city,
    orders.order_id,
    products.product_name,
    products.category,
    order_items.quantity,
    products.price,
    (order_items.quantity * products.price) AS total_amount
FROM orders
JOIN customers ON orders.customer_id = customers.customer_id
JOIN order_items ON orders.order_id = order_items.order_id
JOIN products ON order_items.product_id = products.product_id
ORDER BY orders.order_id ASC, products.product_name ASC;

-- 22. Filter joined result to show only completed orders
SELECT 
    customers.customer_name,
    customers.city,
    orders.order_id,
    products.product_name,
    products.category,
    order_items.quantity,
    products.price,
    (order_items.quantity * products.price) AS total_amount
FROM orders
JOIN customers ON orders.customer_id = customers.customer_id
JOIN order_items ON orders.order_id = order_items.order_id
JOIN products ON order_items.product_id = products.product_id
WHERE orders.status = 'completed'
ORDER BY orders.order_id ASC, products.product_name ASC;


-- ============================================================================
-- Level 4 - Business Reports with Relationships
-- ============================================================================

-- 23. Calculate completed revenue by city
SELECT 
    customers.city,
    SUM(order_items.quantity * products.price) AS total_revenue
FROM orders
JOIN customers ON orders.customer_id = customers.customer_id
JOIN order_items ON orders.order_id = order_items.order_id
JOIN products ON order_items.product_id = products.product_id
WHERE orders.status = 'completed'
GROUP BY customers.city
ORDER BY total_revenue DESC;

-- 24. Calculate completed revenue by product category
SELECT 
    products.category,
    SUM(order_items.quantity * products.price) AS total_revenue
FROM orders
JOIN order_items ON orders.order_id = order_items.order_id
JOIN products ON order_items.product_id = products.product_id
WHERE orders.status = 'completed'
GROUP BY products.category
ORDER BY total_revenue DESC;

-- 25. Show top 5 customers by completed revenue
SELECT 
    customers.customer_id,
    customers.customer_name,
    SUM(order_items.quantity * products.price) AS total_spent
FROM orders
JOIN customers ON orders.customer_id = customers.customer_id
JOIN order_items ON orders.order_id = order_items.order_id
JOIN products ON order_items.product_id = products.product_id
WHERE orders.status = 'completed'
GROUP BY customers.customer_id, customers.customer_name
ORDER BY total_spent DESC
LIMIT 5;

-- 26. Show top 5 products by completed revenue
SELECT 
    products.product_id,
    products.product_name,
    SUM(order_items.quantity * products.price) AS total_revenue
FROM orders
JOIN order_items ON orders.order_id = order_items.order_id
JOIN products ON order_items.product_id = products.product_id
WHERE orders.status = 'completed'
GROUP BY products.product_id, products.product_name
ORDER BY total_revenue DESC
LIMIT 5;

-- 27. Count how many orders each customer has
SELECT 
    customers.customer_id,
    customers.customer_name,
    COUNT(orders.order_id) AS total_orders
FROM customers
LEFT JOIN orders ON customers.customer_id = orders.customer_id
GROUP BY customers.customer_id, customers.customer_name
ORDER BY total_orders DESC;

-- 28. Count how many items each order has
SELECT 
    orders.order_id,
    SUM(order_items.quantity) AS total_items_count
FROM orders
JOIN order_items ON orders.order_id = order_items.order_id
GROUP BY orders.order_id
ORDER BY orders.order_id ASC;

-- 29. Find customers who have more than one order
SELECT 
    customers.customer_id,
    customers.customer_name,
    COUNT(orders.order_id) AS order_count
FROM customers
JOIN orders ON customers.customer_id = orders.customer_id
GROUP BY customers.customer_id, customers.customer_name
HAVING COUNT(orders.order_id) > 1;

-- 30. Find products that were sold more than once
SELECT 
    products.product_id,
    products.product_name,
    SUM(order_items.quantity) AS total_quantity_sold
FROM products
JOIN order_items ON products.product_id = order_items.product_id
GROUP BY products.product_id, products.product_name
HAVING SUM(order_items.quantity) > 1;


-- ============================================================================
-- Level 5 - LEFT JOIN Thinking
-- ============================================================================

-- 31. Show all customers and their orders (Include customers even if they have no orders)
SELECT 
    customers.customer_id,
    customers.customer_name,
    orders.order_id,
    orders.order_date,
    orders.status
FROM customers
LEFT JOIN orders ON customers.customer_id = orders.customer_id;

-- 32. Show all products and times sold (Include products that were never sold)
SELECT 
    products.product_id,
    products.product_name,
    COUNT(order_items.order_item_id) AS times_ordered
FROM products
LEFT JOIN order_items ON products.product_id = order_items.product_id
GROUP BY products.product_id, products.product_name;