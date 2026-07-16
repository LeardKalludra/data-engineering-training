Source Data:
- orders_raw.csv (contains raw customer purchases with quantities, raw statuses, and sales channels)
- customers_raw.csv (contains customer profile information and their corresponding home cities)
- products_raw.csv (contains details on product listings, including specific names, pricing, and category mapping)

Ingestion:
- Plain Python file reads raw CSV data from the local file system.
- Standard custom loops strip unnecessary whitespace from both the headers and the rows during initial loading.

Bronze layer:
- The system stores unchanged raw records directly in memory as dictionaries.
- Files tracked: orders_raw.csv, customers_raw.csv, products_raw.csv.

Cleaning rules:
- Customer cities: Strips leading/trailing spaces and capitalizes the first letter (e.g., "new york" becomes "New york").
- Order statuses: Standardizes strings to lowercase, mapping variations like "complete" or "done" directly to "completed", "canceled" to "cancelled", and empty/unrecognized values to "unknown".
- Channels: Converts string entries to lowercase, resolving values like "web" to "online" and mapping unknown values to "unknown".

Validation rules:
- Format verification: Quantity values must parse correctly as positive integers (values > 0).
- Referential integrity: Any customer_id present in orders must map to a valid record in the customers master file.
- Referential integrity: Any product_id present in orders must map to a valid record in the products master file.
- Mandatory fields: Orders with missing IDs (order, customer, product), missing dates, or invalid/empty statuses and channels are flagged as invalid.
- Error handling: Records failing any validation checks are routed to a quarantined list containing exact failure reasons.

Silver layer:
- orders_clean.csv: Contains only the valid orders with standardized statuses and channels, enriched with customer details (name, city) and product details (name, category, price).
- invalid_orders.csv: Holds all quarantine-validated orders with their original raw data and appended "reason" columns documenting the validation failures.

Transformation rules:
- Total revenue calculation: Computes "total_amount" dynamically for clean orders by multiplying the validated quantity by the product's master list unit price.
- Metric aggregation: Dynamically compiles sums and counts by fields to generate status, city, category, channel, customer, and product metrics.

Gold layer:
- output/data_quality_report.txt: Provides operational insight into raw-to-clean conversion rates, reason-specific validation errors, and post-clean column distributions.
- output/business_summary.txt: Delivers key performance metrics, including total revenue from completed orders, high-value customer segments, top products, and core business recommendations.

Business Output:
- Financial insights: Total completed revenue generated solely from completed orders.
- Operational metrics: Consolidated counts of order states and distributions across geographical markets.
- Performance lists: Top 3 customers and top 3 products sorted by overall completed revenue contributions.
- Strategy guidance: High-level recommendations pointing out your highest-value category and distribution channels.

What makes this data trusted:
- Isolation of revenue: Cancelled and pending order types are dynamically separated from revenue summaries to avoid false inflation.
- Referential checking: Every row in the clean dataset is rigorously validated against actual product prices and customer IDs, keeping corrupted and ghost transactions out of final analytics.