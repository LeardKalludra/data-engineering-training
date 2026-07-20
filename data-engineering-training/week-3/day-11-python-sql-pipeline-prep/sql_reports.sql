-- Query 1: Show all clean orders
SELECT * FROM clean_orders;

-- Query 2: Total completed revenue
SELECT SUM(total_amount) AS total_completed_revenue
FROM clean_orders
WHERE status = 'completed';

-- Query 3: Count orders by status
SELECT status, COUNT(*) AS order_count
FROM clean_orders
GROUP BY status;

-- Query 4: Count orders by city
SELECT city, COUNT(*) AS order_count
FROM clean_orders
GROUP BY city;

-- Query 5: Completed revenue by city
SELECT city, SUM(total_amount) AS completed_revenue
FROM clean_orders
WHERE status = 'completed'
GROUP BY city
ORDER BY completed_revenue DESC;

-- Query 6: Completed revenue by category
SELECT category, SUM(total_amount) AS completed_revenue
FROM clean_orders
WHERE status = 'completed'
GROUP BY category
ORDER BY completed_revenue DESC;

-- Query 7: Top 5 orders by total_amount
SELECT * FROM clean_orders
ORDER BY total_amount DESC
LIMIT 5;

-- Query 8: Top customers by completed revenue
SELECT customer_id, customer_name, SUM(total_amount) AS completed_revenue
FROM clean_orders
WHERE status = 'completed'
GROUP BY customer_id, customer_name
ORDER BY completed_revenue DESC;

-- Query 9: Count orders by channel
SELECT channel, COUNT(*) AS order_count
FROM clean_orders
GROUP BY channel;

-- Query 10: City with highest completed revenue
SELECT city, SUM(total_amount) AS completed_revenue
FROM clean_orders
WHERE status = 'completed'
GROUP BY city
ORDER BY completed_revenue DESC
LIMIT 1;

----------------------------------------------------------------------
-- BONUS QUESTION: Customer Segment Breakdown & Analysis
----------------------------------------------------------------------
-- Query: Completed revenue and average order value (AOV) by customer segment
SELECT 
    segment,
    COUNT(*) AS total_completed_orders,
    SUM(total_amount) AS segment_completed_revenue,
    ROUND(AVG(total_amount), 2) AS average_order_value
FROM clean_orders
WHERE status = 'completed'
GROUP BY segment
ORDER BY segment_completed_revenue DESC;