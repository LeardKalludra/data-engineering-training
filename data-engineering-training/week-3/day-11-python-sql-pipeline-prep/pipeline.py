import csv

BRONZE_ORDERS = "data/bronze/orders_raw.csv"
BRONZE_CUSTOMERS = "data/bronze/customers_raw.csv"
BRONZE_PRODUCTS = "data/bronze/products_raw.csv"

SILVER_CLEAN = "data/silver/orders_clean.csv"
SILVER_INVALID = "data/silver/invalid_orders.csv"

GOLD_CITY = "data/gold/revenue_by_city.csv"
GOLD_CATEGORY = "data/gold/revenue_by_category.csv"
GOLD_CUSTOMERS = "data/gold/top_customers.csv"
GOLD_SUMMARY = "data/gold/executive_summary.txt"


def load_csv(file_path):
    with open(file_path, mode='r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        reader.fieldnames = [name.strip() for name in reader.fieldnames]
        data = []
        for row in reader:
            data.append({k.strip(): (v.strip() if v else "") for k, v in row.items()})
        return data


def write_csv(file_path, fieldnames, data):
    with open(file_path, mode='w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)


def normalize_status(status):
    value = status.strip().lower()
    if value in ["completed", "complete", "done"]:
        return "completed"
    elif value in ["canceled", "cancelled"]:
        return "cancelled"
    elif value == "pending":
        return "pending"
    else:
        return "unknown"


def normalize_city(city):
    return city.strip().title() if city else "Unknown"


def normalize_channel(channel):
    val = channel.lower().strip()
    valid_channels = {'online', 'store', 'web', 'bank'}
    return val if val in valid_channels else ('unknown' if not val else val)


def build_customer_lookup(customers_raw):
    lookup = {}
    for row in customers_raw:
        lookup[row['customer_id']] = {
            'customer_name': row['customer_name'],
            'city': normalize_city(row['city']),
            'segment': row['segment']
        }
    return lookup


def build_product_lookup(products_raw):
    lookup = {}
    for row in products_raw:
        try:
            price = float(row['price'])
        except ValueError:
            price = 0.0
        lookup[row['product_id']] = {
            'product_name': row['product_name'],
            'category': row['category'],
            'price': price
        }
    return lookup


def validate_order(row, customer_lookup, product_lookup, seen_order_ids):
    reasons = []

    order_id = row.get("order_id", "")
    if order_id in seen_order_ids:
        reasons.append("Duplicate order_id")
    else:
        seen_order_ids.add(order_id)

    raw_qty = row.get("quantity", "")
    if not raw_qty:
        reasons.append("Missing quantity")
    else:
        try:
            qty = int(raw_qty)
            if qty <= 0:
                reasons.append("Quantity must be positive")
        except ValueError:
            reasons.append("Quantity is not an integer")

    raw_status = row.get("status", "")
    if not raw_status:
        reasons.append("Missing status")
    else:
        normalized_status = normalize_status(raw_status)
        if normalized_status == "unknown":
            reasons.append(f"Invalid status: {raw_status}")

    if not row.get("order_date", ""):
        reasons.append("Missing order_date")

    customer_id = row.get("customer_id", "")
    if customer_id not in customer_lookup:
        reasons.append(f"Unknown customer_id: {customer_id}")

    product_id = row.get("product_id", "")
    if product_id not in product_lookup:
        reasons.append(f"Unknown product_id: {product_id}")

    return reasons


def process_silver_data(orders_raw, customer_lookup, product_lookup):
    clean_orders = []
    invalid_orders = []
    seen_order_ids = set()

    for row in orders_raw:
        reasons = validate_order(row, customer_lookup, product_lookup, seen_order_ids)
        if reasons:
            invalid_row = dict(row)
            invalid_row["invalid_reason"] = "; ".join(reasons)
            invalid_orders.append(invalid_row)
        else:
            customer_info = customer_lookup[row["customer_id"]]
            product_info = product_lookup[row["product_id"]]
            quantity = int(row["quantity"])
            price = product_info["price"]
            total_amount = round(quantity * price, 2)

            clean_row = {
                "order_id": row["order_id"],
                "customer_id": row["customer_id"],
                "customer_name": customer_info["customer_name"],
                "city": customer_info["city"],
                "segment": customer_info["segment"],
                "product_id": row["product_id"],
                "product_name": product_info["product_name"],
                "category": product_info["category"],
                "quantity": quantity,
                "price": price,
                "status": normalize_status(row["status"]),
                "order_date": row["order_date"],
                "channel": normalize_channel(row.get("channel", "")),
                "total_amount": total_amount
            }
            clean_orders.append(clean_row)

    return clean_orders, invalid_orders


def process_gold_reports(clean_orders):
    completed_orders = [o for o in clean_orders if o["status"] == "completed"]

    revenue_by_city = {}
    city_count = {}
    revenue_by_category = {}
    cat_count = {}
    customer_revenue = {}
    customer_count = {}
    customer_ids = {}

    for o in completed_orders:
        city = o["city"]
        category = o["category"]
        cid = o["customer_id"]
        total_amount = o["total_amount"]

        revenue_by_city[city] = revenue_by_city.get(city, 0.0) + total_amount
        city_count[city] = city_count.get(city, 0) + 1

        revenue_by_category[category] = revenue_by_category.get(category, 0.0) + total_amount
        cat_count[category] = cat_count.get(category, 0) + 1

        customer_revenue[cid] = customer_revenue.get(cid, 0.0) + total_amount
        customer_count[cid] = customer_count.get(cid, 0) + 1
        customer_ids[cid] = o["customer_name"]

    def get_revenue(item):
        return item[1]

    rev_by_city = [
        {
            "city": city,
            "completed_orders": city_count[city],
            "total_revenue": round(revenue, 2)
        }
        for city, revenue in sorted(revenue_by_city.items(), key=get_revenue, reverse=True)
    ]

    rev_by_category = [
        {
            "category": category,
            "completed_orders": cat_count[category],
            "total_revenue": round(revenue, 2)
        }
        for category, revenue in sorted(revenue_by_category.items(), key=get_revenue, reverse=True)
    ]

    top_customers = [
        {
            "customer_id": cid,
            "customer_name": customer_ids[cid],
            "completed_orders": customer_count[cid],
            "total_revenue": round(revenue, 2)
        }
        for cid, revenue in sorted(customer_revenue.items(), key=get_revenue, reverse=True)[:5]
    ]

    total_valid_orders = len(clean_orders)
    completed_count = len(completed_orders)
    total_revenue = round(sum(o["total_amount"] for o in completed_orders), 2)

    exec_summary = (
        f"==================================================\n"
        f"EXECUTIVE BUSINESS SUMMARY\n"
        f"==================================================\n"
        f"Total Valid Orders: {total_valid_orders}\n"
        f"Completed Orders:   {completed_count}\n"
        f"Total Revenue:     €{total_revenue:,.2f}\n"
        f"==================================================\n"
    )

    return rev_by_city, rev_by_category, top_customers, exec_summary


def main():
    print("Starting data processing pipeline...")

    orders_raw = load_csv(BRONZE_ORDERS)
    customers_raw = load_csv(BRONZE_CUSTOMERS)
    products_raw = load_csv(BRONZE_PRODUCTS)

    customer_lookup = build_customer_lookup(customers_raw)
    product_lookup = build_product_lookup(products_raw)

    clean_orders, invalid_orders = process_silver_data(orders_raw, customer_lookup, product_lookup)

    silver_clean_fields = [
        "order_id", "customer_id", "customer_name", "city", "segment",
        "product_id", "product_name", "category", "quantity", "price",
        "status", "order_date", "channel", "total_amount"
    ]

    write_csv(SILVER_CLEAN, silver_clean_fields, clean_orders)

    raw_invalid_fields = list(orders_raw[0].keys() if orders_raw else [])
    invalid_fields = raw_invalid_fields + ["invalid_reason"]
    write_csv(SILVER_INVALID, invalid_fields, invalid_orders)

    print(f"Silver data processing complete. Clean orders: {len(clean_orders)}, Invalid orders: {len(invalid_orders)}")

    rev_by_city, rev_by_category, top_customers, exec_summary = process_gold_reports(clean_orders)

    write_csv(GOLD_CITY, ["city", "completed_orders", "total_revenue"], rev_by_city)
    write_csv(GOLD_CATEGORY, ["category", "completed_orders", "total_revenue"], rev_by_category)
    write_csv(GOLD_CUSTOMERS, ["customer_id", "customer_name", "completed_orders", "total_revenue"], top_customers)

    with open(GOLD_SUMMARY, mode='w', encoding='utf-8') as f:
        f.write(exec_summary)

    print("Gold reports generated successfully.")
    print("Data processing pipeline completed.")


if __name__ == "__main__":
    main()