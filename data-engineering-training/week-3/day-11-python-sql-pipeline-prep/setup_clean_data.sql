DROP TABLE IF EXISTS clean_orders;

CREATE TABLE clean_orders (
    order_id INTEGER,
    customer_id TEXT,
    customer_name TEXT,
    city TEXT,
    segment TEXT,
    product_id TEXT,
    product_name TEXT,
    category TEXT,
    quantity INTEGER,
    price REAL,
    status TEXT,
    order_date TEXT,
    channel TEXT,
    total_amount REAL
);

INSERT INTO clean_orders VALUES 
(1, 'C001', 'Arta', 'Vushtrri', 'Individual', 'P001', 'Laptop', 'Electronics', 1, 700.0, 'completed', '2026-07-01', 'online', 700.0),
(2, 'C002', 'Blend', 'Prishtina', 'Individual', 'P002', 'Mouse', 'Accessories', 2, 15.0, 'completed', '2026-07-01', 'store', 30.0),
(4, 'C004', 'Elira', 'Vushtrri', 'Individual', 'P004', 'Keyboard', 'Accessories', 1, 40.0, 'cancelled', '2026-07-02', 'store', 40.0),
(5, 'C001', 'Arta', 'Vushtrri', 'Individual', 'P002', 'Mouse', 'Accessories', 3, 15.0, 'completed', '2026-07-03', 'online', 45.0),
(10, 'C009', 'Jon', 'Prishtina', 'Business', 'P008', 'Headphones', 'Accessories', 4, 50.0, 'pending', '2026-07-05', 'store', 200.0),
(11, 'C010', 'Era', 'Vushtrri', 'Individual', 'P001', 'Laptop', 'Electronics', 1, 700.0, 'completed', '2026-07-05', 'online', 700.0),
(12, 'C011', 'Noar', 'Gjilan', 'Individual', 'P009', 'Webcam', 'Electronics', 2, 90.0, 'completed', '2026-07-06', 'bank', 180.0),
(13, 'C012', 'Sara', 'Peja', 'Business', 'P010', 'Notebook', 'Office', 1, 5.0, 'cancelled', '2026-07-06', 'online', 5.0),
(15, 'C004', 'Elira', 'Vushtrri', 'Individual', 'P004', 'Keyboard', 'Accessories', 5, 40.0, 'completed', '2026-07-07', 'store', 200.0),
(19, 'C006', 'Faton', 'Prizren', 'Individual', 'P006', 'Chair', 'Office', 3, 120.0, 'pending', '2026-07-09', 'web', 360.0),
(20, 'C007', 'Gresa', 'Prishtina', 'Business', 'P007', 'USB Cable', 'Accessories', 2, 8.0, 'completed', '2026-07-10', 'online', 16.0),
(21, 'C008', 'Nora', 'Ferizaj', 'Individual', 'P008', 'Headphones', 'Accessories', 1, 50.0, 'completed', '2026-07-10', 'store', 50.0),
(23, 'C010', 'Era', 'Vushtrri', 'Individual', 'P010', 'Notebook', 'Office', 2, 5.0, 'completed', '2026-07-11', 'online', 10.0),
(24, 'C011', 'Noar', 'Gjilan', 'Individual', 'P001', 'Laptop', 'Electronics', 1, 700.0, 'completed', '2026-07-12', 'store', 700.0);

SELECT * FROM clean_orders;