--Show every single row and column inside the customers table
SELECT * FROM customers;

--Show every single row and column inside the products table
SELECT * FROM products;

--Show every single row and column inside the orders table
SELECT * FROM orders;



--Count how many customers we have registered in our system
SELECT COUNT(*) AS total_customers 
FROM customers;

--Count how many unique products we sell in our shop
SELECT COUNT(*) AS total_products 
FROM products;

--Count how many total orders have been placed in our system
SELECT COUNT(*) AS total_orders 
FROM orders;