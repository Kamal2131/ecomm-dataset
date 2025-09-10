# 📊 E-commerce Analytics Project

## 📌 Overview

<details>
<summary>Click to see what this project covers</summary>

This project simulates an **end-to-end data analytics pipeline** for an e-commerce company. It covers:

1. **Synthetic Data Generation** (customers, products, orders)
2. **Data Ingestion & Cleaning**
3. **Exploratory Data Analysis (EDA)**
4. **Business Questions Answered with SQL/Pandas**
5. **Customer Segmentation with RFM Analysis**
6. **Visualization (Python + Power BI)**

The goal is to showcase a real-world analytics workflow with Python and Pandas, including data preparation, insights, and visualization.
</details>

---

## ⚙️ Setup Instructions

<details>
<summary>Prerequisites & Installation</summary>

### Prerequisites

* Python **3.8+**
* Recommended: Virtual environment (e.g. `venv` or `uv`)

### Installation

Clone this repo:

```bash
git clone https://github.com/yourusername/ecommerce-analytics.git
cd ecommerce-analytics
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Alternatively, if you are using `uv`:

```bash
uv sync
```
</details>

<details>
<summary>Project Structure</summary>

```
answers/
   ticket-0-generate-data.py    # Generate synthetic datasets
   ticket-1-visualizing-data.py # Basic visualizations
   ticket-2-3-eda.py            # Exploratory Data Analysis
   ticket-4-business.py         # Business questions & SQL/Pandas queries
   ticket-5-RFM.py              # RFM segmentation analysis

data/
   raw/    # Generated raw data (customers, products, orders)
   clean/  # Cleaned datasets
   plots/  # Saved charts/visualizations

PowerBi/                        # Dashboards and PBIX files

all-tickets.ipynb               # Combined Jupyter Notebook version of all scripts
main.py                         # Optional entrypoint script
pyproject.toml                  # Project configuration
requirements.txt                # Project dependencies
README.md                       # Project documentation
```

Run a specific script, e.g.:

```bash
python answers/ticket-2-3-eda.py
```
</details>

---

## 🔄 Workflow

<details>
<summary>1. Synthetic Data Generation</summary>

* Generates **customers**, **products**, and **orders** datasets.
* Ensures realistic patterns: product preferences by age, order frequency distribution, seasonality.
* Outputs to `data/raw/`.
</details>

<details>
<summary>2. Data Cleaning</summary>

* Handles missing values (drop, impute, or flag).
* Normalizes categorical values (e.g., gender, locations).
* Fixes incorrect data types (dates, numeric fields).
* Removes duplicates.
* Produces a **data dictionary** and **summary statistics**.
* Outputs to `data/clean/`.
</details>

<details>
<summary>3. Exploratory Data Analysis (EDA)</summary>

* **Univariate & bivariate analysis** with 5+ visualizations:
  * Order amounts distribution
  * Order frequency per customer
  * Customer demographics (age, gender)
  * Product category performance
  * Seasonality (monthly revenue)
* Insights documented in Markdown / Notion.
</details>

<details>
<summary>4. Business Questions</summary>

Answered using **Pandas & SQL equivalents**:

* Who are the top 10 customers by revenue?
* What are the top-selling categories?
* What's the repeat purchase rate?
* What's the AOV (Average Order Value) trend?
* Which region generates the most revenue?
</details>

<details>
<summary>5. RFM Segmentation</summary>

* Calculates **Recency, Frequency, Monetary** metrics.
* Scores customers (1–5 scale).
* Assigns segments: *Champions, Loyal, Potential Loyalist, New, At Risk, Hibernating*.
* Visualizations:
  * Segment distribution
  * Monetary value by segment
  * Recency vs Frequency scatterplot
* Key business takeaways documented.
</details>

<details>
<summary>6. Visualization (Power BI)</summary>

* Data exported for dashboarding in **Power BI**.
* Reports include customer segmentation, revenue trends, and top-performing categories.
</details>

---

<details>
<summary>📂 Outputs</summary>

* **Cleaned datasets** → `data/clean/`
* **EDA & business visuals** → `data/plots/`
* **RFM segments table** → `data/clean/rfm_segments.csv`
* **Dashboards** → `PowerBi/`
</details>

<details>
<summary>🚀 Business Impact</summary>

* Identify high-value customers (Champions, Loyal).
* Detect churn risk (At Risk, Hibernating).
* Understand product & region performance.
* Support data-driven marketing and retention strategies.
</details>

