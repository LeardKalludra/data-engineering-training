PRAGMA foreign_keys = ON;

-- Foreign key test 1: Insert order with non-existent customer_id
INSERT INTO orders (customer_id, order_date, status, channel) 
VALUES (999, '2026-07-21', 'completed', 'Online');

-- Foreign key test 2: Insert order_item with non-existent order_id
INSERT INTO order_items (order_id, product_id, quantity) 
VALUES (999, 1, 2);

-- Foreign key test 3: Insert order_item with non-existent product_id
INSERT INTO order_items (order_id, product_id, quantity) 
VALUES (1, 999, 2);

-- CHECK test 1: Insert product with negative price
INSERT INTO products (product_name, category, price) 
VALUES ('Invalid Product', 'Electronics', -10.00);

-- CHECK test 2: Insert order_item with quantity 0
INSERT INTO order_items (order_id, product_id, quantity) 
VALUES (1, 1, 0);

-- Status test: Insert order with status 'done'
INSERT INTO orders (customer_id, order_date, status, channel) 
VALUES (1, '2026-07-21', 'done', 'Online');