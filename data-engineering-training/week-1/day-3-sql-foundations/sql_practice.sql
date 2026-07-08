DROP TABLE IF EXISTS orders;

CREATE TABLE orders (
    order_id INTEGER,
    customer_id TEXT,
    product TEXT,
    quantity INTEGER,
    price INTEGER,
    status TEXT 
);

INSERT INTO orders (order_id, customer_id, product, quantity, price, status) VALUES
(1, 'Arta', 'Laptop', 1, 700, 'completed'),
(2, 'Blend', 'Mouse', 2, 15, 'completed'),
(3, 'Arta', 'Keyboard', 1, 40, 'cancelled'),
(4, 'Dren', 'Monitor', 1, 180, 'completed'),
(5, 'Elira', 'Mouse', 1, 15, 'completed'),
(6, 'Dren', 'Laptop', 1, 700, 'pending');


SELECT * from orders
WHERE status = 'completed';
-- This query returns all rows where the order status is 'completed'.

SELECT * from orders
WHERE status = 'pending';
-- This query filters the dataset to display only orders currently marked as 'pending'.

SELECT * from orders
WHERE status = 'cancelled';
-- This query retrieves all orders that have been 'cancelled'.

SELECT * from orders
WHERE price > 100;
-- This query filters out items that cost 100 or less, showing only items priced strictly over 100.

SELECT * from orders
WHERE price < 100;
-- This query shows only cheaper items that have a price tag under 100.

SELECT * from orders
WHERE price >= 180;
-- This query pulls all orders where the unit price is 180 or more.

SELECT * from orders
WHERE status <> 'cancelled';
-- This query extracts all orders that are active, meaning the status is not 'cancelled'.

SELECT * from orders
WHERE customer_id == 'Arta';
-- This query selects every order placed specifically by the customer named Arta.

SELECT * from orders
WHERE product = 'Mouse';
-- This query searches for and displays all records where the purchased item is a Mouse.


SELECT * FROM orders
WHERE status = 'completed' AND price > 50;
-- This query finds successful orders that are also higher-value items priced above 50.


SELECT * FROM orders
WHERE status = 'completed' AND product = 'Mouse';
-- This query isolates orders for a Mouse that have been successfully processed and completed.


SELECT * FROM orders
WHERE status = 'completed' or status = 'cancelled';
-- This query fetches orders that are either completely finished or completely called off.

SELECT * from orders
WHERE customer_id = 'Dren' AND status = 'completed';
-- This query displays the finalized, completed orders made specifically by Dren.

SELECT * from orders
WHERE product = 'Laptop' and price = 700;
-- This query looks for Laptop records that are specifically priced at exactly 700.

SELECT * FROM orders
WHERE status = 'completed' or price > 500;
-- This query fetches orders if they are finished OR if they represent a high-ticket item over 500.

SELECT * from orders
WHERE status <> 'cancelled' and price > 100;
-- This query finds all uncancelled orders that have an item price greater than 100.

SELECT * FROM orders
ORDER BY price ASC;
-- This query lists all orders arranged from the lowest price to the highest price.

SELECT * FROM orders
ORDER BY price DESC;
-- This query sorts all order entries starting with the most expensive items down to the cheapest.

SELECT * FROM orders
ORDER BY price DESC
LIMIT 3;
-- This query reveals only the top 3 highest-priced items in the orders table.

SELECT * FROM orders
ORDER BY price ASC
LIMIT 2;
-- This query isolates the 2 lowest-priced item entries in the dataset.

SELECT * FROM orders
WHERE status = 'completed' ORDER BY price DESC;
-- This query filters for finalized orders and ranks them from highest price to lowest price.

SELECT * FROM orders
ORDER BY product ASC;
-- This query organizes all records alphabetically by the name of the product.

SELECT * FROM orders
ORDER BY customer_id ASC;
-- This query sorts the order list alphabetically by the customer names.

SELECT customer_id AS customer_name, product, quantity, price, (quantity * price) AS total_amount
FROM orders;
-- This query updates the customer header and multiplies quantity by price to calculate the total amount spent.

SELECT customer_id AS customer_name, product, quantity, price, (quantity * price) AS total_amount
FROM orders
WHERE status = 'completed';
-- This query builds custom columns and calculates transaction values exclusively for completed orders.

SELECT customer_id AS customer_name, product, quantity, price, (quantity * price) AS total_amount
FROM orders
WHERE status = 'completed'
ORDER BY price DESC;
-- This query generates transaction details for completed orders, ranked from the highest unit price down.

SELECT customer_id AS customer_name, product, quantity, price, (quantity * price) AS total_amount
FROM orders
WHERE status = 'cancelled' or status = 'pending';
-- This query reviews calculated order costs exclusively for non-finalized (cancelled or pending) orders.


SELECT customer_id AS customer, product AS item, (quantity * price) AS total_amount
FROM orders;
-- This query assigns cleaner aliases ('customer', 'item') to the outputs and calculates the total order amounts.

SELECT customer_id AS customer_name, product, quantity, price, (quantity * price) AS total_amount
FROM orders
ORDER BY total_amount DESC
LIMIT 3;
-- This query lists total financial amounts per transaction and returns the 3 most expensive overall order totals.


SELECT customer_id AS customer_name, product, quantity, price, (quantity * price) AS total_amount
FROM orders
WHERE (quantity * price) > 100;
-- This query filters the rows to display only calculated transaction totals that exceed 100.