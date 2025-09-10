import os
import random
import numpy as np
import pandas as pd
from faker import Faker
from datetime import datetime, timedelta, date

# ------------------------
# Configuration / Reproducibility
# ------------------------
RANDOM_SEED = 42
random.seed(RANDOM_SEED)
np.random.seed(RANDOM_SEED)
Faker.seed(RANDOM_SEED)

# Initialize faker
fake = Faker()

# Output directory
OUTPUT_DIR = "data/raw"
os.makedirs(OUTPUT_DIR, exist_ok=True)


# Customers dataset -------------------------------------------------->

n_customers = 800  
customer_ids = list(range(1, n_customers + 1))

customers = []
for cid in customer_ids:
    name = fake.name()
    age = random.randint(18, 75)
    gender = random.choice(["Male", "Female", "Other"])
    location = fake.city()
    signup_date = fake.date_between(start_date="-5y", end_date="today")
    customers.append([cid, name, age, gender, location, signup_date])

df_customers = pd.DataFrame(customers, columns=[
    "customer_id", "name", "age", "gender", "location", "signup_date"
])


# Products dataset ------------------------------------------------------->

n_products = 300  
product_ids = list(range(1, n_products + 1))

categories = {
    "Electronics": ["Smartphone", "Laptop", "Headphones", "Smartwatch", "Camera"],
    "Fashion": ["T-shirt", "Jeans", "Sneakers", "Jacket", "Dress"],
    "Home": ["Sofa", "Dining Table", "Bed Frame", "Chair", "Cookware"],
    "Books": ["Novel", "Biography", "Textbook", "Comics", "Cookbook"],
    "Beauty": ["Lipstick", "Perfume", "Shampoo", "Skincare Cream", "Makeup Kit"]
}

products = []
for pid in product_ids:
    category = random.choice(list(categories.keys()))
    product_name = random.choice(categories[category]) + f" {random.randint(1,999)}"
    price = round(random.uniform(5, 2000), 2)
    products.append([pid, category, product_name, price])

df_products = pd.DataFrame(products, columns=[
    "product_id", "category", "product_name", "price"
])


# Orders dataset ----------------------------------------------------------->

n_orders = 20000  

orders = []

# 80% of customers are active
active_customers = np.random.choice(customer_ids, size=int(0.8 * len(customer_ids)), replace=False)

# Assign order counts per customer (Poisson distributed)
# Convert customer IDs to int for consistent typing
customer_order_counts = {int(cid): int(np.random.poisson(lam=25)) for cid in active_customers}

order_id = 1
for cid, count in customer_order_counts.items():
    if count <= 0:
        continue  

    # Retrieve age for customer
    age = int(df_customers.loc[df_customers["customer_id"] == cid, "age"].values[0])

    # Category preference by age
    if age < 30:
        category_weights = {"Fashion": 0.4, "Electronics": 0.3, "Home": 0.1, "Books": 0.1, "Beauty": 0.1}
    elif age < 50:
        category_weights = {"Fashion": 0.2, "Electronics": 0.3, "Home": 0.2, "Books": 0.2, "Beauty": 0.1}
    else:
        category_weights = {"Fashion": 0.1, "Electronics": 0.2, "Home": 0.4, "Books": 0.2, "Beauty": 0.1}

    categories_list = list(category_weights.keys())
    weights = list(category_weights.values())

    for _ in range(count):
        # Pick category based on weights
        category = np.random.choice(categories_list, p=weights)
        product_subset = df_products[df_products["category"] == category]
        if product_subset.empty:
            # Fallback to random product if a category is empty for any reason
            product_row = df_products.sample(1).iloc[0]
        else:
            product_row = product_subset.sample(1).iloc[0]

        product_id = int(product_row["product_id"])
        price = float(product_row["price"])

        # Skew dates toward recent years using an exponential distribution
        days_offset = int(np.random.exponential(scale=500))
        dt_ord = datetime.today() - timedelta(days=days_offset)
        # If the sampled date goes beyond the 5-year window, draw a faker date instead
        if dt_ord < datetime.today() - timedelta(days=5 * 365):
            dt_ord = fake.date_between(start_date="-5y", end_date="today")

        # Normalize order_date to a datetime.date object to keep CSV column consistent
        if isinstance(dt_ord, datetime):
            order_date = dt_ord.date()
        elif isinstance(dt_ord, date):
            order_date = dt_ord
        else:
            # Last-resort conversion
            order_date = pd.to_datetime(dt_ord).date()

        quantity = np.random.choice([1, 2, 3, 4, 5], p=[0.7, 0.15, 0.1, 0.04, 0.01])
        total_amount = round(price * quantity, 2)

        orders.append([order_id, cid, product_id, order_date, quantity, total_amount])
        order_id += 1

# Truncate to max n_orders if needed
if len(orders) > n_orders:
    orders = orders[:n_orders]

# Build DataFrame
df_orders = pd.DataFrame(orders, columns=[
    "order_id", "customer_id", "product_id", "order_date", "quantity", "total_amount"
])


# Save to CSV ---------------------------------------------------------------->

df_customers.to_csv(os.path.join(OUTPUT_DIR, "customers.csv"), index=False)
df_products.to_csv(os.path.join(OUTPUT_DIR, "products.csv"), index=False)
df_orders.to_csv(os.path.join(OUTPUT_DIR, "orders.csv"), index=False)


# Reload to validate CSV integrity
c = pd.read_csv(os.path.join(OUTPUT_DIR, "customers.csv"))
p = pd.read_csv(os.path.join(OUTPUT_DIR, "products.csv"))
o = pd.read_csv(os.path.join(OUTPUT_DIR, "orders.csv"))

# Referential integrity checks
customers_ok = o['customer_id'].isin(c['customer_id']).all()
products_ok = o['product_id'].isin(p['product_id']).all()

print("Synthetic datasets generated in /data/raw/ with realistic distributions")
print(f" - customers: {len(c)} rows")
print(f" - products: {len(p)} rows")
print(f" - orders: {len(o)} rows (generated, may be truncated to {n_orders})")
print(f" - referential integrity: customers_ok={customers_ok}, products_ok={products_ok}")

# Extra statistics
num_customers_with_orders = o['customer_id'].nunique()
num_customers = len(c)
print(f" - customers with >=1 order: {num_customers_with_orders} / {num_customers}")

# Date range check
o['order_date'] = pd.to_datetime(o['order_date'])
print(f" - orders date range: {o['order_date'].min().date()} to {o['order_date'].max().date()}")
