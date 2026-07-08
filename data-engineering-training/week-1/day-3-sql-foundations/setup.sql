DROP TABLE IF EXISTS food_orders;

CREATE TABLE food_orders (
    order_id INT,
    customer_name VARCHAR(100),
    item VARCHAR(100),
    quantity INT,
    price DECIMAL(10, 2),
    status VARCHAR(20) 
);

INSERT INTO food_orders (order_id, customer_name, item, quantity, price, status) VALUES
(1, 'Arta', 'Pizza Margherita', 2, 8.50, 'completed'),
(2, 'Blend', 'Burger & Fries', 1, 12.00, 'completed'),
(3, 'Arta', 'Pasta Carbonara', 1, 10.50, 'cancelled'),
(4, 'Dren', 'Chicken Caesar Salad', 1, 9.00, 'completed'),
(5, 'Elira', 'Sushi Roll Combo', 2, 15.00, 'completed'),
(6, 'Dren', 'Steak', 1, 24.99, 'pending'),
(7, 'Fiona', 'Club Sandwich', 3, 7.50, 'completed'),
(8, 'Genc', 'Tacos', 4, 3.00, 'pending'),
(9, 'Blend', 'Ice Cream', 2, 3.50, 'completed'),
(10, 'Arta', 'Espresso', 1, 1.50, 'pending');

DROP TABLE IF EXISTS customers;

CREATE TABLE customers (
    customer_id INT,
    customer_name VARCHAR(100),
    phone_number VARCHAR(20),
    loyalty_points INT
);

INSERT INTO customers (customer_id, customer_name, phone_number, loyalty_points) VALUES
(10, 'Arta', '044-111-222', 150),
(11, 'Blend', '044-333-444', 45),
(12, 'Dren', '044-555-666', 210),
(13, 'Elira', '044-777-888', 95);