from order_data import orders

# --- Part 1 Functions ---
def print_raw_count(records):
    print("Raw records:", len(records))
    
    
def print_first_three_records(records):
    print("\nFIRST THREE RAW RECORDS:")
    for order in records[:3]:
        print(f"Order ID: {order['order_id']}")
        print(f"Customer: {order['customer_name']}")
        print(f"City: {order['city']}")
        print(f"Product: {order['product']}")
        print(f"Category: {order['category']}")
        print(f"Quantity: {order['quantity']}")
        print(f"Price: {order['price']}")
        print(f"Status: {order['status']}")
        print(f"Channel: {order['channel']}")
        print(f"Date: {order['order_date']}")
        print("=" * 20)
        
        
def print_unique_raw_values(records):
    statuses = []
    cities = []
    categories = []
    channels = []

    for order in records:
        if order["status"] not in statuses:
            statuses.append(order["status"])
        if order["city"] not in cities:
            cities.append(order["city"])
        if order["category"] not in categories:
            categories.append(order["category"])
        if order["channel"] not in channels:
            channels.append(order["channel"])

    print("\nUNIQUE RAW VALUES BEFORE CLEANING:")

    print("Raw statuses:")
    for status in sorted(statuses):
        print(f"- {status}")

    print("\nRaw cities:")
    for city in sorted(cities):
        print(f"- {city}")

    print("\nRaw categories:")
    for category in sorted(categories):
        print(f"- {category}")

    print("\nRaw channels:")
    for channel in sorted(channels):
        print(f"- {channel}")


# --- Part 2 Functions ---
def validate_order(order):
    reasons = []
    
    if order["customer_name"].strip() == "":
        reasons.append("Missing customer name")

    if order["quantity"] <= 0:
        reasons.append("Quantity must be greater than 0")

    if order["price"] <= 0:
        reasons.append("Price must be greater than 0")
    return reasons


def split_valid_and_invalid_orders(records):
    valid_orders = []
    invalid_orders = []
    for order in records:
        validation_errors = validate_order(order)
        if validation_errors:
            invalid_order = order.copy()
            invalid_order["reasons"] = validation_errors
            invalid_orders.append(invalid_order)
        else:
            valid_orders.append(order)
    return valid_orders, invalid_orders


def write_invalid_records(invalid_orders):
    with open(
        "output/invalid_records.txt",
        "w",
        encoding="utf-8"
    ) as file:
        file.write("INVALID RECORDS REPORT\n")
        file.write("=" * 50 + "\n\n")

        for order in invalid_orders:
            file.write(f"Order ID: {order['order_id']}\n")
            file.write(f"Customer: {order['customer_name']}\n")
            file.write("Reasons:\n")
            for reason in order["reasons"]:
                file.write(f"- {reason}\n")
            file.write("\n")


def write_validation_report(raw_records, valid_orders, invalid_orders):
    with open(
        "output/validation_report.txt",
        "w",
        encoding="utf-8"
    ) as file:
        file.write("DATA VALIDATION REPORT\n")
        file.write("=" * 50 + "\n\n")
        file.write(f"Raw records: {len(raw_records)}\n")
        file.write(f"Valid records: {len(valid_orders)}\n")
        file.write(f"Invalid records: {len(invalid_orders)}\n\n")
        file.write("Invalid record details:\n")
        file.write("-" * 50 + "\n")

        for order in invalid_orders:
            file.write(f"Order ID {order['order_id']}: ")
            file.write(", ".join(order["reasons"]))
            file.write("\n")


# --- Part 3 Functions ---
def normalize_status(status):
    s = status.strip().lower()
    if s in ["completed", "complete"]:
        return "completed"
    return s


def normalize_city(city):
    c = city.strip()
    if c.lower() in ["prishtine", "prishtina"]:
        return "Prishtina"
    return c.title()


def normalize_category(category):
    return category.strip().title()


def normalize_channel(channel):
    return channel.strip().lower()


def calculate_total_amount(order):
    return order["quantity"] * order["price"]


