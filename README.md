# RetailIQ — E-commerce Sales & Profitability Analytics

**RetailIQ** is an end-to-end business intelligence project built using Python, Pandas, NumPy, PostgreSQL, SQL, Streamlit and Plotly. It transforms transaction-level Sample Superstore data into an interactive analytics dashboard for understanding revenue, profitability, product performance, customer behavior and regional trends.

> **Dataset Note:** This project uses Tableau's fictional Sample Superstore dataset for educational and portfolio purposes. All dashboard metrics are calculated dynamically from the source data; no results are hardcoded.

---

## Business Problem

Retail businesses need to understand more than just their total sales. They need insights into:

- Which products and categories generate the highest revenue and profit?
- Which products contribute to business losses?
- How do discounts affect profitability?
- Which customer segments generate the most revenue?
- Which regions perform best?
- How do sales and profits change over time?

RetailIQ addresses these questions through an interactive business intelligence dashboard backed by Python analytics and SQL queries.

## Key Features

- **Business KPIs:** Revenue, profit, distinct orders, average order value and profit margin.
- **Product Analytics:** Category performance, top-selling products, loss-making products and discount-profit relationships.
- **Customer Analytics:** Customer segmentation, revenue contribution, purchasing patterns and repeat customer analysis.
- **Regional Analytics:** Regional and state-level sales, profitability and shipping performance.
- **Time-Series Analysis:** Monthly revenue trends and year-over-year sales growth.
- **Dynamic Insights:** Automatically generated business insights based on active dashboard filters.
- **SQL Analytics:** 12 reusable PostgreSQL business queries.
- **Interactive Dashboard:** Streamlit interface with Plotly visualizations and global filters for date, region, category, segment and shipping mode.
- **Data Quality:** Data cleaning, duplicate handling, missing-value checks and derived analytical metrics.

## Dashboard Preview

RetailIQ provides four interactive analytical views:

### 1. Executive Overview

Business KPIs, monthly revenue trends, category performance and key business insights.

![Executive Overview](docs/screenshots/executive-overview.png)

### 2. Product Analysis

Product and category performance, top-selling products and profitability analysis.

![Product Analysis](docs/screenshots/product-analysis.png)

### 3. Customer Analytics

Customer segmentation, purchasing patterns and customer revenue contribution.

![Customer Analytics](docs/screenshots/customer-analysis.png)

### 4. Regional Analysis

Regional sales, profitability and shipping performance.

![Regional Analysis](docs/screenshots/regional-analysis.png)

---

## Tech Stack

| Category | Technologies |
|---|---|
| Programming | Python |
| Data Analysis | Pandas, NumPy |
| Database | PostgreSQL |
| Query Language | SQL |
| Dashboard | Streamlit |
| Visualization | Plotly |
| Testing | Pytest |
| Version Control | Git, GitHub |

## Dataset Source

The project uses the **Sample Superstore** dataset provided by Tableau.

