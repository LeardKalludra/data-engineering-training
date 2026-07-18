# Layer Explanation

## Bronze layer
- What files are stored here? 
  `orders_raw.csv`, `customers_raw.csv`, and `products_raw.csv`.
- Why do we keep raw data unchanged? 
  To protect historical single-source-of-truth records and allow reprocessing if our rules update.
- What data problems did you notice? 
  Missing items, mixed date layouts, trailing punctuation, negative totals, and string symbols in number entries.
- Which data problems could break business reports if they are not cleaned? 
  Alphabetical characters in integer fields break quantitative aggregates, and duplicate order IDs inflate operational results.

## Silver layer
- What cleaning rules did you apply? 
  Enforced field presence checks, normalized geographic names, parsed statuses, and filtered out non-positive digits.
- Which records became invalid and why? 
  Orders with absent dates, invalid quantities like letters or negative amounts, and reference keys not present in clean dimension collections.
- What columns were added during enrichment? 
  `customer_name`, `city`, `product_name`, `category`, `price`, and calculated `total_amount`.
- Why is Silver safer than Bronze? 
  It ensures mathematical data validity and referential integrity guarantees prior to reporting extraction.

## Gold layer
- Which reports did you create? 
  Category performance, regional sales summaries, top client profiles, and asset trends reports.
- Which business questions do these reports answer? 
  Where revenue groups are dense, what items hold the highest inventory velocity, and who drives sales volumes.
- Why should dashboards use Gold outputs instead of raw Bronze data? 
  Gold removes corrupted transactional rows, ensuring business evaluations use accurate metrics.