## 1. Total order activity
*   **What we found:** We had a total of 14 orders placed in our system.
*   **The actual number:** 14 orders (10 went through, 2 are stuck, 2 were cancelled).
*   **SQL query used:**
    ```sql
    SELECT COUNT(*) AS total_orders FROM orders;
    ```
*   **What this means:** This is the total number of times a customer clicked "buy". It shows people are using our shop, but not every click turns into real money.

## 2. Completed revenue
*   **What we found:** The actual money we made from finished sales is $1,639.00.
*   **The actual number:** $1,639.00.
*   **SQL query used:**
    ```sql
    SELECT SUM(quantity * price) AS completed_revenue
    FROM orders
    JOIN products ON orders.product_id = products.product_id
    WHERE status = 'completed';
    ```
*   **What this means:** This is the only money we actually have in our bank account. We do not count "pending" or "cancelled" orders here because that money hasn't actually arrived yet.

## 3. Revenue by product
*   **What we found:** Laptops and Monitors make us the most money, even though we don't sell very many of them.
*   **The actual numbers (from highest to lowest):**
    *   Laptop: $700.00 (1 sold)
    *   Monitor: $540.00 (3 sold)
    *   Headphones: $150.00 (3 sold)
    *   Desk Chair: $120.00 (1 sold)
    *   Mouse: $105.00 (7 sold)
    *   USB Cable: $24.00 (3 sold)
*   **SQL query used:**
    ```sql
    SELECT product_name, SUM(quantity * price) AS revenue
    FROM orders
    JOIN products ON orders.product_id = products.product_id
    WHERE status = 'completed'
    GROUP BY product_name
    ORDER BY revenue DESC;
    ```
*   **What this means:** Expensive items (Laptops and Monitors) bring in almost all of our cash. Cheap items like Mice and USB Cables are popular, but they don't help our bank account nearly as much.

## 4. Revenue by category
*   **What we found:** Electronics is our absolute best-selling category.
*   **The actual numbers:**
    *   Electronics: $1,240.00
    *   Accessories: $279.00
    *   Office: $120.00
*   **SQL query used:**
    ```sql
    SELECT category, SUM(quantity * price) AS revenue
    FROM orders
    JOIN products ON orders.product_id = products.product_id
    WHERE status = 'completed'
    GROUP BY category
    ORDER BY revenue DESC;
    ```
*   **What this means:** Electronics makes up almost 75% of our sales. We should focus our shop's setup and ads on Electronics.

## 5. Orders by city
*   **What we found:** Most of our customers live in Prishtina and Vushtrri.
*   **The actual numbers:**
    *   Prishtina: 5 orders
    *   Vushtrri: 4 orders
    *   Mitrovica: 2 orders
    *   Peja: 1 order
    *   Prizren: 1 order
    *   Ferizaj: 1 order
*   **SQL query used:**
    ```sql
    SELECT customers.city, COUNT(*) AS order_count
    FROM orders
    JOIN customers ON orders.customer_id = customers.customer_id
    GROUP BY customers.city
    ORDER BY order_count DESC;
    ```
*   **What this means:** Prishtina and Vushtrri are our main hotspots. If we want to run a local discount or advertisement, we should do it there.

## 6. Customers with more than one order
*   **What we found:** We have 4 loyal, repeat customers who bought things from us more than once.
*   **The actual numbers:**
    *   Arta: 2 orders
    *   Blend: 2 orders
    *   Dren: 2 orders
    *   Elira: 2 orders
*   **SQL query used:**
    ```sql
    SELECT customers.customer_name, COUNT(*) AS order_count
    FROM orders
    JOIN customers ON orders.customer_id = customers.customer_id
    GROUP BY customers.customer_name
    HAVING COUNT(*) > 1;