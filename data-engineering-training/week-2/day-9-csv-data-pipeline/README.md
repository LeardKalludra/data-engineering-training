import csv

def load_csv(file_path):
    file = open(file_path, "r", encoding="utf-8")
    reader = csv.DictReader(file)
    data = []
    for row in reader:
        clean_row = {}
        for key, value in row.items():
            clean_key = key.strip() if key else ""
            clean_value = value.strip() if value else ""
            clean_row[clean_key] = clean_value
        data.append(clean_row)
    file.close()
    return data

def write_csv(file_path, rows, fieldnames):
    with open(file_path, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow(row)
    print(f"Written {len(rows)} records to {file_path}.")

def normalize_status(status):
    if not status:
        return "unknown"
    status = status.lower().strip()
    if status in ["completed", "complete", "done"]:
        return "completed"
    elif status in ["cancelled", "canceled"]:
        return "cancelled"
    elif status == "pending":
        return "pending"
    return "unknown"

def normalize_city(city):
    if not city:
        return "Unknown"
    city = city.lower().strip()
    return city.capitalize()

def normalize_channel(channel):
    if not channel:
        return "unknown"
    channel = channel.lower().strip()
    if channel in ["online", "web"]:
        return "online"
    elif channel == "store":
        return "store"
    return "unknown"

def is_positive_integer(value):
    if not value:
        return False
    try:
        number = int(value)
        return number > 0
    except ValueError:
        return False

def build_lookup_table(rows, key_field):
    lookup_table = {}
    for row in rows:
        key = row.get(key_field)
        if key:
            lookup_table[key] = row
    return lookup_table

def validate_order(order, customers_lookup, products_lookup, duplicate_ids):
    reasons = []
    order_id = order.get("order_id")
    if not order_id:
        reasons.append("missing_order_id")
    elif order_id in duplicate_ids:
        reasons.append("duplicate_order_id")

    cust_id = order.get("customer_id")
    if not cust_id:
        reasons.append("missing_customer_id")
    elif cust_id not in customers_lookup:
        reasons.append("invalid_customer_id")

    prod_id = order.get("product_id")
    if not prod_id:
        reasons.append("missing_product_id")
    elif prod_id not in products_lookup:
        reasons.append("invalid_product_id")

    if not order.get("order_date"):
        reasons.append("missing_order_date")

    qty = order.get("quantity")
    if not qty:
        reasons.append("missing_quantity")
    elif not is_positive_integer(qty):
        try:
            if int(qty) <= 0:
                reasons.append("negative_quantity")
            else:
                reasons.append("invalid_quantity")
        except ValueError:
            reasons.append("invalid_quantity")

    normalized_status = normalize_status(order.get("status", ""))
    if not order.get("status"):
        reasons.append("missing_status")
    elif normalized_status not in ["completed", "pending", "cancelled"]:
        reasons.append("invalid_status")

    normalized_channel = normalize_channel(order.get("channel", ""))
    if not order.get("channel"):
        reasons.append("missing_channel")
    elif normalized_channel not in ["online", "store", "unknown"]:
        reasons.append("invalid_channel")

    is_valid = len(reasons) == 0
    return is_valid, ", ".join(reasons)

def enrich_order(order, customers_lookup, products_lookup):
    cust_id = order.get("customer_id")
    prod_id = order.get("product_id")
    customer = customers_lookup.get(cust_id, {})
    product = products_lookup.get(prod_id, {})
    enriched_order = order.copy()
    enriched_order["customer_name"] = customer.get("customer_name") or customer.get("name") or "Unknown"
    enriched_order["city"] = customer.get("city") or "Unknown"
    enriched_order["product_name"] = product.get("product_name") or product.get("name") or "Unknown"
    enriched_order["category"] = product.get("category") or "Unknown"
    enriched_order["price"] = product.get("price") or "0.0"
    return enriched_order

def calculate_total_amount(order):
    try:
        quantity = int(order.get("quantity", 0))
        price = float(order.get("price", 0.0))
        return quantity * price
    except ValueError:
        return 0.0

def count_by_field(rows, field_name):
    counts = {}
    for row in rows:
        val = row.get(field_name, "unknown")
        counts[val] = counts.get(val, 0) + 1
    return counts

def sum_by_field(rows, group_field, amount_field):
    sums = {}
    for row in rows:
        group_val = row.get(group_field, "unknown")
        try:
            amount_val = float(row.get(amount_field, 0.0))
        except ValueError:
            amount_val = 0.0
        sums[group_val] = sums.get(group_val, 0.0) + amount_val
    return sums

def get_completed_orders(rows):
    completed = []
    for row in rows:
        if row.get("status") == "completed":
            completed.append(row)
    return completed

def get_top_n_by_field(rows, field_name, n):
    sorted_rows = sorted(rows, key=lambda x: float(x.get(field_name, 0.0)), reverse=True)
    return sorted_rows[:n]

def create_data_quality_report(raw_orders, clean_orders, invalid_orders):
    invalid_reasons = {}
    for order in invalid_orders:
        reasons = order.get("reason", "")
        if reasons:
            for reason in reasons.split(", "):
                invalid_reasons[reason] = invalid_reasons.get(reason, 0) + 1

    status_counts = {}
    for order in clean_orders:
        status = order.get("status", "unknown")
        status_counts[status] = status_counts.get(status, 0) + 1

    channel_counts = {}
    for order in clean_orders:
        channel = order.get("channel", "unknown")
        channel_counts[channel] = channel_counts.get(channel, 0) + 1

    city_counts = {}
    for order in clean_orders:
        city = order.get("city", "Unknown")
        city_counts[city] = city_counts.get(city, 0) + 1

    status_str = ", ".join([f"{k}: {v}" for k, v in status_counts.items()])
    channel_str = ", ".join([f"{k}: {v}" for k, v in channel_counts.items()])
    city_str = ", ".join([f"{k}: {v}" for k, v in city_counts.items()])
    reasons_str = ", ".join([f"{k}: {v}" for k, v in invalid_reasons.items()]) if invalid_reasons else "None"

    main_problems = []
    if invalid_reasons:
        sorted_reasons = sorted(invalid_reasons.items(), key=lambda x: x[1], reverse=True)
        main_problems = [f"High occurrence of {reason} ({count} cases)" for reason, count in sorted_reasons[:2]]
    else:
        main_problems = ["No major data quality issues found."]
    main_problems_str = "; ".join(main_problems)

    report_content = f"""Data Quality Report - Day 9
Total raw orders: {len(raw_orders)}
Valid orders: {len(clean_orders)}
Invalid orders: {len(invalid_orders)}
Invalid records by reason: {reasons_str}
Status values after cleaning: {status_str}
Channel values after cleaning: {channel_str}
City values after cleaning: {city_str}
Bronze input files checked: orders_raw.csv, customers_raw.csv, products_raw.csv
Silver output files created: orders_clean.csv, invalid_orders.csv
Main data quality problems found: {main_problems_str}
"""

    with open("output/data_quality_report.txt", "w", encoding="utf-8") as file:
        file.write(report_content)
    print("Written data quality report to output/data_quality_report.txt.")

def create_business_summary(clean_orders):
    completed_orders = get_completed_orders(clean_orders)
    total_completed_revenue = sum(float(row.get("total_amount", 0.0)) for row in completed_orders)
    
    orders_by_status = count_by_field(clean_orders, "status")
    orders_by_city = count_by_field(clean_orders, "city")
    
    revenue_by_category = sum_by_field(completed_orders, "category", "total_amount")
    revenue_by_channel = sum_by_field(completed_orders, "channel", "total_amount")
    
    customer_revenue = sum_by_field(completed_orders, "customer_name", "total_amount")
    top_customers_list = [{"customer_name": k, "revenue": v} for k, v in customer_revenue.items()]
    top_3_customers = get_top_n_by_field(top_customers_list, "revenue", 3)
    
    product_revenue = sum_by_field(completed_orders, "product_name", "total_amount")
    top_products_list = [{"product_name": k, "revenue": v} for k, v in product_revenue.items()]
    top_3_products = get_top_n_by_field(top_products_list, "revenue", 3)
    
    top_order = get_top_n_by_field(completed_orders, "total_amount", 1)
    if top_order:
        most_val_order = f"Order {top_order[0].get('order_id')} by {top_order[0].get('customer_name')} (${float(top_order[0].get('total_amount')):.2f})"
    else:
        most_val_order = "None"
        
    non_revenue_orders = []
    for row in clean_orders:
        if row.get("status") in ["pending", "cancelled"]:
            non_revenue_orders.append(row)
    non_revenue_count = len(non_revenue_orders)
    
    status_str = ", ".join([f"{k}: {v}" for k, v in orders_by_status.items()])
    city_str = ", ".join([f"{k}: {v}" for k, v in orders_by_city.items()])
    
    cat_revenue_str = ", ".join([f"{k}: ${v:.2f}" for k, v in revenue_by_category.items()])
    chan_revenue_str = ", ".join([f"{k}: ${v:.2f}" for k, v in revenue_by_channel.items()])
    
    cust_str = ", ".join([f"{c['customer_name']}: ${c['revenue']:.2f}" for c in top_3_customers])
    prod_str = ", ".join([f"{p['product_name']}: ${p['revenue']:.2f}" for p in top_3_products])
    
    rec_list = []
    for cat, rev in sorted(revenue_by_category.items(), key=lambda x: x[1], reverse=True)[:1]:
        rec_list.append(f"Focus sales efforts on your leading category '{cat}'")
    for chan, rev in sorted(revenue_by_channel.items(), key=lambda x: x[1], reverse=True)[:1]:
        rec_list.append(f"maximize marketing budgets for the '{chan}' channel")
    recommendation = f"Double down on high-performing segments: {', and '.join(rec_list)}."

    report_content = f"""Business Summary - Day 9
Completed revenue: ${total_completed_revenue:.2f}
Orders by status: {status_str}
Orders by city: {city_str}
Revenue by category: {cat_revenue_str}
Revenue by channel: {chan_revenue_str}
Top 3 customers by completed revenue: {cust_str}
Top 3 products by completed revenue: {prod_str}
Most valuable completed order: {most_val_order}
Orders that should not count as revenue: {non_revenue_count}
Business recommendation: {recommendation}
Why this Gold output can be trusted: This report is dynamically compiled from clean and verified relationships mapped directly against customers and products master files. All non-completed statuses (pending/cancelled) have been isolated from direct revenue calculations.
"""

    with open("output/business_summary.txt", "w", encoding="utf-8") as file:
        file.write(report_content)
    print("Written business summary report to output/business_summary.txt.")

def detect_duplicates(orders):
    seen = set()
    duplicates = set()
    for order in orders:
        order_id = order.get("order_id")
        if order_id:
            if order_id in seen:
                duplicates.add(order_id)
            seen.add(order_id)
    return duplicates

def generate_bonus_files(clean_orders):
    completed_orders = get_completed_orders(clean_orders)
    
    clean_fields = [
        "order_id", "customer_id", "customer_name", "city", 
        "product_id", "product_name", "category", "quantity", 
        "price", "total_amount", "status", "channel", "order_date"
    ]
    write_csv("output/completed_orders.csv", completed_orders, clean_fields)
    
    city_revenue = sum_by_field(completed_orders, "city", "total_amount")
    sorted_city_revenue = sorted(city_revenue.items(), key=lambda x: x[1], reverse=True)
    with open("output/revenue_by_city.txt", "w", encoding="utf-8") as f:
        for city, rev in sorted_city_revenue:
            f.write(f"{city}: ${rev:.2f}\n")
            
    cat_revenue = sum_by_field(completed_orders, "category", "total_amount")
    sorted_cat_revenue = sorted(cat_revenue.items(), key=lambda x: x[1], reverse=True)
    with open("output/revenue_by_category.txt", "w", encoding="utf-8") as f:
        for cat, rev in sorted_cat_revenue:
            f.write(f"{cat}: ${rev:.2f}\n")
            
    customer_revenue = sum_by_field(completed_orders, "customer_name", "total_amount")
    sorted_customers = sorted(customer_revenue.items(), key=lambda x: x[1], reverse=True)
    with open("output/top_customers.txt", "w", encoding="utf-8") as f:
        for cust, rev in sorted_customers:
            f.write(f"{cust}: ${rev:.2f}\n")
            
    product_revenue = sum_by_field(completed_orders, "product_name", "total_amount")
    sorted_products = sorted(product_revenue.items(), key=lambda x: x[1], reverse=True)
    with open("output/top_products.txt", "w", encoding="utf-8") as f:
        for prod, rev in sorted_products:
            f.write(f"{prod}: ${rev:.2f}\n")

def write_cleaning_log():
    log_content = """Cleaning Rules Applied:
1. whitespace_trimming: Every column header and text cell value is stripped of surrounding spaces during loading.
2. customer_city_normalization: All cities are lowercased, stripped, and capitalized (e.g. 'new york' -> 'New york'). Empty values default to 'Unknown'.
3. order_status_standardization: Maps status strings to 'completed' (from 'completed', 'complete', 'done'), 'cancelled' (from 'cancelled', 'canceled'), 'pending', or fallback 'unknown'.
4. sales_channel_standardization: Converts channel values to lowercase, matching variations like 'web' or 'online' to 'online', 'store' to 'store', and others to 'unknown'.
5. duplicates_removal: Identified order_id collisions are flagged as 'duplicate_order_id' and quarantined to invalid_orders.csv.
"""
    with open("output/cleaning_log.txt", "w", encoding="utf-8") as f:
        f.write(log_content)
    print("Written cleaning log to output/cleaning_log.txt.")

def write_pipeline_steps():
    steps_content = """# Pipeline Steps Mapping

- **Source**: `data/orders_raw.csv`, `data/customers_raw.csv`, `data/products_raw.csv`
- **Ingestion**: Raw files loaded via python's native `csv.DictReader` while stripping whitespace characters.
- **Bronze**: Data parsed as in-memory state objects matching raw configurations.
- **Cleaning**: Execution of status mapping, city capitalizing, channel alignment, and duplicate id identification.
- **Silver**: Output generation mapping valid transactions to `output/orders_clean.csv` and error-associated transactions to `output/invalid_orders.csv`.
- **Transformation**: Calculate total transaction metrics, order category sums, city sums, and customer ranking structures.
- **Gold**: Generates complete metrics in `output/business_summary.txt`, `output/data_quality_report.txt`, and isolated datasets like `output/completed_orders.csv`.
- **Business Output**: Delivers final, trusted, sorted operational reporting across markets, product lines, and consumers.
"""
    with open("pipeline_steps.md", "w", encoding="utf-8") as f:
        f.write(steps_content)
    print("Written pipeline steps mapping to pipeline_steps.md.")

def run_tests():
    print("\n--- Running Tests ---")
    assert normalize_status("Complete") == "completed", "Test Failed: Status 'Complete'"
    assert normalize_status("done") == "completed", "Test Failed: Status 'done'"
    assert normalize_status("canceled") == "cancelled", "Test Failed: Status 'canceled'"
    assert normalize_city("  pristina ") == "Pristina", "Test Failed: City Capitalization"
    assert normalize_channel("WEB") == "online", "Test Failed: Channel WEB"
    assert is_positive_integer("5") is True, "Test Failed: Positive Integer"
    assert is_positive_integer("-1") is False, "Test Failed: Negative Value Check"
    print("All tests passed successfully!")

def main():
    run_tests()

    orders_data = load_csv("data/orders_raw.csv")
    customers_data = load_csv("data/customers_raw.csv")
    products_data = load_csv("data/products_raw.csv")

    for customer in customers_data:
        customer["city"] = normalize_city(customer.get("city", ""))

    customers_lookup = build_lookup_table(customers_data, "customer_id")
    products_lookup = build_lookup_table(products_data, "product_id")
    
    duplicate_order_ids = detect_duplicates(orders_data)

    valid_orders = []
    invalid_orders = []

    for order in orders_data:
        is_valid, error_reason = validate_order(order, customers_lookup, products_lookup, duplicate_order_ids)
        if is_valid:
            order["status"] = normalize_status(order.get("status", ""))
            order["channel"] = normalize_channel(order.get("channel", ""))
            valid_orders.append(order)
        else:
            quarantine_record = order.copy()
            quarantine_record["reason"] = error_reason
            invalid_orders.append(quarantine_record)

    enriched_orders = []
    for order in valid_orders:
        enriched_order = enrich_order(order, customers_lookup, products_lookup)
        total_amount = calculate_total_amount(enriched_order)
        enriched_order["total_amount"] = f"{total_amount:.2f}"
        enriched_orders.append(enriched_order)

    clean_fields = [
        "order_id", "customer_id", "customer_name", "city", 
        "product_id", "product_name", "category", "quantity", 
        "price", "total_amount", "status", "channel", "order_date"
    ]

    invalid_fields = [
        "order_id", "customer_id", "product_id", "quantity", 
        "status", "channel", "order_date", "reason"
    ]

    write_csv("output/orders_clean.csv", enriched_orders, clean_fields)
    write_csv("output/invalid_orders.csv", invalid_orders, invalid_fields)

    create_data_quality_report(
        raw_orders=orders_data, 
        clean_orders=enriched_orders, 
        invalid_orders=invalid_orders
    )

    create_business_summary(enriched_orders)
    
    generate_bonus_files(enriched_orders)
    write_cleaning_log()
    write_pipeline_steps()

if __name__ == "__main__":
    main()