def clean_order(order):
    cleaned = order.copy()
    cleaned["status"] = normalize_status(order["status"])
    cleaned["city"] = normalize_city(order["city"])
    cleaned["category"] = normalize_category(order["category"])
    cleaned["channel"] = normalize_channel(order["channel"])
    cleaned["total_amount"] = calculate_total_amount(order)
    return cleaned


# --- Part 4 Functions ---
def get_completed_orders(clean_orders):
    return [order for order in clean_orders if order["status"] == "completed"]


def calculate_completed_revenue(clean_orders):
    completed = get_completed_orders(clean_orders)
    return sum(order["total_amount"] for order in completed)


# --- Part 5 Dynamic Dictionary Functions ---
def count_by_field(records, field_name):
    summary = {}
    for r in records:
        val = r.get(field_name)
        summary[val] = summary.get(val, 0) + 1
    return summary


def sum_revenue_by_field(records, field_name):
    summary = {}
    for r in records:
        if r["status"] == "completed":
            val = r.get(field_name)
            summary[val] = summary.get(val, 0) + r["total_amount"]
    return summary


def get_customers_with_multiple_orders(records):
    counts = count_by_field(records, "customer_name")
    return [cust for cust, count in counts.items() if count > 1]


def get_products_with_multiple_orders(records):
    counts = count_by_field(records, "product")
    return [prod for prod, count in counts.items() if count > 1]


# --- Part 6 Helper Functions for Sorting (No Lambdas) ---
def sort_key_total_amount(order):
    """Returns the total amount to sort orders descending."""
    return order["total_amount"]


def sort_key_dictionary_value(item_tuple):
    """Returns the dictionary value from an items tuple (key, value) for sorting."""
    return item_tuple[1]


def get_top_orders_by_total_amount(records, limit=5):
    completed = get_completed_orders(records)
    return sorted(completed, key=sort_key_total_amount, reverse=True)[:limit]


def get_top_elements_from_dict(summary_dict, limit=3):
    sorted_items = sorted(summary_dict.items(), key=sort_key_dictionary_value, reverse=True)
    return sorted_items[:limit]


# --- Part 8 Output File Generation ---
def write_business_report(cleaned_valid_orders, invalid_orders):
    completed_orders = get_completed_orders(cleaned_valid_orders)
    completed_revenue = calculate_completed_revenue(cleaned_valid_orders)
    
    avg_val = completed_revenue / len(completed_orders) if completed_orders else 0.0
    highest = max((o["total_amount"] for o in completed_orders), default=0.0)
    lowest = min((o["total_amount"] for o in completed_orders), default=0.0)
    
    rev_by_city = sum_revenue_by_field(cleaned_valid_orders, "city")
    rev_by_category = sum_revenue_by_field(cleaned_valid_orders, "category")
    rev_by_channel = sum_revenue_by_field(cleaned_valid_orders, "channel")
    
    with open("output/business_report.txt", "w", encoding="utf-8") as file:
        file.write("EXECUTIVE BUSINESS PERFORMANCE REPORT\n")
        file.write("=" * 50 + "\n\n")
        
        file.write("SECTION 1: KEY PERFORMANCE INDICATORS\n")
        file.write("-" * 50 + "\n")
        file.write(f"Total Completed Revenue: EUR {completed_revenue:,.2f}\n")
        file.write(f"Number of Completed Orders: {len(completed_orders)}\n")
        file.write(f"Average Order Size: EUR {avg_val:,.2f}\n")
        file.write(f"Highest Completed Order: EUR {highest:,.2f}\n")
        file.write(f"Lowest Completed Order: EUR {lowest:,.2f}\n\n")
        
        file.write("SECTION 2: PERFORMANCE BY DIMENSIONS\n")
        file.write("-" * 50 + "\n")
        file.write("Completed Revenue by City:\n")
        for city, rev in sorted(rev_by_city.items(), key=sort_key_dictionary_value, reverse=True):
            file.write(f"  - {city}: EUR {rev:,.2f}\n")
            
        file.write("\nCompleted Revenue by Category:\n")
        for cat, rev in sorted(rev_by_category.items(), key=sort_key_dictionary_value, reverse=True):
            file.write(f"  - {cat}: EUR {rev:,.2f}\n")
            
        file.write("\nCompleted Revenue by Channel:\n")
        for ch, rev in sorted(rev_by_channel.items(), key=sort_key_dictionary_value, reverse=True):
            file.write(f"  - {ch}: EUR {rev:,.2f}\n\n")
            
        file.write("SECTION 3: STRATEGIC BUSINESS RECOMMENDATIONS\n")
        file.write("-" * 50 + "\n")
        file.write("1. Mitigate Data Loss: Integrate frontend form validation rule controls to avoid \n")
        file.write("   costly data validation dropouts (such as missing names, empty prices, or wrong quantities).\n")
        file.write("2. Focus on Top Locations: Prishtina and Vushtrri generate our largest sales volumes.\n")
        file.write("   Focus high-tier digital ads and store operations on these core hubs.\n")


