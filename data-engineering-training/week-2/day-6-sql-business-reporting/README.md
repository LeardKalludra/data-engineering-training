# Day 6 - SQL Business Reporting Sprint

### Project Goal
Transforming highly fragmented transactional databases into actionable, clean analytics metrics and readable business reporting.

### Files Included
* `setup.sql` - Environment building and database population script.
* `basic_aggregations.sql` - Core top-line financial metrics queries.
* `group_by_reports.sql` - Categorized and grouped segment reports.
* `join_reports.sql` - Complete relational multi-table data joins.
* `business_report.md` - Contextual analysis and executive summaries.
* `query_explanations.md` - Explanations of core logic choices.
* `daily_report.txt` - Personal sprint logging.

### Execution Instructions
1. Copy the contents of `setup.sql` into SQLiteOnline.com and execute them to build the ecosystem.
2. Run `basic_aggregations.sql`, followed sequentially by `group_by_reports.sql` and `join_reports.sql`.

### Architectural Concepts Learned
* **Basic Aggregation**: Compresses data down into one simple baseline metrics figure.
* **GROUP BY**: Sections rows out dynamically into defined relational buckets.
* **HAVING**: Filters data explicitly *after* those relational groups have been compiled.
* **JOIN**: Bridges primary keys across separate operational silo tables into unified datasets.