# Day 11 - Python + SQL Pipeline Preparation

## Project Goal
To build a complete, reproducible data pipeline that ingests raw Bronze datasets, performs automated data validation and cleaning to generate Silver-level trusted data, and creates Gold-level business summaries using both Python and SQL.

## Bronze Data
Raw CSV datasets received:
- `orders_raw.csv`
- `customers_raw.csv`
- `products_raw.csv`

### Problems Identified in Bronze Layer:
- **Missing & Bad Values**: Missing quantities, non-numeric quantities (`abc`), non-positive quantities (`0`, `-1`), missing order dates, and missing status fields.
- **Formatting Inconsistencies**: Mixed case statuses (`Completed`, ` done`, ` canceled`, ` returned`) and inconsistent city casings (`prishtina`, `VUSHTRRI`, `ferizaj`).
- **Referential Integrity Issues**: Unknown customer IDs (`C013`, invalid ID `0005`) and unknown product IDs (`P999`) that do not exist in dimension lookup tables.

## Silver Data
### Validation Rules Applied:
- **Quantity**: Must be an integer greater than 0.
- **Status**: Standardized to `completed`, `pending`, or `cancelled`. Unknown or invalid statuses (e.g., `returned`) fail validation.
- **Dates & Keys**: `order_date` must exist. Both `customer_id` and `product_id` must match records in reference files.
- **Uniqueness**: `order_id` must be unique.

### Invalid Records & Normalization:
- Records failing validation are routed to `data/silver/invalid_orders.csv` with a clear explanation in `invalid_reason`.
- Cities are converted to proper title case (e.g., `Prishtina`, `Vushtrri`).
- Channels are lowercased and standardized.

## Gold Reports
Outputs created:
1. `data/gold/revenue_by_city.csv`: Completed revenue and order count broken down by city.
2. `data/gold/revenue_by_category.csv`: Completed revenue grouped by product category.
3. `data/gold/top_customers.csv`: Top 5 customers ranked by completed revenue.
4. `data/gold/executive_summary.txt`: High-level summary of total valid orders, completed orders, and overall revenue.

*Note: In accordance with business rules, only valid orders with `status = 'completed'` count toward completed revenue.*

## Python vs SQL
- **Python**: Best suited for ingestion, string manipulation, flexible multi-rule validations, structural error logging, and data standardization.
- **SQL**: Best suited for declarative analytical queries, fast aggregations (`GROUP BY`, `SUM`, `COUNT`), ranking, and reporting on clean, trusted tables.

## Business Insights & Bonus Segment Analysis
- **Top City**: Vushtrri drives the highest completed revenue (€1,655.00), heavily supported by high-value product sales (e.g., Laptops).
- **Top Category**: Electronics generated the bulk of the revenue (€2,280.00).
- **Data Quality**: 10 out of 24 raw orders were flagged as invalid due to data entry issues (missing quantities, unmatched IDs, invalid statuses), highlighting the need for stricter validation at the source.
- **Bonus Insight (Customer Segment Performance)**: Individual customers generate significantly higher overall revenue (€2,575.00 across 8 orders) compared to Business customers (€46.00 across 2 orders). However, Business customers present an opportunity for growth through higher order quantities when properly targeted.

## What I Can Explain Live
- How foreign key lookups work using Python dictionaries.
- Why pending and cancelled orders are excluded from completed revenue figures.
- How raw records are isolated into `invalid_orders.csv` without crashing the entire processing pipeline.
- How to convert this standard Python code into a Delta Lake architecture on Databricks.

## What I Would Improve Next
- Add logging instead of print statements for production monitoring.
- Implement automated unit tests for validation functions.
- Transition from standard CSV storage to Delta Lake tables to leverage ACID transactions and time travel.