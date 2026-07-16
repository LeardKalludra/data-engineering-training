# Day 9 - CSV Data Pipeline: From Raw Data to Clean Reports

## Goal of the Practice
The goal is to build a reliable data pipeline using pure Python to clean, validate, and enrich raw sales data, turning it into trusted business reports.

## Medallion Architecture (Bronze, Silver, Gold)
- **Bronze**: Stores raw, untouched CSV data in memory directly as loaded.
- **Silver**: Holds clean, validated, and enriched records (`orders_clean.csv`) and separates bad records with error logs (`invalid_orders.csv`).
- **Gold**: Contains high-level business insights and quality summaries ready for decision-making.

## Files and Folders Included
- `csv_pipeline.py` - Main script containing the pipeline logic and tests.
- `pipeline_explanation.md` - Documentation detailing the pipeline architecture.
- `pipeline_steps.md` - Map of files to the different pipeline stages.
- `README.md` - Project overview and run instructions.
- `daily_report.txt` - Daily progress and learning summary.
- `data/`
  - `orders_raw.csv` - Raw transaction dataset.
  - `customers_raw.csv` - Raw customer dataset.
  - `products_raw.csv` - Raw product dataset.
- `output/`
  - `orders_clean.csv` - Cleaned, enriched, and validated orders.
  - `invalid_orders.csv` - Quarantined orders failing validation.
  - `completed_orders.csv` - Valid orders with a "completed" status.
  - `data_quality_report.txt` - Operational stats on data cleaning.
  - `business_summary.txt` - Core financial KPIs.
  - `revenue_by_city.txt` - City revenue sorted highest to lowest.
  - `revenue_by_category.txt` - Category revenue sorted highest to lowest.
  - `top_customers.txt` - Customer spending ranking.
  - `top_products.txt` - Product sales ranking.
  - `cleaning_log.txt` - Explanation of applied cleaning rules.

## How to Run the Pipeline
Run the script using python in your terminal:
```bash
python csv_pipeline.py