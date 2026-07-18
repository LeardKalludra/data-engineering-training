import csv

def load_csv(file_path):
    file = open(file_path, "r", encoding="utf-8")
    reader = csv.DictReader(file)
    data = []
    for row in reader:
        clean_row = {}
        for key, value in row.items():
            if key is not None:
                clean_key = key.strip()
                clean_value = value.strip()
                clean_row[clean_key] = clean_value
        data.append(clean_row)
    file.close()
    return data

def write_csv(file_path, rows, fieldnames):
    file = open(file_path, "w", newline="", encoding="utf-8")
    writer = csv.DictWriter(file, fieldnames=fieldnames, extrasaction="ignore")
    writer.writeheader()
    for row in rows:
        writer.writerow(row)
    file.close()

def ensure_output_folders():
    pass

def normalize_status(value):
    if not value:
        return "unknown"
    val = value.lower().strip()
    if val == "completed" or val == "complete" or val == "done":
        return "completed"
    elif val == "cancelled" or val == "canceled":
        return "cancelled"
    elif val == "pending":
        return "pending"
    return "unknown"

def normalize_city(value):
    if not value:
        return "Unknown"
    val = value.lower().strip().replace(".", "")
    if val == "prishtina":
        return "Prishtina"
    elif val == "vushtrri":
        return "Vushtrri"
    return val.title()

def normalize_channel(value):
    if not value:
        return "unknown"
    val = value.lower().strip()
    if val == "online" or val == "web" or val == "mobile":
        return "online"
    elif val == "store":
        return "store"
    return "unknown"

def is_positive_number(value):
    if not value:
        return False
    try:
        val = float(value)
        return val > 0
    except ValueError:
        return False

def is_positive_integer(value):
    if not value:
        return False
    try:
        val = int(value)
        return val > 0
    except ValueError:
        return False

def build_lookup(rows, key_field):
    lookup_table = {}
    for row in rows:
        key = row.get(key_field)
        if key:
            lookup_table[key] = row
    return lookup_table

def clean_customers(raw_customers):
    cleaned_list = []
    for cust in raw_customers:
        cust_id = cust.get("customer_id", "").strip()
        name = cust.get("customer_name", "").strip()
        city_raw = cust.get("city", "").strip()
        
        cleaned_cust = {
            "customer_id": cust_id,
            "customer_name": name,
            "city": normalize_city(city_raw)
        }
        cleaned_list.append(cleaned_cust)
    return cleaned_list

def clean_products(raw_products):
    cleaned_list = []
    for prod in raw_products:
        prod_id = prod.get("product_id", "").strip()
        name = prod.get("product_name", "").strip()
        category = prod.get("category", "").strip()
        price = prod.get("price", "").strip()
        
        if not is_positive_number(price):
            continue
            
        if not category:
            clean_category = "Unknown"
        else:
            clean_category = category
        
        cleaned_prod = {
            "product_id": prod_id,
            "product_name": name,
            "category": clean_category,
            "price": price
        }
        cleaned_list.append(cleaned_prod)
    return cleaned_list

def validate_order(order, customers_lookup, products_lookup, duplicate_order_ids):
    reasons = []
    order_id = order.get("order_id", "").strip()
    cust_id = order.get("customer_id", "").strip()
    prod_id = order.get("product_id", "").strip()
    quantity_str = order.get("quantity", "").strip()
    order_date = order.get("order_date", "").strip()

    if not order_id:
        reasons.append("missing_order_id")
    elif order_id in duplicate_order_ids:
        reasons.append("duplicate_order_id")

    if not cust_id:
        reasons.append("missing_customer_id")
    elif cust_id not in customers_lookup:
        reasons.append("invalid_customer_id")

    if not prod_id:
        reasons.append("missing_product_id")
    elif prod_id not in products_lookup:
        reasons.append("invalid_product_id")

    if not quantity_str:
        reasons.append("missing_quantity")
    elif not is_positive_integer(quantity_str):
        reasons.append("invalid_quantity")

    if not order_date:
        reasons.append("missing_order_date")

    is_valid = (len(reasons) == 0)
    return is_valid, ", ".join(reasons)

