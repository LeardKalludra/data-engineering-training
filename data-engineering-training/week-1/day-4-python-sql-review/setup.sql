CREATE TABLE orders (
    order_id INTEGER PRIMARY KEY,
    customer_name TEXT,
    city TEXT,
    product TEXT,
    category TEXT,
    quantity INTEGER,
    price REAL,
    status TEXT,
    order_date TEXT
);

INSERT INTO orders (order_id, customer_name, city, product, category, quantity, price, status, order_date) VALUES
(1, 'Arta', 'Vushtrri', 'Laptop', 'Electronics', 1, 700, 'completed', '2026-07-01'),
(2, 'Blend', 'Prishtina', 'Mouse', 'Accessories', 2, 15, 'completed', '2026-07-01'),
(3, 'Arta', 'Vushtrri', 'Keyboard', 'Accessories', 1, 40, 'cancelled', '2026-07-02'),
(4, 'Dren', 'Mitrovica', 'Monitor', 'Electronics', 1, 180, 'completed', '2026-07-02'),
(5, 'Elira', 'Prishtina', 'Mouse', 'Accessories', 1, 15, 'completed', '2026-07-03'),
(6, 'Dren', 'Mitrovica', 'Laptop', 'Electronics', 1, 700, 'pending', '2026-07-03'),
(7, 'Nora', 'Vushtrri', 'Headphones', 'Accessories', 1, 50, 'completed', '2026-07-04'),
(8, 'Leart', 'Peja', 'Monitor', 'Electronics', 2, 180, 'completed', '2026-07-04'),
(9, 'Faton', 'Prizren', 'Desk Chair', 'Office', 1, 120, 'completed', '2026-07-05'),
(10, 'Gresa', 'Prishtina', 'USB Cable', 'Accessories', 3, 8, 'completed', '2026-07-05'),
(11, 'Rina', 'Vushtrri', 'Laptop', 'Electronics', 1, 650, 'cancelled', '2026-07-06'),
(12, 'Arben', 'Ferizaj', 'Desk', 'Office', 1, 220, 'pending', '2026-07-06');

SELECT * FROM orders;