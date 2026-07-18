# Day 10 Bronze / Silver / Gold Pipeline with Python

## Project goal
The goal of this project is to build a reliable, multi-layer data engineering pipeline using pure Python to transform unstructured, messy raw CSV records into clean, validated, and business-ready analytical assets. The architecture models industry-standard medallion data lake design patterns (Bronze $\rightarrow$ Silver $\rightarrow$ Gold) to demonstrate how data quality engineering underpins reliable corporate reporting.

## Bronze layer
* **Files Stored**: `orders_raw.csv`, `customers_raw.csv`, and `products_raw.csv`.
* **Ingestion Strategy**: Raw assets are ingested as immutable single-source-of-truth tables using native Python streams. No manual edits or adjustments are performed on these files to ensure lineage visibility and reproducible data reprocessing.

## Silver layer
* **Cleaning Rules Applied**: 
  * Trimmed white spaces and removed structural trailing punctuation from string variables.
  * Normalized transaction status parameters into standard types: `completed`, `cancelled`, and `pending`[cite: 2].
  * Standardized purchasing channel attributes into `online` or `store` fields, assigning `unknown` to missing items[cite: 2].
  * Standardized city names to formal title cases (`Prishtina`, `Vushtrri`)[cite: 2].
  * Enforced integrity constraints: Order quantities must be positive integers, product prices must be positive floats, and matching keys must actively exist inside clean dimension lookup indexes[cite: 2].
* **Enrichment Logic**: Extracted valid records into `orders_clean.csv`, appending structural data fields including `customer_name`, `city`, `product_name`, `category`, and `price` while computing `total_amount` ($quantity \times price$)[cite: 2].
* **Error Isolation**: Diverted invalid data entries into `invalid_orders.csv` complete with explicit, concatenated reason flags describing why the constraint check failed[cite: 2].

## Gold layer
* **Assets Generated**: Highly aggregated business reports including regional revenue streams (`revenue_by_city.csv`), inventory groupings (`revenue_by_category.csv`), high-value client tracking (`revenue_by_customer.csv`), and velocity matrices (`top_products.csv`)[cite: 2].
* **Bonus Assets**: Deployed specialized files tracking marketing channels (`revenue_by_channel.csv`), validation error counts (`invalid_reasons_summary.csv`), inactive consumer segments (`inactive_customers.csv`), and unsold warehouse inventory (`unsold_products.csv`).
* **Dashboard Layer**: Compiled a single-row executive KPI collection (`dashboard_data.csv`) optimized for fast BI dashboard visualization ingestion.

## How to run the pipeline
1. Ensure the messy raw source files are placed inside the project path at `data/bronze/`[cite: 2].
2. Execute the self-contained pipeline script from your terminal:
   ```bash
   python pipeline.py