# --- Main Application Flow ---
def main():
    # Part 1: Raw Analysis
    print_raw_count(orders)
    print_first_three_records(orders)
    print_unique_raw_values(orders)

    # Part 2: Validation
    valid_orders, invalid_orders = split_valid_and_invalid_orders(orders)

    write_invalid_records(invalid_orders)
    write_validation_report(orders, valid_orders, invalid_orders)

    print("\n" + "=" * 50)
    print("VALIDATION SUMMARY")
    print("=" * 50)

    print(f"Raw records: {len(orders)}")
    print(f"Valid records: {len(valid_orders)}")
    print(f"Invalid records: {len(invalid_orders)}")

    print("\nInvalid records:")
    for order in invalid_orders:
        print(f"\nOrder ID: {order['order_id']}")
        for reason in order["reasons"]:
            print(f"- {reason}")

    # Part 3: Cleaning & Normalization
    cleaned_valid_orders = []
    for order in valid_orders:
        cleaned_valid_orders.append(clean_order(order))

    cleaned_statuses = []
    cleaned_cities = []
    cleaned_categories = []
    cleaned_channels = []

    for order in cleaned_valid_orders:
        if order["status"] not in cleaned_statuses:
            cleaned_statuses.append(order["status"])
        if order["city"] not in cleaned_cities:
            cleaned_cities.append(order["city"])
        if order["category"] not in cleaned_categories:
            cleaned_categories.append(order["category"])
        if order["channel"] not in cleaned_channels:
            cleaned_channels.append(order["channel"])

    print("\n" + "=" * 50)
    print("UNIQUE CLEANED VALUES AFTER CLEANING:")
    print("=" * 50)

    print("Cleaned statuses:")
    for status in sorted(cleaned_statuses):
        print(f"- {status}")

    print("\nCleaned cities:")
    for city in sorted(cleaned_cities):
        print(f"- {city}")

    print("\nCleaned categories:")
    for category in sorted(cleaned_categories):
        print(f"- {category}")

    print("\nCleaned channels:")
    for channel in sorted(cleaned_channels):
        print(f"- {channel}")

    # Part 4: Business Metrics
    completed_orders = get_completed_orders(cleaned_valid_orders)
    
    non_revenue_count = 0
    for order in cleaned_valid_orders:
        if order["status"] in ["pending", "cancelled", "returned"]:
            non_revenue_count += 1
            
    completed_revenue = calculate_completed_revenue(cleaned_valid_orders)
    completed_count = len(completed_orders)
    
    if completed_count > 0:
        avg_completed_value = completed_revenue / completed_count
    else:
        avg_completed_value = 0.0
        
    if completed_orders:
        highest_order_value = max(order["total_amount"] for order in completed_orders)
        lowest_order_value = min(order["total_amount"] for order in completed_orders)
    else:
        highest_order_value = 0.0
        lowest_order_value = 0.0

    print("\n" + "=" * 50)
    print("PART 4: BUSINESS METRICS SUMMARY")
    print("=" * 50)
    print(f"Raw records: {len(orders)}")
    print(f"Valid records: {len(cleaned_valid_orders)}")
    print(f"Invalid records: {len(invalid_orders)}")
    print(f"Completed orders: {completed_count}")
    print(f"Non-revenue orders: {non_revenue_count}")
    print(f"Completed revenue: {completed_revenue:.2f}")
    print(f"Average completed order value: {avg_completed_value:.2f}")
    print(f"Highest completed order: {highest_order_value:.2f}")
    print(f"Lowest completed order: {lowest_order_value:.2f}")

    # Part 5: Dynamic Reports Using Dictionaries
    orders_by_status = count_by_field(cleaned_valid_orders, "status")
    orders_by_city = count_by_field(cleaned_valid_orders, "city")
    orders_by_category = count_by_field(cleaned_valid_orders, "category")
    orders_by_channel = count_by_field(cleaned_valid_orders, "channel")
    
    rev_by_city = sum_revenue_by_field(cleaned_valid_orders, "city")
    rev_by_category = sum_revenue_by_field(cleaned_valid_orders, "category")
    rev_by_channel = sum_revenue_by_field(cleaned_valid_orders, "channel")
    rev_by_customer = sum_revenue_by_field(cleaned_valid_orders, "customer_name")
    
    mult_orders_cust = get_customers_with_multiple_orders(cleaned_valid_orders)
    mult_orders_prod = get_products_with_multiple_orders(cleaned_valid_orders)

    print("\n" + "=" * 50)
    print("PART 5: DYNAMIC REPORTS USING DICTIONARIES")
    print("=" * 50)
    
    print("\nOrders count by status:")
    for key, val in orders_by_status.items():
        print(f"- {key}: {val}")
        
    print("\nOrders count by city:")
    for key, val in orders_by_city.items():
        print(f"- {key}: {val}")

    print("\nRevenue by city:")
    for key, val in rev_by_city.items():
        print(f"- {key}: EUR {val:.2f}")

    print("\nRevenue by customer:")
    for key, val in rev_by_customer.items():
        print(f"- {key}: EUR {val:.2f}")
        
    print("\nCustomers with multiple orders:")
    for cust in mult_orders_cust:
        print(f"- {cust}")

    # Part 6: Top Records and Ranking
    top_5_orders = get_top_orders_by_total_amount(cleaned_valid_orders, 5)
    top_3_cust = get_top_elements_from_dict(rev_by_customer, 3)
    
    rev_by_product = sum_revenue_by_field(cleaned_valid_orders, "product")
    top_3_products = get_top_elements_from_dict(rev_by_product, 3)

    print("\n" + "=" * 50)
    print("PART 6: TOP RECORDS AND RANKINGS")
    print("=" * 50)
    
    print("\nTop 5 Completed Orders by Total Value:")
    for o in top_5_orders:
        print(f"- Order ID {o['order_id']} | {o['customer_name']} | {o['product']}: EUR {o['total_amount']:.2f}")
        
    print("\nTop 3 Customers by Completed Revenue:")
    for cust, rev in top_3_cust:
        print(f"- {cust}: EUR {rev:.2f}")
        
    print("\nTop 3 Products by Completed Revenue:")
    for prod, rev in top_3_products:
        print(f"- {prod}: EUR {rev:.2f}")

    # Part 7: Data Quality Investigation
    print("\n" + "=" * 50)
    print("PART 7: DATA QUALITY INVESTIGATION")
    print("=" * 50)
    print(f"1. Removed {len(invalid_orders)} invalid records due to bad input data (missing names, 0 price/quantity).")
    print(f"2. {non_revenue_count} valid orders are pending, cancelled, or returned, which don't count as active business revenue.")
    print("3. Pre-cleaning status values had case errors ('Completed', 'complete'). We standardized them into 'completed'.")
    print("4. Calculating metrics on unvalidated raw records would skew average value stats and inject non-completed cash flows.")

    # Part 8: Executive Report Generation
    write_business_report(cleaned_valid_orders, invalid_orders)


if __name__ == "__main__":
    main()