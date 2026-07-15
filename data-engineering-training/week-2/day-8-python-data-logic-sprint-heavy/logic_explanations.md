# Logic Explanations - Day 8 Practice

### 1. Why we run validation before revenue calculation
Validating the raw dataset ensures we exclude corrupted metrics. If we compute total revenue using orders that lack prices (e.g., price = 0), or contain negative quantities, our resulting operational metrics will be incorrect.

### 2. How status normalization works
We clean string values by stripping whitespace and converting everything to lowercase. Specifically, standardizing variants such as "Completed" and "complete" into the unified label "completed" allows exact-match lookups to evaluate accurate transaction sums.

### 3. Why only completed orders count as business revenue
Active business cash flow depends on finalized transactions. Pending, cancelled, or returned orders represent potential or reversed transactions and do not constitute cleared business income.

### 4. How `count_by_field` works step-by-step
1. Initialize an empty dictionary.
2. Iterate through each clean dictionary record.
3. Fetch the value of the targeted field (such as "city").
4. If it's the first time seeing this value, initialize its count at 0 and add 1. If it already exists, increment its count value.

### 5. How `sum_revenue_by_field` works step-by-step
1. Initialize an empty dictionary.
2. Iterate through each valid cleaned record.
3. Check if the status is exactly "completed".
4. If completed, fetch the field value and add the calculated `total_amount` to that specific group's running total.

### 6. How sorting is used to find top records
We use Python's built-in `sorted()` function combined with `lambda` expressions as sorting keys (e.g., extracting `total_amount`), setting `reverse=True` to place the highest elements at the beginning of the resulting list.

### 7. What `main()` does and why it improves script structure
The `main()` function organizes our code's operational sequence. By grouping executive commands inside a single caller block, we keep our helper functions clean, isolated, and highly reusable.