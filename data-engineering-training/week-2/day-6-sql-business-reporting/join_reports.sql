-- 5. Create completed revenue by category, sorted highest to lowest.
SELECT 
    p.category,
    SUM(o.quantity * p.price) AS completed_revenue
FROM orders o
JOIN products p ON o.product_id = p.product_id
WHERE o.status = 'completed'
GROUP BY p.category
ORDER BY completed_revenue DESC;