def enrich_order(order, customers_lookup, products_lookup):
    cust_id = order.get("customer_id", "").strip()
    prod_id = order.get("product_id", "").strip()
    
    customer = customers_lookup.get(cust_id)
    product = products_lookup.get(prod_id)
    
    enriched = {
        "order_id": order.get("order_id", "").strip(),
        "customer_id": cust_id,
        "customer_name": customer.get("customer_name", "Unknown"),
        "city": customer.get("city", "Unknown"),
        "product_id": prod_id,
        "product_name": product.get("product_name", "Unknown"),
        "category": product.get("category", "Unknown"),
        "quantity": order.get("quantity", "").strip(),
        "price": product.get("price", "0.0"),
        "order_date": order.get("order_date", "").strip()
    }
    
    qty = int(order.get("quantity", 0))
    price_val = float(product.get("price", 0.0))
    enriched["total_amount"] = f"{(qty * price_val):.2f}"
    
    enriched["status"] = normalize_status(order.get("status", ""))
    enriched["channel"] = normalize_channel(order.get("channel", ""))
    
    return enriched

def create_silver_orders(raw_orders, customers_lookup, products_lookup):
    orders_clean = []
    invalid_orders = []
    
    seen_ids = set()
    duplicate_ids = set()
    for order in raw_orders:
        order_id = order.get("order_id", "").strip()
        if order_id:
            if order_id in seen_ids:
                duplicate_ids.add(order_id)
            seen_ids.add(order_id)

    for order in raw_orders:
        is_valid, reason = validate_order(order, customers_lookup, products_lookup, duplicate_ids)
        if is_valid:
            enriched = enrich_order(order, customers_lookup, products_lookup)
            orders_clean.append(enriched)
        else:
            invalid_record = order.copy()
            invalid_record["reason"] = reason
            invalid_orders.append(invalid_record)
            
    return orders_clean, invalid_orders

def count_by_field(rows, field_name):
    counts = {}
    for row in rows:
        val = row.get(field_name, "")
        if val not in counts:
            counts[val] = 0
        counts[val] += 1
    return counts

def sum_by_group(rows, group_field, amount_field):
    sums = {}
    for row in rows:
        group = row.get(group_field, "")
        amount = float(row.get(amount_field, 0.0))
        if group not in sums:
            sums[group] = 0.0
        sums[group] += amount
    return sums

def create_revenue_by_category(clean_orders):
    category_metrics = {}
    for order in clean_orders:
        if order["status"] == "completed":
            cat = order["category"]
            rev = float(order["total_amount"])
            if cat not in category_metrics:
                category_metrics[cat] = {"category": cat, "completed_revenue": 0.0, "total_completed_orders": 0}
            category_metrics[cat]["completed_revenue"] += rev
            category_metrics[cat]["total_completed_orders"] += 1
            
    rows = list(category_metrics.values())
    for r in rows:
        r["completed_revenue"] = float(f"{r['completed_revenue']:.2f}")
    
    rows.sort(key=lambda x: x["completed_revenue"], reverse=True)
    
    for r in rows:
        r["completed_revenue"] = f"{r['completed_revenue']:.2f}"
    return rows

def create_revenue_by_city(clean_orders):
    city_metrics = {}
    for order in clean_orders:
        if order["status"] == "completed":
            city = order["city"]
            rev = float(order["total_amount"])
            if city not in city_metrics:
                city_metrics[city] = {"city": city, "completed_revenue": 0.0, "total_completed_orders": 0}
            city_metrics[city]["completed_revenue"] += rev
            city_metrics[city]["total_completed_orders"] += 1
            
    rows = list(city_metrics.values())
    for r in rows:
        r["completed_revenue"] = float(f"{r['completed_revenue']:.2f}")
        
    rows.sort(key=lambda x: x["completed_revenue"], reverse=True)
    
    for r in rows:
        r["completed_revenue"] = f"{r['completed_revenue']:.2f}"
    return rows

def create_revenue_by_customer(clean_orders):
    cust_metrics = {}
    for order in clean_orders:
        if order["status"] == "completed":
            name = order["customer_name"]
            city = order["city"]
            rev = float(order["total_amount"])
            if name not in cust_metrics:
                cust_metrics[name] = {"customer_name": name, "city": city, "completed_revenue": 0.0, "total_completed_orders": 0}
            cust_metrics[name]["completed_revenue"] += rev
            cust_metrics[name]["total_completed_orders"] += 1
            
    rows = list(cust_metrics.values())
    for r in rows:
        r["completed_revenue"] = float(f"{r['completed_revenue']:.2f}")
        
    rows.sort(key=lambda x: x["completed_revenue"], reverse=True)
    
    for r in rows:
        r["completed_revenue"] = f"{r['completed_revenue']:.2f}"
    return rows

