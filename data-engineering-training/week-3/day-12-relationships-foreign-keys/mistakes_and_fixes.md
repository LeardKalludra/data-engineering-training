# Relationship Tests, Errors, and Fixes

## 1. Foreign Key Test 1 (Invalid Customer ID)
* **Attempt:** `INSERT INTO orders (customer_id, order_date, status, channel) VALUES (999, '2026-07-21', 'completed', 'Online');`
* **Error:** `Runtime error: FOREIGN KEY constraint failed (19)`
* **Fix:** Use a valid `customer_id` that exists in `customers` table (e.g., ID 1).

## 2. Foreign Key Test 2 (Invalid Order ID)
* **Attempt:** `INSERT INTO order_items (order_id, product_id, quantity) VALUES (999, 1, 2);`
* **Error:** `Runtime error: FOREIGN KEY constraint failed (19)`
* **Fix:** Use a valid `order_id` from the `orders` table (e.g., ID 1).

## 3. Foreign Key Test 3 (Invalid Product ID)
* **Attempt:** `INSERT INTO order_items (order_id, product_id, quantity) VALUES (1, 999, 2);`
* **Error:** `Runtime error: FOREIGN KEY constraint failed (19)`
* **Fix:** Reference an existing `product_id` (e.g., ID 1).

## 4. CHECK Test 1 (Negative Price)
* **Attempt:** `INSERT INTO products (product_name, category, price) VALUES ('Invalid Product', 'Electronics', -10.00);`
* **Error:** `Runtime error: CHECK constraint failed: price > 0 (19)`
* **Fix:** Ensure `price` is strictly greater than 0 (e.g., 29.99).

## 5. CHECK Test 2 (Zero Quantity)
* **Attempt:** `INSERT INTO order_items (order_id, product_id, quantity) VALUES (1, 1, 0);`
* **Error:** `Runtime error: CHECK constraint failed: quantity > 0 (19)`
* **Fix:** Pass a positive quantity integer (e.g., 1).

## 6. Status Test (Invalid Status Value)
* **Attempt:** `INSERT INTO orders (customer_id, order_date, status, channel) VALUES (1, '2026-07-21', 'done', 'Online');`
* **Error:** `Runtime error: CHECK constraint failed: status IN ('completed', 'pending', 'cancelled') (19)`
* **Fix:** Use one of the allowed statuses: `'completed'`, `'pending'`, or `'cancelled'`.