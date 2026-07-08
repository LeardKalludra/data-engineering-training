# Data Pipeline Thinking - Day 3

Chosen business: 
Restaurant

Source Data: 
Digital receipts from the restaurant cash register and online app.

Ingestion: 
Loading the daily sales files into our database.

Storage: 
Saving the data in the `food_orders` table.

Cleaning: 
Removing duplicate orders and fixing missing customer names.

Transformation: 
Multiplying quantity by price to find the total cost of each order.

Business Output: 
A daily sales report for the restaurant manager.

Business questions we can answer:
1. What is today's total revenue?
2. Which dish is ordered the most?
3. How many orders are currently pending?

Possible data problems:
1. Missing price values for some food items.
2. Typos in food names (like "Piza" instead of "Pizza").
3. Duplicate clicks causing the same order to show up twice.