def create_top_products(clean_orders):
    prod_metrics = {}
    for order in clean_orders:
        if order["status"] == "completed":
            name = order["product_name"]
            cat = order["category"]
            qty = int(order["quantity"])
            rev = float(order["total_amount"])
            if name not in prod_metrics:
                prod_metrics[name] = {"product_name": name, "category": cat, "total_quantity_sold": 0, "completed_revenue": 0.0}
            prod_metrics[name]["total_quantity_sold"] += qty
            prod_metrics[name]["completed_revenue"] += rev
            
    rows = list(prod_metrics.values())
    for r in rows:
        r["completed_revenue"] = float(f"{r['completed_revenue']:.2f}")
        
    rows.sort(key=lambda x: x["completed_revenue"], reverse=True)
    
    for r in rows:
        r["completed_revenue"] = f"{r['completed_revenue']:.2f}"
    return rows

def create_data_quality_report(raw_orders, clean_orders, invalid_orders):
    raw_cust_file = load_csv("data/bronze/customers_raw.csv")
    raw_prod_file = load_csv("data/bronze/products_raw.csv")
    
    total_raw = len(raw_orders)
    total_clean = len(clean_orders)
    total_invalid = len(invalid_orders)
    
    is_matching = "YES" if (total_clean + total_invalid == total_raw) else "NO"
    
    seen_order_ids = set()
    dup_order_count = 0
    missing_dates = 0
    invalid_qtys = 0
    
    for o in raw_orders:
        oid = o.get("order_id", "").strip()
        if oid in seen_order_ids:
            dup_order_count += 1
        if oid:
            seen_order_ids.add(oid)
            
        if not o.get("order_date", "").strip():
            missing_dates += 1
            
        qty = o.get("quantity", "").strip()
        if not qty:
            invalid_qtys += 1
        else:
            try:
                if int(qty) <= 0:
                    invalid_qtys += 1
            except ValueError:
                invalid_qtys += 1

    invalid_statuses = 0
    for o in raw_orders:
        st = o.get("status", "").lower().strip()
        if st not in ["completed", "complete", "done", "cancelled", "canceled", "pending", ""]:
            invalid_statuses += 1

    invalid_prices = 0
    for p in raw_prod_file:
        pr = p.get("price", "").strip()
        try:
            if float(pr) <= 0:
                invalid_prices += 1
        except ValueError:
            invalid_prices += 1

    missing_cities = 0
    for c in raw_cust_file:
        if not c.get("city", "").strip():
            missing_cities += 1

    reason_counts = {}
    for o in invalid_orders:
        reasons = o.get("reason", "").split(", ")
        for r in reasons:
            if r:
                reason_counts[r] = reason_counts.get(r, 0) + 1

    report = "Validation Checks\n"
    report += f"Raw orders count: {total_raw}\n"
    report += f"Silver clean orders count: {total_clean}\n"
    report += f"Invalid orders count: {total_invalid}\n"
    report += f"Raw Silver + Invalid: {is_matching}\n"
    report += f"Customer IDs checked: {len(raw_cust_file)}\n"
    report += f"Product IDs checked: {len(raw_prod_file)}\n"
    report += f"Duplicate order IDs found: {dup_order_count}\n"
    report += f"Missing dates found: {missing_dates}\n"
    report += f"Invalid quantities found: {invalid_qtys}\n"
    report += f"Invalid statuses found: {invalid_statuses}\n"
    report += f"Invalid products found: {reason_counts.get('invalid_product_id', 0)}\n"
    report += f"Invalid customers found: {reason_counts.get('invalid_customer_id', 0)}\n"
    report += f"Invalid product prices found: {invalid_prices}\n"
    report += f"Missing customer cities found: {missing_cities}\n"
    report += "Invalid records by reason:\n"
    
    for reason_name, count in reason_counts.items():
        report += f"{reason_name}: {count}\n"
        
    f = open("data_quality_report.txt", "w", encoding="utf-8")
    f.write(report)
    f.close()

