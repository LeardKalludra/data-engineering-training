orders = [
    {
        "order_id": 1,
        "customer_name": "Arta",
        "city": "Vushtrri",
        "product": "Laptop",
        "category": "Electronics",
        "quantity": 1,
        "price": 700,
        "status": "completed",
        "order_date": "2026-07-01"
    },
    {
        "order_id": 2,
        "customer_name": "Blend",
        "city": "Prishtina",
        "product": "Mouse",
        "category": "Accessories",
        "quantity": 2,
        "price": 15,
        "status": "completed",
        "order_date": "2026-07-01"
    },
    {
        "order_id": 3,
        "customer_name": "Arta",
        "city": "Vushtrri",
        "product": "Keyboard",
        "category": "Accessories",
        "quantity": 1,
        "price": 40,
        "status": "cancelled",
        "order_date": "2026-07-02"
    },
    {
        "order_id": 4,
        "customer_name": "Dren",
        "city": "Mitrovica",
        "product": "Monitor",
        "category": "Electronics",
        "quantity": 1,
        "price": 180,
        "status": "completed",
        "order_date": "2026-07-02"
    },
    {
        "order_id": 5,
        "customer_name": "Elira",
        "city": "Prishtina",
        "product": "Mouse",
        "category": "Accessories",
        "quantity": 1,
        "price": 15,
        "status": "completed",
        "order_date": "2026-07-03"
    },
    {
        "order_id": 6,
        "customer_name": "Dren",
        "city": "Mitrovica",
        "product": "Laptop",
        "category": "Electronics",
        "quantity": 1,
        "price": 700,
        "status": "pending",
        "order_date": "2026-07-03"
    },
    {
        "order_id": 7,
        "customer_name": "Nora",
        "city": "Vushtrri",
        "product": "Headphones",
        "category": "Accessories",
        "quantity": 1,
        "price": 50,
        "status": "completed",
        "order_date": "2026-07-04"
    },
    {
        "order_id": 8,
        "customer_name": "Leart",
        "city": "Peja",
        "product": "Monitor",
        "category": "Electronics",
        "quantity": 2,
        "price": 180,
        "status": "completed",
        "order_date": "2026-07-04"
    },
    {
        "order_id": 9,
        "customer_name": "Faton",
        "city": "Prizren",
        "product": "Desk Chair",
        "category": "Office",
        "quantity": 1,
        "price": 120,
        "status": "completed",
        "order_date": "2026-07-05"
    },
    {
        "order_id": 10,
        "customer_name": "Gresa",
        "city": "Prishtina",
        "product": "USB Cable",
        "category": "Accessories",
        "quantity": 3,
        "price": 8,
        "status": "completed",
        "order_date": "2026-07-05"
    },
    {
        "order_id": 11,
        "customer_name": "Rina",
        "city": "Vushtrri",
        "product": "Laptop",
        "category": "Electronics",
        "quantity": 1,
        "price": 650,
        "status": "cancelled",
        "order_date": "2026-07-06"
    },
    {
        "order_id": 12,
        "customer_name": "Arben",
        "city": "Ferizaj",
        "product": "Desk",
        "category": "Office",
        "quantity": 1,
        "price": 220,
        "status": "pending",
        "order_date": "2026-07-06"
    },
    {
        "order_id": 13,
        "customer_name": "Agon",
        "city": "Prishtina",
        "product": "Tablet",
        "category": "Electronics",
        "quantity": 1,
        "price": 300,
        "status": "completed",
        "order_date": "2026-07-07"
    },
    {
        "order_id": 14,
        "customer_name": "Vala",
        "city": "Peja",
        "product": "Paper",
        "category": "Office",
        "quantity": 5,
        "price": 5,
        "status": "cancelled",
        "order_date": "2026-07-07"
    }
]

def print_basic_data():
    print(f"Total orders: {len(orders)}")
    print("\nCustomer names:")
    for costumers in orders:
        print(costumers["customer_name"])
    print("\nOrder details:")
    for costumers in orders:
        print(f"{costumers["customer_name"]} ordered {costumers["product"]} from {costumers["city"]} and the status is {costumers["status"]}.")

def print_filtered_records():
    print("\nCompleted orders:")
    for costumers in orders:
        if costumers["status"] == "completed":
            print(f"{costumers["order_id"]} - {costumers["customer_name"]} - {costumers["product"]}")
    print("\nPending orders:")
    for costumers in orders:
        if costumers["status"] == "pending":
            print(f"{costumers["order_id"]} - {costumers["customer_name"]} - {costumers["product"]}")
    print("\nCancelled orders:")
    for costumers in orders:
        if costumers["status"] == "cancelled":
            print(f"{costumers["order_id"]} - {costumers["customer_name"]} - {costumers["product"]}")        
    print("\nOrders where price is greater than 100:")
    for costumers in orders:
        if costumers["price"] > 100:
            print(f"{costumers["customer_name"]} - {costumers["price"]}")                
    print("\nOrders where category is Accessories.")
    for costumers in orders:
        if costumers["category"] == "Accessories":
            print(f"{costumers["customer_name"]} - {costumers["category"]}")                

