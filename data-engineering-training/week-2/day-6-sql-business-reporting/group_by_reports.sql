-- Fix for task: Count orders by order_date sorted from highest to lowest
SELECT 
    order_date,
    COUNT(*) AS order_date_count
FROM orders
GROUP BY order_date
ORDER BY order_date_count DESC;