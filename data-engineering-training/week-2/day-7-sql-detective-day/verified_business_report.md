# Verified Business Report Day 7 SQL Detective Day

## 1. Total order activity
*   **Insight:** The business recorded a total of 14 orders from its customer base during the tracking period.
*   **Verified result:** 14 total orders (10 completed, 2 pending, 2 cancelled).
*   **SQL query used:**
    ```sql
    SELECT COUNT(*) AS total_orders FROM orders;
    ```
*   **Business meaning:** This metric establishes the baseline transactional volume of the shop. While 14 orders show active engagement, a portion of these transactions did not result in realized sales.

## 2. Completed revenue
*   **Insight:** Total realized sales revenue from successfully finalized transactions is $1,639.00.
*   **Verified result:** $1,639.00 completed revenue.
*   **SQL query used:**
    ```sql
    SELECT SUM(quantity * price) AS completed_revenue
    FROM orders
    JOIN products ON orders.product_id = products.product_id
    WHERE status = 'completed';
    ```
*   **Business meaning:** This represents actual, cleared money in the bank. Uncompleted statuses (pending/cancelled) are strictly omitted to prevent over-reporting and cash flow distortion.

## 3. Revenue by product
*   **Insight:** The Laptop is the single highest driver of completed revenue, despite only selling one completed unit.
*   **Verified result:** 
    *   Laptop: $700.00
    *   Monitor: $540.00 (3 units)
    *   Headphones: $150.00 (3 units)
    *   Desk Chair: $120.00 (1 unit)
    *   Mouse: $105.00 (7 units)
    *   USB Cable: $24.00 (3 units)
*   **SQL query used:**
    ```sql
    SELECT product_name, SUM(quantity * price) AS revenue
    FROM orders
    JOIN products ON orders.product_id = products.product_id
    WHERE status = 'completed'
    GROUP BY product_name
    ORDER BY revenue DESC;
    ```
*   **Business meaning:** High-ticket items (Laptops and Monitors) generate 75.6% of the company's revenue, whereas high-volume, low-cost accessories like Mice and USB Cables keep transactional volume high but contribute minimally to the bottom line.

## 4. Revenue by category
*   **Insight:** Electronics is the dominant category, pulling in over four times the revenue of Accessories and Office products combined.
*   **Verified result:**
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
*   **Business meaning:** Marketing efforts and stock capital should heavily prioritize Electronics, as it functions as the primary financial engine for the business.

## 5. Orders by city
*   **Insight:** Prishtina generates the highest raw order count, closely followed by Vushtrri.
*   **Verified result:**
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
*   **Business meaning:** Prishtina and Vushtrri together account for nearly 65% of all ordering activity, indicating these are key regional markets where local logistics or localized ad spend should be optimized.

## 6. Customers with more than one order
*   **Insight:** We have 4 repeat customers who have purchased more than once, indicating healthy initial retention.
*   **Verified result:** 
    *   Arta (Customer 1): 2 orders
    *   Blend (Customer 2): 2 orders
    *   Dren (Customer 3): 2 orders
    *   Elira (Customer 4): 2 orders
*   **SQL query used:**
    ```sql
    SELECT customers.customer_name, COUNT(*) AS order_count
    FROM orders
    JOIN customers ON orders.customer_id = customers.customer_id
    GROUP BY customers.customer_name
    HAVING COUNT(*) > 1;
    ```
*   **Business meaning:** 40% of the total customer base (4 out of 10) are repeat buyers. Designing a simple loyalty or referral program for these high-value users could easily boost customer lifetime value.

## 7. Orders not counted as revenue
*   **Insight:** There are 4 orders currently stalled or cancelled, representing a major pipeline leak of $1,660.00 in unearned revenue—nearly matching our actual earned revenue.
*   **Verified result:** 4 unearned orders (2 cancelled, 2 pending) totaling $1,660.00.
    *   O3 (cancelled): Keyboard ($40.00)
    *   O6 (pending): Laptop ($700.00)
    *   O11 (cancelled): Laptop ($700.00)
    *   O12 (pending): Desk ($220.00)
*   **SQL query used:**
    ```sql
    SELECT orders.order_id, orders.status, products.product_name, (orders.quantity * products.price) AS lost_value
    FROM orders
    JOIN products ON orders.product_id = products.product_id
    WHERE orders.status <> 'completed';
    ```
*   **Business meaning:** High-ticket cancellations and delays are severely hurting performance. A single cancelled Laptop order cost $700, and a pending Laptop order is holding up another $700. Addressing inventory/checkout friction on high-value items is critical.

## 8. Final recommendation
Based on the verified data, my recommendation is:
1.  **Secure the Pending Pipeline:** Reach out to Customer 3 (Dren, pending Laptop) and Customer 9 (Arben, pending Desk) immediately. Securing these two pending orders will instantly add $920 to the business's completed revenue (+56% increase).
2.  **Investigate Laptop Cancellations:** Since two high-value Laptop orders were cancelled (costing $1,400 in lost potential revenue), audit the supply chain or checkout experience to understand why customers are dropping off.
3.  **Prioritize Top-Tier Regions:** Allocate 70% of geographic marketing budgets to Prishtina and Vushtrri, as they represent the dominant customer clusters.