def print_calculated_values():
    print("\nOrder totals:")
    total_amount = 0
    for costumers in orders:
        total_amount = costumers["quantity"] * costumers["price"]
        print(f"{costumers["customer_name"]} - {costumers["product"]} - {costumers["quantity"]} x {costumers["price"]} = {total_amount}")           

def get_price(item):
    return item["price"]

def get_total_amount(item):
    return item["quantity"] * item["price"]

def print_sorting_and_top_records():
    print("\nOrders from most expensive to cheapest by price:")
    orders_sorted_by_price = sorted(orders, key=get_price, reverse=True)
    for costumers in orders_sorted_by_price:
        print(f"{costumers["customer_name"]} - {costumers["product"]}")
    print("\nOrders from highest to lowest by total amount:")
    orders_sorted = sorted(orders, key=get_total_amount, reverse=True)
    for costumers in orders_sorted:
        total_amount = costumers["quantity"] * costumers["price"]
        print(f"{costumers["customer_name"]} - {costumers["product"]} - {total_amount}")
    print("\nTop 3 orders by total amount:")
    for costumers in orders_sorted[:3]:
        total_amount = costumers["quantity"] * costumers["price"]
        print(f"{costumers["customer_name"]} - {costumers["product"]} - {total_amount}")

def print_simple_summary():
    print("\nStatus counts:")
    completed_count = 0
    pending_count = 0
    cancelled_count = 0
    for costumers in orders:
        if costumers["status"] == "completed":
            completed_count = completed_count + 1
        if costumers["status"] == "pending":
            pending_count = pending_count + 1
        if costumers["status"] == "cancelled":
            cancelled_count = cancelled_count + 1
    print(f"completed: {completed_count}")
    print(f"pending: {pending_count}")
    print(f"cancelled: {cancelled_count}")
    total_revenue = 0
    for costumers in orders:
        if costumers["status"] == "completed":
            total_revenue = total_revenue + (costumers["quantity"] * costumers["price"])
    print(f"Completed revenue: {total_revenue}")
    print("\nCustomers who have more than one order:")
    order_counts = {}
    for costumers in orders:
        name = costumers["customer_name"]
        if name in order_counts:
            order_counts[name] = order_counts[name] + 1
        else:
            order_counts[name] = 1
    for name in order_counts:
        if order_counts[name] > 1:
            print(f"{name} - {order_counts[name]} orders")

def print_business_challenge_and_bonus():
    print("\n--- Part 4: Mini Business Challenge ---")
    expensive_order = max(orders, key=get_price)
    print(f"Most expensive single order customer: {expensive_order["customer_name"]} (${expensive_order["price"]})")
    highest_total_order = max(orders, key=get_total_amount)
    highest_total = highest_total_order["quantity"] * highest_total_order["price"]
    print(f"Highest total_amount order: {highest_total_order["customer_name"]} - {highest_total_order["product"]} (${highest_total})")
    print("\nOrders NOT counted as real revenue (Pending/Cancelled):")
    for costumers in orders:
        if costumers["status"] == "pending" or costumers["status"] == "cancelled":
            print(f"{costumers["customer_name"]} - {costumers["product"]} ({costumers["status"]})")
    print("\nBusiness Answer 1:")
    print("The most valuable orders are Arta's Laptop (Order 1) and Dren's Laptop (Order 6), valued at $700 each. However, since Dren's order is pending, Arta's completed order is currently the most valuable secured revenue.")
    print("\nBusiness Answer 2:")
    print("Cancelled orders represent transactions that were never completed. Counting them would artificially inflate financial metrics with money the business never received.")
    print("\n--- Bonus Tasks ---")
    city_counts = {}
    for costumers in orders:
        city = costumers["city"]
        if city in city_counts:
            city_counts[city] = city_counts[city] + 1
        else:
            city_counts[city] = 1
    print(f"Orders by city: {city_counts}")
    category_counts = {}
    for costumers in orders:
        cat = costumers["category"]
        if cat in category_counts:
            category_counts[cat] = category_counts[cat] + 1
        else:
            category_counts[cat] = 1
    print(f"Orders by category: {category_counts}")

print_basic_data()
print_filtered_records()
print_calculated_values()
print_sorting_and_top_records()
print_simple_summary()
print_business_challenge_and_bonus()