-- SHOW ALL ORDERS --
SELECT * FROM orders;

-- Show Completed Orders --
SELECT order_id, customer_name, price, order_date  FROM orders WHERE status = 'completed';

-- Show pending or cancelled orders.--
SELECT order_id, customer_name, status, order_date  FROM orders WHERE status = 'cancelled' OR status = 'pending';

-- Show total_amount as quantity * price. --
SELECT order_id, customer_name, price, quantity,(quantity * price) AS total_amount,order_date 
FROM orders 
WHERE status = 'cancelled' OR status = 'pending';

-- Show completed orders with total_amount. -- 

SELECT order_id,  customer_name,price, quantity,(quantity * price) AS total_amount,order_date 
FROM orders 
WHERE status = 'completed';

-- Calculate Completed Revenue
SELECT SUM(quantity * price) AS total_revenue FROM orders WHERE status = 'completed';

-- Count Orders by Status
SELECT status, COUNT(*) AS order_count FROM orders GROUP BY status;


-- Count Orders by City 
SELECT city, COUNT(*) AS order_count FROM orders GROUP BY city;


-- Count Orders by Category
SELECT category, COUNT(*) AS order_count FROM orders GROUP BY category;


-- Show Top 3 Orders by Total Amount
SELECT order_id,customer_name,quantity,price,(quantity * price) AS total_amount
FROM orders
ORDER BY total_amount DESC
LIMIT 3;

-- Find the Most Valuable Order
SELECT order_id,customer_name,product,quantity,price,(quantity * price) AS total_amount
FROM orders
ORDER BY total_amount DESC
LIMIT 1;