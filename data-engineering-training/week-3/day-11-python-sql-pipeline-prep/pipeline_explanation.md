# Part 1: Data Understanding & Architecture Breakdown

## 1. How many raw orders exist?
There are **24 raw order records** in `data/bronze/orders_raw.csv`.

## 2. Which columns are used to join orders with customers and products?
- **Orders to Customers:** Joined on `customer_id`.
- **Orders to Products:** Joined on `product_id`.

## 3. Which values look inconsistent?
- **Status Column:** Mixed casing and variations (`Completed`, ` done`, ` canceled`, ` cancelled`, ` returned`).
- **City Column:** Inconsistent letter casing (e.g., `prishtina`, `VUSHTRRI`, `ferizaj`).
- **Channel Column:** Mixed casing and trailing spaces (`ONLINE `, ` store`, `WEB`).
- **Data Types & Empty Fields:** Non-numeric quantities (`abc`), non-positive numbers (`0`, `-1`), missing values for `quantity`, `order_date`, and `status`.
- **Referential Keys:** Unknown customer IDs (`C013`, `0005`) and unknown product IDs (`P999`) that do not exist in the dimension tables.
- **Duplicate Keys:** Duplicate `order_id` values (e.g., duplicate order ID `1`).

## 4. Which records should not be trusted for revenue?
- **Invalid Records:** Any record failing validation (missing fields, duplicate IDs, bad quantities, non-existent customer/product keys, invalid statuses like `returned`).
- **Non-Completed Orders:** Valid records with `pending` or `cancelled` status. Only valid records with `status = 'completed'` count toward completed revenue.

## 5. Medallion Architecture Mapping
- **Bronze Layer (Raw Data):**
  - `data/bronze/orders_raw.csv`
  - `data/bronze/customers_raw.csv`
  - `data/bronze/products_raw.csv`

- **Silver Layer (Cleaned & Validated Data):**
  - `data/silver/orders_clean.csv` (Valid, enriched orders)
  - `data/silver/invalid_orders.csv` (Rejected orders with `invalid_reason`)

- **Gold Layer (Business Aggregations & Reports):**
  - `data/gold/revenue_by_city.csv`
  - `data/gold/revenue_by_category.csv`
  - `data/gold/top_customers.csv`
  - `data/gold/executive_summary.txt`