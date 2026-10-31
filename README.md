# RetailIQ — E-commerce Sales & Profitability Analytics

**An end-to-end business intelligence project** built with Python, Pandas, NumPy, PostgreSQL, SQL, Streamlit and Plotly. RetailIQ turns transaction-level Sample Superstore data into an interactive view of revenue, profitability, product mix, customer value and regional performance.

> **Dataset note:** Sample Superstore is fictional educational data supplied by Tableau. It is not real company or customer performance. All dashboard metrics are calculated from the downloaded source file; no results are hardcoded.

## Business problem
Retail leaders need to understand not only how much they sell, but where profit is generated or lost, which products and customer segments matter, how discounting relates to profitability, and how performance changes over time. RetailIQ provides a filterable analytics workflow for those questions.

## Features
- Data quality checks, duplicate handling, date parsing and derived analytical fields.
- Revenue, profit, distinct order count, average order value and profit margin KPIs.
- Product/category/sub-category performance, loss-making products and discount-profit analysis.
- Customer ranking, revenue contribution and repeat vs one-time customer classification.
- Regional/state performance and shipping-mode mix.
- Dynamic insight statements calculated from the active filters.
- PostgreSQL loading pipeline and 12 reusable business SQL queries.
- Premium dark Streamlit UI with Plotly charts and global date/region/category/segment/ship-mode filters.

## Dataset source and setup
Download **Superstore Sales** from the official [Tableau Public Sample Data page](https://public.tableau.com/app/learn/sample-data). Tableau describes this as fictitious sample sales and profit data. The official Tableau tutorial also points users to this sample source ([Tableau getting-started guide](https://help.tableau.com/current/guides/get-started-tutorial/en-us/get-started-tutorial-connect.htm)).

1. Download the CSV version if offered (or the Excel version).
2. Place the file in `data/raw/` (for example `data/raw/Sample - Superstore.csv`).
3. If using Excel, the workbook must contain an `Orders` sheet.
4. Do not commit the raw dataset unless its source terms permit redistribution.

## Architecture

```text
Raw Tableau sample data
        |
        v
src/data_loader.py -> src/data_cleaning.py -> data/processed/superstore_cleaned.csv
                                                   |
                          +------------------------+----------------------+
                          |                                               |
                          v                                               v
                 PostgreSQL loader                              Streamlit + Plotly
                 src/database.py                               dashboard/pages/
                          |
                          v
                  sql/business_queries.sql
```

## Project structure

```text
retailiq/
├── data/raw/                 # Downloaded source file (gitignored)
├── data/processed/           # Generated clean CSV (gitignored)
├── notebooks/exploratory_analysis.ipynb
├── src/                      # Loading, cleaning, analysis, database modules
├── sql/                      # PostgreSQL schema and business questions
├── dashboard/
│   ├── app.py
│   ├── common.py
│   ├── components/styles.py
│   └── pages/                 # Executive, Product, Customer, Regional
├── tests/test_analysis.py
├── requirements.txt
├── .env.example
└── README.md
```

## Run locally

Python 3.10+ is recommended.

```bash
# 1. Create and activate a virtual environment
python -m venv .venv
# macOS/Linux
source .venv/bin/activate
# Windows PowerShell: .venv\Scripts\Activate.ps1

# 2. Install packages
pip install -r requirements.txt

# 3. Put the downloaded dataset in data/raw/

# 4. Clean and validate the dataset
python -m src.prepare_data

# 5. Launch the dashboard (CSV mode; PostgreSQL is optional)
streamlit run dashboard/app.py
```

## PostgreSQL setup

Create a database named `retailiq` in PostgreSQL, then copy `.env.example` to `.env` and update `DATABASE_URL`:

```env
DATABASE_URL=postgresql+psycopg2://postgres:YOUR_PASSWORD@localhost:5432/retailiq
```

Load the cleaned data:

```bash
python -m src.load_database
```

The loader creates/replaces `superstore_orders` and adds indexes for order date and region. Run the analytical queries in `sql/business_queries.sql` using pgAdmin or `psql`. Keep `.env` private; never commit credentials.

## Data cleaning methodology
- Normalize field names and validate required analytical columns.
- Parse order and ship dates; coerce sales, profit, quantity and discount to numeric values.
- Remove exact duplicate rows only. Negative profit is valid business information and is retained.
- Exclude rows missing essential order/date/sales/profit values; report the number removed.
- Fill missing quantity/discount with zero and derive year, month, month-year, profit margin, shipping duration, order value, loss flag and discount band.
- The cleaning report prints row counts and missing-value counts so decisions are auditable.

## Key business questions
1. What are total revenue, profit, distinct orders, AOV and profit margin?
2. Which categories and products generate the most revenue and profit?
3. Which products have negative cumulative profit?
4. How does discount level relate to profit?
5. Which customer segments and customers contribute the most revenue?
6. What share of customers are repeat purchasers?
7. Which regions and states lead sales and profitability?
8. How do revenue and profit evolve monthly and yearly?

## Analytical definitions
- **Revenue:** sum of `sales` across transaction lines.
- **Profit:** sum of `profit` across transaction lines; losses remain negative.
- **Orders:** count of distinct `order_id`, never raw line count.
- **AOV:** total revenue divided by distinct orders.
- **Profit margin:** total profit divided by total revenue.
- **Repeat customer:** customer with more than one distinct order in the filtered dataset. This is a dataset-window definition, not a lifetime label.

## Limitations
- This is fictional sample data for learning and portfolio demonstration, not a forecast or real commercial benchmark.
- Discount/profit relationships are descriptive correlations and do not establish causality.
- The dashboard filters affect the selected analysis window; repeat-customer status is therefore relative to the active filters.
- The optional PostgreSQL loader replaces the target table when re-run. Back up any database table you need to preserve.
- Geographic maps are omitted because a state/city map requires geocoding or a dependable geographic reference layer.

## Screenshots
Add dashboard screenshots here after running the app, for example:

```markdown
![Executive overview](docs/screenshots/executive-overview.png)
```

## Validation
Run the unit tests with:

```bash
pytest -q
```

The tests cover cleaning/derived columns, negative-profit retention, distinct-order KPI calculation, repeat-customer classification and empty-state insights.
