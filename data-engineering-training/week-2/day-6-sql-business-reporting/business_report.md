# Business Report - Day 6 SQL Business Reporting Sprint

1. **Total orders**: 14
2. **Completed orders**: 10
3. **Pending orders**: 2
4. **Cancelled orders**: 2
5. **Completed revenue**: $1499.00
6. **Product with highest completed revenue**: Laptop ($700.00)
7. **Category with highest completed revenue**: Electronics ($1060.00)
8. **City with most orders**: Prishtina (4 orders)
9. **City with highest completed revenue**: Vushtrri ($750.00)
10. **Customer with highest completed revenue**: Arta ($700.00)
11. **Customers with more than one order**: Arta (2), Blend (2), Dren (2), Elira (2)
12. **Orders that should not count as real revenue**: Pending and Cancelled orders. Cancelled transactions are permanently lost, and pending transactions are volatile risk factors that haven't cleared financially. 
13. **One business recommendation**: Expand operations and marketing structures within Vushtrri. Despite having fewer orders than Prishtina, it drives our highest revenue concentration due to high-value item adoption.
14. **One data quality or reporting risk**: The system lacks structured constraints tracking product historical pricing changes over time; calculating revenue directly dynamically from a changing `products.price` table will retroactively alter accurate historical sales figures.
15. **What this report would help a manager decide**: It directly helps inventory management optimize electronics and hardware logistics while signaling where localized B2B marketing pushes are succeeding.