def create_executive_summary(clean_orders, invalid_orders):
    raw_orders = load_csv("data/bronze/orders_raw.csv")
    total_raw = len(raw_orders)
    total_clean = len(clean_orders)
    total_invalid = len(invalid_orders)
    
    statuses = count_by_field(clean_orders, "status")
    completed_count = statuses.get("completed", 0)
    pending_count = statuses.get("pending", 0)
    cancelled_count = statuses.get("cancelled", 0)
    
    total_revenue = 0.0
    for o in clean_orders:
        if o["status"] == "completed":
            total_revenue += float(o["total_amount"])
            
    cat_rev = {}
    city_rev = {}
    cust_rev = {}
    prod_rev = {}
    
    for o in clean_orders:
        if o["status"] == "completed":
            amt = float(o["total_amount"])
            cat_rev[o["category"]] = cat_rev.get(o["category"], 0.0) + amt
            city_rev[o["city"]] = city_rev.get(o["city"], 0.0) + amt
            cust_rev[o["customer_name"]] = cust_rev.get(o["customer_name"], 0.0) + amt
            prod_rev[o["product_name"]] = prod_rev.get(o["product_name"], 0.0) + amt

    top_cat = max(cat_rev, key=cat_rev.get) if cat_rev else "None"
    top_city = max(city_rev, key=city_rev.get) if city_rev else "None"
    top_cust = max(cust_rev, key=cust_rev.get) if cust_rev else "None"
    top_prod = max(prod_rev, key=prod_rev.get) if prod_rev else "None"
    
    reason_counts = {}
    for o in invalid_orders:
        reasons = o.get("reason", "").split(", ")
        for r in reasons:
            if r:
                reason_counts[r] = reason_counts.get(r, 0) + 1
    
    common_reason = max(reason_counts, key=reason_counts.get) if reason_counts else "None"
    
    summary = "Executive Summary\n"
    summary += f"Total raw orders: {total_raw}\n"
    summary += f"Valid silver orders: {total_clean}\n"
    summary += f"Invalid orders: {total_invalid}\n"
    summary += f"Completed orders: {completed_count}\n"
    summary += f"Pending orders: {pending_count}\n"
    summary += f"Cancelled orders: {cancelled_count}\n"
    summary += f"Completed revenue: {total_revenue:.2f}\n"
    summary += f"Top category: {top_cat}\n"
    summary += f"Top city: {top_city}\n"
    summary += f"Top customer: {top_cust}\n"
    summary += f"Top product: {top_prod}\n"
    summary += "Day 10 Pipeline\n"
    summary += f"Most common invalid reason: {common_reason}\n"
    summary += "Business recommendation: Standardize user inputs at collection point to prevent bad quantity formats and missing customer accounts from impacting analytical metrics.\n"
    
    f = open("data/gold/executive_summary.txt", "w", encoding="utf-8")
    f.write(summary)
    f.close()
    
    dash_fields = ["total_raw_orders", "valid_orders", "invalid_orders", "completed_revenue", "top_category"]
    dash_row = {
        "total_raw_orders": total_raw,
        "valid_orders": total_clean,
        "invalid_orders": total_invalid,
        "completed_revenue": f"{total_revenue:.2f}",
        "top_category": top_cat
    }
    write_csv("data/gold/dashboard_data.csv", [dash_row], dash_fields)

