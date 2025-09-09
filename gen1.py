import pandas as pd
import numpy as np
from faker import Faker
from datetime import datetime, timedelta
import random
import os

# Initialize Faker and set seed for reproducibility
fake = Faker()
np.random.seed(42)
random.seed(42)

# Create output directory
os.makedirs('data1/raw', exist_ok=True)

# Generate Customers DataFrame (600 customers)
customers = []
for i in range(1, 601):
    signup_date = fake.date_between(start_date='-5y', end_date='-30d')
    customers.append({
        'customer_id': i,
        'name': fake.name(),
        'age': np.random.normal(45, 15),  # Mean age 45 with std 15
        'gender': random.choice(['M', 'F', 'O']),
        'location': fake.city() + ', ' + fake.state_abbr(),
        'signup_date': signup_date
    })
df_customers = pd.DataFrame(customers)
df_customers['age'] = df_customers['age'].clip(18, 80).round().astype(int)  # Ensure age between 18-80

# Generate Products DataFrame (300 products)
categories = {
    'Electronics': {'price_range': (50, 2000), 'products': ['Phone', 'Laptop', 'Headphones', 'Monitor']},
    'Fashion': {'price_range': (20, 500), 'products': ['Shirt', 'Dress', 'Shoes', 'Watch']},
    'Home': {'price_range': (30, 1500), 'products': ['Lamp', 'Chair', 'Table', 'Sofa']},
    'Beauty': {'price_range': (15, 300), 'products': ['Perfume', 'Cream', 'Makeup Kit', 'Serum']},
    'Sports': {'price_range': (25, 800), 'products': ['Dumbbells', 'Yoga Mat', 'Running Shoes', 'Jacket']}
}

products = []
product_id = 1
for category, details in categories.items():
    for product in details['products']:
        for variant in range(1, 16):  # 15 variants per product type
            price = round(np.random.uniform(*details['price_range']), 2)
            products.append({
                'product_id': product_id,
                'category': category,
                'product_name': f"{product} {variant}",
                'price': price
            })
            product_id += 1

df_products = pd.DataFrame(products)

# Generate Orders DataFrame (20,000 orders)
orders = []
order_date_range = pd.date_range(end=datetime.today(), periods=730, freq='D')  # Last 2 years

# Age-based purchase preferences
age_affinity = {
    'Electronics': (18, 35),
    'Fashion': (18, 40),
    'Beauty': (20, 45),
    'Sports': (18, 50),
    'Home': (30, 80)
}

# Create a list of customers with their age and preferred categories
customer_preferences = []
for customer in customers:
    age = customer['age']
    prefs = {}
    for category, (min_age, max_age) in age_affinity.items():
        # Calculate preference score based on age
        center = (min_age + max_age) / 2
        prefs[category] = np.exp(-0.5 * ((age - center) / 15)**2)
    customer_preferences.append((customer, prefs))

# Generate exactly 20,000 orders
for order_id in range(1, 20001):
    # Select a customer and their preferences
    customer, prefs = random.choice(customer_preferences)
    
    # Select a category based on preferences
    categories = list(prefs.keys())
    weights = [prefs[cat] for cat in categories]
    selected_category = random.choices(categories, weights=weights, k=1)[0]
    
    # Select a product from the chosen category
    category_products = [p for p in products if p['category'] == selected_category]
    product = random.choice(category_products)
    
    # Generate order date (after signup)
    order_date = fake.date_between(
        start_date=max(customer['signup_date'], order_date_range[0].date()),
        end_date=order_date_range[-1].date()
    )
    
    # Generate quantity (mostly 1-2 items)
    quantity = min(np.random.poisson(1.2) + 1, 5)  # Cap at 5 items
    total = quantity * product['price']
    
    orders.append({
        'order_id': order_id,
        'customer_id': customer['customer_id'],
        'product_id': product['product_id'],
        'order_date': order_date,
        'quantity': quantity,
        'total_amount': round(total, 2)
    })

df_orders = pd.DataFrame(orders)

# Save to CSV
df_customers.to_csv('data1/raw/customers.csv', index=False)
df_products.to_csv('data1/raw/products.csv', index=False)
df_orders.to_csv('data1/raw/orders.csv', index=False)

print("Dataset generation completed!")
print(f"Customers: {len(df_customers)} rows")
print(f"Products: {len(df_products)} rows")
print(f"Orders: {len(df_orders)} rows")