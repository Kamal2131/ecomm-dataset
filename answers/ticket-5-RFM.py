import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# ------------------------
# Load Data
# ------------------------
customers = pd.read_csv("data/clean/customers_clean.csv", parse_dates=["signup_date"])
products = pd.read_csv("data/clean/products_clean.csv")
orders = pd.read_csv("data/clean/orders_clean.csv", parse_dates=["order_date"])

# Output directory for plots
PLOT_DIR = "data/plots"
os.makedirs(PLOT_DIR, exist_ok=True)

# ------------------------
# 1. Compute RFM Metrics
# ------------------------
latest_date = orders["order_date"].max()
rfm = orders.groupby("customer_id").agg({
    "order_date": lambda x: (latest_date - x.max()).days,
    "order_id": "count",
    "total_amount": "sum"
}).reset_index()

rfm.rename(columns={
    "order_date": "Recency",
    "order_id": "Frequency",
    "total_amount": "Monetary"
}, inplace=True)

# ------------------------
# 2. Score RFM (1–5 scale)
# ------------------------
rfm["R_Score"] = pd.qcut(rfm["Recency"], 5, labels=[5,4,3,2,1]).astype(int)
rfm["F_Score"] = pd.qcut(rfm["Frequency"].rank(method="first"), 5, labels=[1,2,3,4,5]).astype(int)
rfm["M_Score"] = pd.qcut(rfm["Monetary"], 5, labels=[1,2,3,4,5]).astype(int)

rfm["RFM_Segment"] = rfm[["R_Score","F_Score","M_Score"]].astype(str).agg("".join, axis=1)
rfm["RFM_Score"] = rfm[["R_Score","F_Score","M_Score"]].sum(axis=1)

# ------------------------
# 3. Assign Segment Labels
# ------------------------
def segment_customer(row):
    if row["RFM_Score"] >= 12:
        return "Champions"
    elif row["RFM_Score"] >= 9:
        return "Loyal"
    elif row["RFM_Score"] >= 6:
        return "Potential Loyalist"
    elif row["R_Score"] >= 4 and row["F_Score"] <= 2:
        return "New Customer"
    elif row["R_Score"] <= 2 and row["F_Score"] >= 3:
        return "At Risk"
    else:
        return "Hibernating"

rfm["Segment"] = rfm.apply(segment_customer, axis=1)

# ------------------------
# 4. Visualizations
# ------------------------
plt.figure(figsize=(8,5))
segment_counts = rfm["Segment"].value_counts()
segment_counts.plot(kind="bar")
plt.title("Customer Segments Distribution")
plt.ylabel("Number of Customers")
plt.tight_layout()
plt.savefig(os.path.join(PLOT_DIR, "rfm_segments_distribution.png"))
plt.close()

plt.figure(figsize=(8,6))
sns.boxplot(data=rfm, x="Segment", y="Monetary")
plt.title("Monetary Value by Segment")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig(os.path.join(PLOT_DIR, "rfm_monetary_by_segment.png"))
plt.close()

plt.figure(figsize=(8,6))
sns.scatterplot(data=rfm, x="Recency", y="Frequency", hue="Segment", alpha=0.7)
plt.title("Recency vs Frequency by Segment")
plt.tight_layout()
plt.savefig(os.path.join(PLOT_DIR, "rfm_recency_frequency.png"))
plt.close()

# ------------------------
# 5. Insights (Markdown)
# ------------------------
md_insights = f"""
# RFM Analysis Insights

## Segment Distribution
- Champions: {segment_counts.get('Champions',0)} customers — best customers, buy often and recently.
- Loyal: {segment_counts.get('Loyal',0)} customers — frequent buyers, stable revenue.
- Potential Loyalist: {segment_counts.get('Potential Loyalist',0)} customers — could become loyal with engagement.
- New Customers: {segment_counts.get('New Customer',0)} customers — acquired recently, nurture needed.
- At Risk: {segment_counts.get('At Risk',0)} customers — haven’t purchased recently but were active.
- Hibernating: {segment_counts.get('Hibernating',0)} customers — inactive, low value.

## Behavior Differences
- Champions and Loyal customers have **highest monetary value**.
- At Risk customers show good past frequency but poor recency.
- Hibernating segment shows low spend and long inactivity.

## Business Takeaways
- **Champions** → reward loyalty, upsell premium products.
- **Loyal** → maintain engagement with personalized offers.
- **Potential Loyalists** → nurture via discounts or bundles.
- **New Customers** → welcome campaigns, onboarding emails.
- **At Risk** → win-back campaigns.
- **Hibernating** → low ROI, deprioritize.
"""

print(md_insights)
print(" RFM analysis complete. Segments created and plots saved in data/plots/")