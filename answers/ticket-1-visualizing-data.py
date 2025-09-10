import pandas as pd
import numpy as np

# ------------------------
# 1. Data Ingestion
# ------------------------
customers = pd.read_csv("data/raw/customers.csv", parse_dates=["signup_date"])
products = pd.read_csv("data/raw/products.csv")
orders = pd.read_csv("data/raw/orders.csv", parse_dates=["order_date"])

# ------------------------
# 2. Initial Understanding
# ------------------------
print("--- Customers Info ---")
print(customers.info())
print(customers.head())

print("--- Products Info ---")
print(products.info())
print(products.head())

print("--- Orders Info ---")
print(orders.info())
print(orders.head())

# ------------------------
# 3. Handle Missing Values
# ------------------------
# Drop rows with critical nulls (e.g., customer_id, product_id, order_date)
orders = orders.dropna(subset=["customer_id", "product_id", "order_date"])

# Impute missing ages with median
if customers["age"].isnull().any():
    customers["age"].fillna(customers["age"].median(), inplace=True)

# Flag missing locations
customers["location"] = customers["location"].fillna("Unknown")

# ------------------------
# 4. Normalize Categorical Values
# ------------------------
# Example: Normalize state/location naming (CA vs California)
customers["location"] = customers["location"].replace({
    "CA": "California",
    "NY": "New York",
    "TX": "Texas"
})

# Standardize gender values
customers["gender"] = customers["gender"].str.strip().str.title()

# ------------------------
# 5. Fix Incorrect Data Types
# ------------------------
# Ensure numeric fields are correct type
products["price"] = pd.to_numeric(products["price"], errors="coerce")
orders["quantity"] = pd.to_numeric(orders["quantity"], errors="coerce").fillna(1).astype(int)
orders["total_amount"] = pd.to_numeric(orders["total_amount"], errors="coerce")

# ------------------------
# 6. Remove Duplicates
# ------------------------
customers = customers.drop_duplicates(subset="customer_id")
products = products.drop_duplicates(subset="product_id")
orders = orders.drop_duplicates(subset="order_id")

# ------------------------
# 7. Create Data Dictionary
# ------------------------
data_dict = {
    "customers": {
        "customer_id": "Unique ID for customer",
        "name": "Customer full name",
        "age": "Customer age (years)",
        "gender": "Customer gender (Male/Female/Other)",
        "location": "Customer location (city/state)",
        "signup_date": "Date customer signed up"
    },
    "products": {
        "product_id": "Unique ID for product",
        "category": "Product category",
        "product_name": "Name of product",
        "price": "Unit price of product ($)"
    },
    "orders": {
        "order_id": "Unique ID for order",
        "customer_id": "ID of purchasing customer",
        "product_id": "ID of purchased product",
        "order_date": "Date of order",
        "quantity": "Units purchased",
        "total_amount": "Total transaction amount ($)"
    }
}

# ------------------------
# 8. Basic Summary Statistics
# ------------------------
def summarize(df, name):
    print(f"\n--- {name.upper()} SUMMARY ---")
    print(f"Shape: {df.shape}")
    print(df.isnull().sum())
    print(df.describe(include="all"))

summarize(customers, "customers")
summarize(products, "products")
summarize(orders, "orders")

# ------------------------
# Save Cleaned Data
# ------------------------
customers.to_csv("data/clean/customers_clean.csv", index=False)
products.to_csv("data/clean/products_clean.csv", index=False)
orders.to_csv("data/clean/orders_clean.csv", index=False)

print("Data cleaning complete. Cleaned files saved to data/clean/.")
print("Data dictionary:")
for table, fields in data_dict.items():
    print(f"\nTable: {table}")
    for col, desc in fields.items():
        print(f"- {col}: {desc}")