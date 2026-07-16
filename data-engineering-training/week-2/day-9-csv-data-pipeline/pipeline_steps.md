# Pipeline Steps Mapping

- **Source**: `data/orders_raw.csv`, `data/customers_raw.csv`, `data/products_raw.csv`
- **Ingestion**: Raw files loaded via python's native `csv.DictReader` while stripping whitespace characters.
- **Bronze**: Data parsed as in-memory state objects matching raw configurations.
- **Cleaning**: Execution of status mapping, city capitalizing, channel alignment, and duplicate id identification.
- **Silver**: Output generation mapping valid transactions to `output/orders_clean.csv` and error-associated transactions to `output/invalid_orders.csv`.
- **Transformation**: Calculate total transaction metrics, order category sums, city sums, and customer ranking structures.
- **Gold**: Generates complete metrics in `output/business_summary.txt`, `output/data_quality_report.txt`, and isolated datasets like `output/completed_orders.csv`.
- **Business Output**: Delivers final, trusted, sorted operational reporting across markets, product lines, and consumers.
