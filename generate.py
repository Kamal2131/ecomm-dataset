import os
import random
import numpy as np
import pandas as pd
from faker import Faker
from datetime import datetime, timedelta

# Configurations
OUTPUT_DIR = "data/raw"
N_CUSTOMERS = 500
N_PRODUCTS = 200
N_ORDERS = 20000

# Initialize Faker
faker = Faker()

# Ensure output directory exists
os.makedirs(OUTPUT_DIR, exist_ok=True)

# --- Generate Customers ---
def generate_customers(n_customers):
    """ <h2> For Generating the Fake Customer <h2>
    
    <p> "customer_id": i,
            "name": faker.name(),
            "age": random.randint(18, 70),
            "gender": gender,
            "location": faker.city(),
            "signup_date": faker.date_between(start_date="-3y", end_date="today")
    
    <br> This fields will be generating <br>
    
    <p>
    
    """
    customers = []
    for i in range(1, n_customers + 1):
        gender = random.choice(["Male", "Female", "Other"])
        customers.append({
            "customer_id": i,
            "name": faker.name(),
            "age": random.randint(18, 70),
            "gender": gender,
            "location": faker.city(),
            "signup_date": faker.date_between(start_date="-3y", end_date="today")
        })
    return pd.DataFrame(customers)

# --- Generate Products ---
def generate_products(n_products):
    categories = ["Electronics", "Fashion", "Home", "Sports", "Books", "Toys"]
    products = []
    for i in range(1, n_products + 1):
        category = random.choice(categories)
        price = round(random.uniform(5, 500), 2)
        products.append({
            "product_id": i,
            "category": category,
            "product_name": f"{category} - {faker.word().capitalize()}",
            "price": price
        })
    return pd.DataFrame(products)

# --- Generate Orders ---
def generate_orders(n_orders, customers_df, products_df):
    orders = []
    customer_ids = customers_df["customer_id"].tolist()
    product_ids = products_df["product_id"].tolist()

    for i in range(1, n_orders + 1):
        customer_id = random.choice(customer_ids)
        product_id = random.choice(product_ids)
        product_price = products_df.loc[products_df["product_id"] == product_id, "price"].values[0]

        # More realistic order date distribution (last 2 years)
        order_date = faker.date_between(start_date="-2y", end_date="today")

        # Quantity with skew (most orders are 1–3 items, few are bulk)
        quantity = np.random.choice([1, 2, 3, 4, 5, 10], p=[0.5, 0.25, 0.15, 0.05, 0.03, 0.02])

        orders.append({
            "order_id": i,
            "customer_id": customer_id,
            "product_id": product_id,
            "order_date": order_date,
            "quantity": quantity,
            "total_amount": round(product_price * quantity, 2)
        })

    return pd.DataFrame(orders)

# --- Main Execution ---
if __name__ == "__main__":
    print("Generating synthetic dataset...")

    customers_df = generate_customers(N_CUSTOMERS)
    products_df = generate_products(N_PRODUCTS)
    orders_df = generate_orders(N_ORDERS, customers_df, products_df)

    # Save to CSV
    customers_df.to_csv(f"{OUTPUT_DIR}/customers.csv", index=False)
    products_df.to_csv(f"{OUTPUT_DIR}/products.csv", index=False)
    orders_df.to_csv(f"{OUTPUT_DIR}/orders.csv", index=False)

    print(f"Data generated in {OUTPUT_DIR}/")
    print(f"- customers.csv ({len(customers_df)} rows)")
    print(f"- products.csv ({len(products_df)} rows)")
    print(f"- orders.csv ({len(orders_df)} rows)")