- [Tableau Public Sample Data](https://public.tableau.com/app/learn/sample-data)
- [Tableau Getting Started Guide](https://help.tableau.com/current/guides/get-started-tutorial/en-us/get-started-tutorial-connect.htm)

### Dataset Setup

1. Download the Sample Superstore dataset.
2. Place the downloaded file inside `data/raw/`.
3. For Excel files, ensure the workbook contains an `Orders` sheet.
4. The raw dataset is excluded from Git tracking.

## Project Architecture

```text
                 Sample Superstore Dataset
                            |
                            v
                    Data Loading
                  src/data_loader.py
                            |
                            v
                    Data Cleaning
                 src/data_cleaning.py
                            |
                            v
                  Processed CSV Data
                            |
                +-----------+-----------+
                |                       |
                v                       v
         PostgreSQL Database      Streamlit Dashboard
          src/database.py          dashboard/app.py
                |                       |
                v                       v
         SQL Business Queries     Plotly Visualizations
          sql/business_queries.sql
```

## Project Structure

```text
retailiq/
│
├── dashboard/
│   ├── app.py
│   ├── common.py
│   ├── components/
│   │   └── styles.py
│   └── pages/
│       ├── 1_Executive_Overview.py
│       ├── 2_Product_Analysis.py
│       ├── 3_Customer_Analytics.py
│       └── 4_Regional_Analysis.py
│
├── data/
│   ├── raw/
│   └── processed/
│
├── docs/
│   └── screenshots/
│       ├── executive-overview.png
│       ├── product-analysis.png
│       ├── customer-analysis.png
│       └── regional-analysis.png
│
├── notebooks/
│   └── exploratory_analysis.ipynb
│
├── reports/
│
├── sql/
│   ├── schema.sql
│   └── business_queries.sql
│
├── src/
│   ├── data_loader.py
│   ├── data_cleaning.py
│   ├── analysis.py
│   ├── database.py
│   ├── data_loader.py
│   ├── prepare_data.py
│   ├── load_database.py
│   ├── run_eda.py
│   ├── sql_queries.py
│   └── visualizations.py
│
├── tests/
│   └── test_analysis.py
│
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md
```

## Installation & Setup

### Prerequisites

- Python 3.10+
- Git
- PostgreSQL (optional, for database integration)

### 1. Clone the Repository

```bash
git clone https://github.com/pawan646435/RetailIQ.git

cd RetailIQ
```

### 2. Create a Virtual Environment

```bash
python -m venv .venv
```

Activate it:

**macOS/Linux:**

```bash
source .venv/bin/activate
```

**Windows PowerShell:**

```powershell
.venv\Scripts\Activate.ps1
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Add the Dataset

Download the Sample Superstore dataset and place it inside:

```text
data/raw/
```

### 5. Prepare the Data

Run the data preparation pipeline:

```bash
python -m src.prepare_data
```

This cleans the dataset, validates analytical fields and saves the processed CSV inside `data/processed/`.

### 6. Launch the Dashboard

```bash
streamlit run dashboard/app.py
```

The dashboard will open in your browser, typically at:

`http://localhost:8501`

**Note:** The dashboard supports CSV-based analysis. PostgreSQL integration is optional.

## PostgreSQL Integration

### 1. Create a Database

Create a PostgreSQL database named:

```sql
CREATE DATABASE retailiq;
```

### 2. Configure Environment Variables

Copy `.env.example` to `.env` and configure your database connection:

```env
DATABASE_URL=postgresql+psycopg2://postgres:YOUR_PASSWORD@localhost:5432/retailiq
```

Replace `YOUR_PASSWORD` with your PostgreSQL password.

### 3. Load Processed Data

After preparing the dataset, run:

```bash
python -m src.load_database
```

The loader creates the `superstore_orders` table and adds indexes for order date and region.

### 4. Execute SQL Queries

Run the analytical queries from:

```text
sql/business_queries.sql
```

You can execute them using pgAdmin or the PostgreSQL command-line interface (`psql`).

> Keep your `.env` file private. Never commit database credentials to GitHub.

## Data Cleaning & Preparation

The data preparation pipeline performs the following operations:

- Normalizes column names and validates required analytical fields.
- Parses order and shipping dates.
- Converts sales, profit, quantity and discount into appropriate numeric formats.
- Removes exact duplicate records.
- Handles missing essential values and reports removed records.
- Retains negative profit values to preserve genuine loss-making transactions.
- Handles missing quantity and discount values.
- Creates derived fields such as year, month, month-year, profit margin, shipping duration, order value, loss flag and discount band.

A cleaning report provides row counts and missing-value statistics to make the process transparent.

## SQL Business Analysis

RetailIQ includes 12 reusable SQL business queries covering:

1. Total revenue, profit and distinct orders.
2. Monthly revenue and profit trends.
3. Year-over-year sales growth.
4. Top 10 products by revenue.
5. Most profitable product categories.
6. Sales by customer segment.
7. Regional sales and profitability.
8. Top 10 customers by revenue.
9. Repeat versus one-time customers.
10. Discount versus profitability analysis.
11. Loss-making products.
12. Average order value.

These queries are available in `sql/business_queries.sql`.

## Key Analytical Definitions

| Metric | Definition |
|---|---|
| Revenue | Sum of sales across transaction lines |
| Profit | Sum of profit across transaction lines |
| Orders | Count of distinct order IDs |
| Average Order Value | Total revenue / distinct orders |
| Profit Margin | Total profit / total revenue |
| Repeat Customer | Customer with more than one distinct order |

Repeat customer classification is calculated within the currently selected dataset window and dashboard filters.

## Testing & Validation

Unit tests are implemented using Pytest.

Run the test suite:

```bash
python -m pytest -q
```

The tests cover:

- Data cleaning and derived columns.
- Retention of negative profit values.
- Distinct-order KPI calculations.
- Repeat customer classification.
- Empty-state business insights.

## Limitations

- Sample Superstore is fictional educational data, not actual commercial performance.
- Discount-profit relationships are descriptive and do not establish causation.
- Repeat customer status depends on the active dashboard filters.
- The optional PostgreSQL loader replaces the target table when rerun. Back up any existing data you need to preserve.
- Geographic maps are omitted because reliable city/state geocoding requires an additional geographic reference layer.

---

## Author

**Pawan Kumar**

B.Tech Computer Science & Engineering

- [GitHub](https://github.com/pawan646435)
- [LinkedIn](https://www.linkedin.com/in/pawan646435/)

---

*Built as a hands-on business intelligence and data analytics portfolio project.*