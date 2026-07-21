PRAGMA foreign_keys = ON;

-- 1. Insert 6 Customers
INSERT INTO customers (customer_name, city, segment) VALUES
('Arta', 'Vushtrri', 'Retail'),
('Blend', 'Prishtina', 'Corporate'),
('Dren', 'Mitrovica', 'Retail'),
('Elira', 'Peja', 'Corporate'),
('Leart', 'Ferizaj', 'Retail'),
('Gresa', 'Gjakova', 'Corporate');

-- 2. Insert 6 Products
INSERT INTO products (product_name, category, price) VALUES
('Laptop', 'Electronics', 999.99),
('Mouse', 'Accessories', 25.50),
('Monitor', 'Electronics', 199.99),
('Keyboard', 'Accessories', 45.00),
('Desk', 'Furniture', 150.00),
('Headphones', 'Electronics', 79.99);

-- 3. Insert 8 Orders (5 completed, 2 pending, 1 cancelled | Customer 1 & 2 have >1 order)
INSERT INTO orders (customer_id, order_date, status, channel) VALUES
(1, '2026-07-01', 'completed', 'Online'),
(1, '2026-07-05', 'completed', 'In-Store'),
(2, '2026-07-10', 'completed', 'Online'),
(2, '2026-07-12', 'pending',   'Online'),
(3, '2026-07-15', 'completed', 'In-Store'),
(4, '2026-07-18', 'completed', 'Online'),
(5, '2026-07-19', 'pending',   'In-Store'),
(6, '2026-07-20', 'cancelled', 'Online');

-- 4. Insert 12 Order Items (Orders 1 & 3 have >1 item | Products 1 & 2 used in multiple orders)
INSERT INTO order_items (order_id, product_id, quantity) VALUES
(1, 1, 1),
(1, 2, 2),
(1, 4, 1),
(2, 3, 1),
(3, 1, 2),
(3, 5, 1),
(4, 2, 1),
(5, 6, 1),
(6, 3, 2),
(7, 4, 1),
(8, 2, 1),
(8, 6, 1);