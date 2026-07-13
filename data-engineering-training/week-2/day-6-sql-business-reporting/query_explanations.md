# Query Explanations

### Query title: Completed revenue by category
* **File**: `join_reports.sql`
* **Business question**: Which product category generated the most completed revenue?
* **Tables used**: `orders` and `products`
* **Why JOIN is needed**: The orders table contains the structured operational records (`product_id`, `quantity`), but the category metadata classification and the base numerical `price` values live entirely inside the `products` table.
* **Why WHERE is needed**: Only orders containing a status matching 'completed' represent actual cleared capital inflows. Pending and cancelled operations must remain excluded.
* **Why GROUP BY is needed**: We must roll up individual row values into granular group levels to produce exactly one definitive metrics row per category group.
* **What I understood**: Grouping data shifts calculations out of single atomic database listings into macro-level business reporting metrics.