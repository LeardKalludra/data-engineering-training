def load_orders():
    with open("data/orders.csv", "r") as file:
        lines = file.readlines()
    return lines


def calculate_total_amount(lines):
    orders = []
    for line in lines[1:]:
        if not line.strip():
            continue
        columns = line.strip().split(",")
        order = {
            "order_id": int(columns[0]),
            "customer_name": columns[1],
            "city": columns[2],
            "product": columns[3],
            "category": columns[4],
            "quantity": int(columns[5]),
            "price": float(columns[6]),
            "status": columns[7],
        }
        order["total_amount"] = order["quantity"] * order["price"]
        orders.append(order)
    return orders


def get_completed_orders(orders):
    print("\n--- Completed Orders ---")
    for o in orders:
        if o["status"] == "completed":
            print(f"ID: {o["order_id"]} | Name: {o["customer_name"]} | Product: {o["product"]}")


def get_other_orders(orders):
    print("\n--- Pending & Cancelled Orders ---")
    for o in orders:
        if o["status"] != "completed":
            print(f"ID: {o["order_id"]} | Name: {o["customer_name"]} | Status: {o["status"]}")


def calculate_completed_revenue(orders):
    revenue = 0.0
    for o in orders:
        if o["status"] == "completed":
            revenue += o["total_amount"]
    return revenue


def find_most_expensive_single(orders):
    most_expensive = orders[0]
    for o in orders:
        if o["price"] > most_expensive["price"]:
            most_expensive = o
    return most_expensive


def find_highest_total_amount(orders):
    highest_total = orders[0]
    for o in orders:
        if o["total_amount"] > highest_total["total_amount"]:
            highest_total = o
    return highest_total


def count_by_status(orders):
    counts = {}
    for o in orders:
        status = o["status"]
        counts[status] = counts.get(status, 0) + 1
    return counts


def count_by_city(orders):
    counts = {}
    for o in orders:
        city = o["city"]
        counts[city] = counts.get(city, 0) + 1
    return counts


def count_by_category(orders):
    counts = {}
    for o in orders:
        cat = o["category"]
        counts[cat] = counts.get(cat, 0) + 1
    return counts


def print_business_report(total, rev, max_p, max_t, statuses, cities, cats):
    print("\n================ BUSINESS REPORT ================")
    print(f"Total Number of Orders: {total}")
    print(f"Total Completed Revenue: €{rev:.2f}")
    print(f"Most Expensive Single Item: {max_p["product"]} (€{max_p["price"]:.2f})")
    print(f"Highest Total Amount Order: ID {max_t["order_id"]} (€{max_t["total_amount"]:.2f})")
    
    print("\nOrders by Status:")
    for k, v in statuses.items():
        print(f"  {k}: {v}")
        
    print("\nOrders by City:")
    for k, v in cities.items():
        print(f"  {k}: {v}")
        
    print("\nOrders by Category:")
    for k, v in cats.items():
        print(f"  {k}: {v}")
    print("=================================================")


def main():
    raw_lines = load_orders()
    orders = calculate_total_amount(raw_lines)
    
    get_completed_orders(orders)
    get_other_orders(orders)
    
    revenue = calculate_completed_revenue(orders)
    max_price_order = find_most_expensive_single(orders)
    max_total_order = find_highest_total_amount(orders)
    
    status_dict = count_by_status(orders)
    city_dict = count_by_city(orders)
    category_dict = count_by_category(orders)
    
    print_business_report(
        len(orders), 
        revenue, 
        max_price_order, 
        max_total_order, 
        status_dict, 
        city_dict, 
        category_dict
    )


if __name__ == "__main__":
    main()
    