def main():
    log_entries = []
    log_entries.append("Step 1: Loaded Bronze files.")
    orders_raw = load_csv("data/bronze/orders_raw.csv")
    customers_raw = load_csv("data/bronze/customers_raw.csv")
    products_raw = load_csv("data/bronze/products_raw.csv")
    
    log_entries.append("Step 2: Cleaned customers.")
    cleaned_cust = clean_customers(customers_raw)
    
    log_entries.append("Step 3: Cleaned products.")
    cleaned_prod = clean_products(products_raw)
    
    customers_lookup = build_lookup(cleaned_cust, "customer_id")
    products_lookup = build_lookup(cleaned_prod, "product_id")
    
    log_entries.append("Step 4: Validated orders.")
    log_entries.append("Step 5: Created Silver clean orders.")
    log_entries.append("Step 6: Created invalid orders file.")
    orders_clean, invalid_orders = create_silver_orders(orders_raw, customers_lookup, products_lookup)
    
    write_csv("data/silver/customers_clean.csv", cleaned_cust, ["customer_id", "customer_name", "city"])
    write_csv("data/silver/products_clean.csv", cleaned_prod, ["product_id", "product_name", "category", "price"])
    
    orders_clean_fields = [
        "order_id", "customer_id", "customer_name", "city", 
        "product_id", "product_name", "category", "quantity", 
        "price", "total_amount", "status", "channel", "order_date"
    ]
    invalid_orders_fields = [
        "order_id", "customer_id", "product_id", "order_date", 
        "quantity", "status", "channel", "reason"
    ]
    
    write_csv("data/silver/orders_clean.csv", orders_clean, orders_clean_fields)
    write_csv("data/silver/invalid_orders.csv", invalid_orders, invalid_orders_fields)
    
    log_entries.append("Step 7: Created Gold revenue reports.")
    cat_sales = create_revenue_by_category(orders_clean)
    city_sales = create_revenue_by_city(orders_clean)
    cust_sales = create_revenue_by_customer(orders_clean)
    prod_sales = create_top_products(orders_clean)
    
    write_csv("data/gold/revenue_by_category.csv", cat_sales, ["category", "completed_revenue", "total_completed_orders"])
    write_csv("data/gold/revenue_by_city.csv", city_sales, ["city", "completed_revenue", "total_completed_orders"])
    write_csv("data/gold/revenue_by_customer.csv", cust_sales, ["customer_name", "city", "completed_revenue", "total_completed_orders"])
    write_csv("data/gold/top_products.csv", prod_sales, ["product_name", "category", "total_quantity_sold", "completed_revenue"])
    
    channel_metrics = {}
    for o in orders_clean:
        if o["status"] == "completed":
            ch = o["channel"]
            rev = float(o["total_amount"])
            if ch not in channel_metrics:
                channel_metrics[ch] = {"channel": ch, "completed_revenue": 0.0, "total_completed_orders": 0}
            channel_metrics[ch]["completed_revenue"] += rev
            channel_metrics[ch]["total_completed_orders"] += 1
    channel_rows = list(channel_metrics.values())
    channel_rows.sort(key=lambda x: x["completed_revenue"], reverse=True)
    for cr in channel_rows:
        cr["completed_revenue"] = f"{cr['completed_revenue']:.2f}"
    write_csv("data/gold/revenue_by_channel.csv", channel_rows, ["channel", "completed_revenue", "total_completed_orders"])

    reason_counts = {}
    for o in invalid_orders:
        reasons = o.get("reason", "").split(", ")
        for r in reasons:
            if r:
                reason_counts[r] = reason_counts.get(r, 0) + 1
    reason_rows = [{"reason": k, "count": v} for k, v in reason_counts.items()]
    write_csv("data/gold/invalid_reasons_summary.csv", reason_rows, ["reason", "count"])

    sold_prod_names = set()
    for o in orders_clean:
        if o["status"] == "completed":
            sold_prod_names.add(o["product_name"])
    unsold_prod_rows = []
    for p in cleaned_prod:
        if p["product_name"] not in sold_prod_names:
            unsold_prod_rows.append({"product_name": p["product_name"], "category": p["category"]})
    write_csv("data/gold/unsold_products.csv", unsold_prod_rows, ["product_name", "category"])

    valid_cust_ids = set()
    for o in orders_clean:
        valid_cust_ids.add(o["customer_id"])
    inactive_cust_rows = []
    for c in cleaned_cust:
        if c["customer_id"] not in valid_cust_ids:
            inactive_cust_rows.append({"customer_id": c["customer_id"], "customer_name": c["customer_name"]})
    write_csv("data/gold/inactive_customers.csv", inactive_cust_rows, ["customer_id", "customer_name"])

    log_entries.append("Step 8: Created executive summary.")
    create_executive_summary(orders_clean, invalid_orders)
    create_data_quality_report(orders_raw, orders_clean, invalid_orders)
    
    log_entries.append("Pipeline completed successfully.")
    
    log_file = open("pipeline_log.txt", "w", encoding="utf-8")
    log_file.write("Pipeline Log Day 10\n" + "\n".join(log_entries) + "\n")
    log_file.close()

if __name__ == "__main__":
    print("Success: Pipeline completed.")
    main()