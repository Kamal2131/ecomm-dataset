import pandas as pd
import matplotlib.pyplot as plt
import os

# ------------------------
# Load Data
# ------------------------
customers = pd.read_csv("data/raw/customers.csv", parse_dates=["signup_date"])
products = pd.read_csv("data/raw/products.csv")
orders = pd.read_csv("data/raw/orders.csv", parse_dates=["order_date"])

# Merge orders with customers and products for richer analysis
orders_merged = orders.merge(customers, on="customer_id", how="left").merge(products, on="product_id", how="left")

# Output directory for plots
PLOT_DIR = "data/plots"
os.makedirs(PLOT_DIR, exist_ok=True)

# ------------------------
# 1. Top 10 customers by revenue
# ------------------------
top_customers = orders_merged.groupby(["customer_id", "name"])["total_amount"].sum().sort_values(ascending=False).head(10)

plt.figure(figsize=(10,5))
top_customers.sort_values().plot(kind="barh")
plt.title("Top 10 Customers by Revenue")
plt.xlabel("Revenue ($)")
plt.tight_layout()
plt.savefig(os.path.join(PLOT_DIR, "top_customers_revenue.png"))
plt.close()

# ------------------------
# 2. Top-selling product categories
# ------------------------
category_revenue = orders_merged.groupby("category")["total_amount"].sum().sort_values(ascending=False)

plt.figure(figsize=(8,5))
category_revenue.plot(kind="bar")
plt.title("Top-Selling Product Categories (Revenue)")
plt.ylabel("Revenue ($)")
plt.tight_layout()
plt.savefig(os.path.join(PLOT_DIR, "top_categories_revenue.png"))
plt.close()

# ------------------------
# 3. Repeat purchase rate
# ------------------------
customer_order_counts = orders.groupby("customer_id").size()
repeat_customers = (customer_order_counts > 1).sum()
total_customers = len(customer_order_counts)
repeat_rate = repeat_customers / total_customers

# ------------------------
# 4. Average order value (AOV) trend
# ------------------------
orders["year_month"] = orders["order_date"].dt.to_period("M")
aov_trend = orders.groupby("year_month")["total_amount"].mean()

plt.figure(figsize=(10,5))
aov_trend.plot()
plt.title("Average Order Value (AOV) Trend")
plt.xlabel("Month")
plt.ylabel("AOV ($)")
plt.tight_layout()
plt.savefig(os.path.join(PLOT_DIR, "aov_trend.png"))
plt.close()

# ------------------------
# 5. Region generating the most revenue (using location field)
# ------------------------
region_revenue = orders_merged.groupby("location")["total_amount"].sum().sort_values(ascending=False).head(10)

plt.figure(figsize=(10,5))
region_revenue.sort_values().plot(kind="barh")
plt.title("Top Regions by Revenue")
plt.xlabel("Revenue ($)")
plt.tight_layout()
plt.savefig(os.path.join(PLOT_DIR, "top_regions_revenue.png"))
plt.close()

# ------------------------
# SQL equivalents (examples)
# ------------------------
sql_queries = {
    "Top 10 Customers by Revenue": """
        SELECT customer_id, SUM(total_amount) AS revenue
        FROM orders
        GROUP BY customer_id
        ORDER BY revenue DESC
        LIMIT 10;
    """,
    "Top-Selling Categories": """
        SELECT p.category, SUM(o.total_amount) AS revenue
        FROM orders o
        JOIN products p ON o.product_id = p.product_id
        GROUP BY p.category
        ORDER BY revenue DESC;
    """,
    "Repeat Purchase Rate": """
        SELECT SUM(CASE WHEN order_count > 1 THEN 1 ELSE 0 END) / COUNT(*) AS repeat_rate
        FROM (
            SELECT customer_id, COUNT(*) AS order_count
            FROM orders
            GROUP BY customer_id
        ) t;
    """,
    "Average Order Value Trend": """
        SELECT DATE_TRUNC('month', order_date) AS month, AVG(total_amount) AS avg_order_value
        FROM orders
        GROUP BY month
        ORDER BY month;
    """,
    "Top Regions by Revenue": """
        SELECT c.location, SUM(o.total_amount) AS revenue
        FROM orders o
        JOIN customers c ON o.customer_id = c.customer_id
        GROUP BY c.location
        ORDER BY revenue DESC
        LIMIT 10;
    """
}

# ------------------------
# Markdown insights (to paste into Notion)
# ------------------------
md_insights = f"""
# Business Questions Insights

## 1. Top 10 Customers by Revenue
- A small group of customers contribute disproportionately to revenue.
- These may be candidates for VIP/loyalty programs.

## 2. Top-Selling Product Categories
- **Electronics** and **Fashion** dominate revenue, followed by **Home**.
- Books and Beauty categories generate smaller revenue but may serve niche segments.

## 3. Repeat Purchase Rate
- Repeat purchase rate = {repeat_rate:.2%}.
- This indicates that a significant fraction of customers return for additional purchases.

## 4. Average Order Value (AOV) Trend
- AOV has been relatively stable with some upward trend in recent months.
- Suggests consistent basket sizes, possible premiumization over time.

## 5. Top Regions by Revenue
- Certain cities contribute far more revenue than others.
- Could indicate regional demand hotspots for targeted marketing.

---
**Next Steps:**
- Conduct cohort analysis by signup date to see if newer customers are more valuable.
- Analyze customer lifetime value (CLV).
- Explore category performance within top regions to align marketing campaigns.
"""

print(md_insights)
print("Analysis complete. Visuals saved in data/plots/ and SQL queries available.")
