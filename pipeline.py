# Sales Data Pipeline
# Multi Store Data cleaning and analysis

import csv
from datetime import datetime

def read_csv(filename):
    rows = []
    try:
        with open(filename, "r") as f:
            reader = csv.DictReader(f)
            for row in reader:
                rows.append(row)
        print(f"Loaded {len(rows)} rows from {filename}")
    except FileNotFoundError:
        print(f"Error : {filename} not found")
        
    return rows

# Load all 3 stores
store1 = read_csv("store1.csv")
store2 = read_csv("store2.csv")
store3 = read_csv("store3.csv")

# Merge into one list
all_rows = store1 + store2 + store3
print(f"\nTotal rows loaded: {len(all_rows)}")

# Clean and validate each rows
def clean_row(row):
    
    name = row["product"].strip().title()
    
    store = row["store"].strip()
    
    date = row["date"].strip()
    
    try:
        price = float(row["price"])
    except ValueError:
        return None, f"Invalid price: {row['price']}"
    
    try:
        quantity = int(row["quantity"])
    except ValueError:
        return None, f"Invalid quantity: {row['quantity']}"
    
    if quantity <= 0:
        return None, f"Quantity must be above 0"
    
    revenue = quantity * price
    
    clean = {
        "date":      date,
        "product":   name,
        "store":     store,
        "price":     price,
        "quantity":  quantity,
        "revenue":   revenue
    }
    return clean, None

clean_data = []
rejected   = []

for row in all_rows:
    record, error = clean_row(row)
    
    if error:
        rejected.append({"row": row, "reason": error})
    else:
        clean_data.append(record)
        
print(f"\nClean rows: {len(clean_data)}")
print(f"Rejected rows: {len(rejected)}")

if rejected:
    print("\nRejected")
    for r in rejected:
        print(f"  x {r['row']['product']} - {r['reason']}")
        

# Analyze the clean data

total_revenue = sum(row["revenue"] for row in clean_data)

# Revenue by store
store_revenue = {}
for row in clean_data:
    store = row["store"]
    store_revenue[store] = store_revenue.get(store, 0) + row["revenue"]
    
# Revenue by product
product_revenue = {}
for row in clean_data:
    product = row["product"]
    product_revenue[product] = product_revenue.get(product, 0) + row["revenue"]
    
# Best and worst performing store
best_store = max(store_revenue, key=lambda s: store_revenue[s])
worst_store = min(store_revenue, key=lambda s: store_revenue[s])

# best and Worst selling product
best_product = max(product_revenue, key=lambda p:product_revenue[p])
worst_product= min(product_revenue, key=lambda p:product_revenue[p])

# Print Analysis
print("\n---Analysis---")
print(f"Total revenue: ${total_revenue:,}")
print(f"Revenue by store:")
for store, revenue in store_revenue.items():
    print(f"  {store}:  ${revenue:,}")
print(f"Revenue by product:")
for product, revenue in product_revenue.items():
    print(f"   {product}: ${revenue:,}")
print(f"\nBest store: {best_store} (${store_revenue[best_store]:,})")
print(f"Worst store: {worst_store} (${store_revenue[worst_store]:,}) ")
print(f"Best product: {best_product} (${product_revenue[best_product]:,})")
print(f"Worst product: {worst_product} (${product_revenue[worst_product]:,})")


# ── STEP 5: Save clean data to CSV ──────────────
fields = ["date", "product", "store", "price", "quantity", "revenue"]

with open("clean_data.csv", "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=fields)
    writer.writeheader()
    writer.writerows(clean_data)

print("\nClean data saved to clean_data.csv")

# ── STEP 6: Save professional report ────────────
now = datetime.now().strftime("%Y-%m-%d %H:%M")

with open("sales_report.txt", "w") as f:
    f.write("=" * 40 + "\n")
    f.write("     SALES PIPELINE REPORT\n")
    f.write(f"     Generated: {now}\n")
    f.write("=" * 40 + "\n\n")

    f.write("PIPELINE SUMMARY\n")
    f.write("-" * 40 + "\n")
    f.write(f"Total rows loaded  : {len(all_rows)}\n")
    f.write(f"Clean rows         : {len(clean_data)}\n")
    f.write(f"Rejected rows      : {len(rejected)}\n\n")

    if rejected:
        f.write("REJECTED ROWS\n")
        f.write("-" * 40 + "\n")
        for r in rejected:
            f.write(f"  x {r['row']['product']} - {r['reason']}\n")
        f.write("\n")

    f.write("REVENUE BY STORE\n")
    f.write("-" * 40 + "\n")
    for store, revenue in store_revenue.items():
        f.write(f"  {store}: ${revenue:,.0f}\n")
    f.write("\n")

    f.write("REVENUE BY PRODUCT\n")
    f.write("-" * 40 + "\n")
    for product, revenue in product_revenue.items():
        f.write(f"  {product}: ${revenue:,.0f}\n")
    f.write("\n")

    f.write("TOP PERFORMERS\n")
    f.write("-" * 40 + "\n")
    f.write(f"  Best store    : {best_store} (${store_revenue[best_store]:,.0f})\n")
    f.write(f"  Worst store   : {worst_store} (${store_revenue[worst_store]:,.0f})\n")
    f.write(f"  Best product  : {best_product} (${product_revenue[best_product]:,.0f})\n")
    f.write(f"  Worst product : {worst_product} (${product_revenue[worst_product]:,.0f})\n\n")

    f.write("=" * 40 + "\n")
    f.write(f"  Total revenue : ${total_revenue:,.0f}\n")
    f.write("=" * 40 + "\n")

print("Report saved to sales_report.txt")
print("\nPipeline complete!")
