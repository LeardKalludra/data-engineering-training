### 1. What are the main entities in this project?
The main entities are **Customers**, **Products**, **Orders**, and **Order Items**[cite: 1].

### 2. Which table should store customers?
The `customers` table stores customer profile details like `customer_name`, `city`, and `segment`[cite: 1].

### 3. Which table should store products?
The `products` table stores catalog information including `product_name`, `category`, and `price`[cite: 1].

### 4. Which table should store orders?
The `orders` table stores transaction metadata, such as `customer_id`, `order_date`, `status`, and `channel`[cite: 1].

### 5. Why should orders not repeat all customer and product details directly?
Repeating names, cities, and prices inside orders creates severe data duplication[cite: 1]. If a customer updates their name or a product price changes, updating every historic row causes inconsistency and bloated storage. Splitting entities ensures normalisation and data integrity[cite: 1].

### 6. What is the relationship between customers and orders?
It is a **One-to-Many (1:N)** relationship[cite: 1]. One customer can place many orders, but each order belongs to exactly one customer[cite: 1].

### 7. What is the relationship between orders and products?
It is a **Many-to-Many (M:N)** relationship[cite: 1]. An order can contain multiple products, and a single product can be purchased across multiple different orders[cite: 1].

### 8. Why do we need an order_items table?
Relational databases cannot natively handle direct Many-to-Many links[cite: 1]. The `order_items` table acts as a **bridge/junction table** that breaks the M:N relationship into two 1:N relationships (`orders` $\rightarrow$ `order_items` $\leftarrow$ `products`) and holds item-specific attributes like `quantity`[cite: 1].