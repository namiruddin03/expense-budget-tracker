# Personal Expense Tracker and Budget Dashboard

This is a Data Analytics project built to track and analyse 12 months of personal expenses in INR. The project covers data generation, data cleaning and reconciliation in Python, database modelling and budget checking in Oracle SQL / PL/SQL, and an interactive dashboard in Power BI.

---

## Problem Statement

When we make daily payments using UPI, credit cards, debit cards, and net banking, it becomes hard to track actual monthly spending properly. Common issues in raw transaction data include:

- **Missing Categories:** Many online transactions (like Swiggy, Zomato, Uber, Jio, Amazon) appear without a proper category or are marked as "Uncategorised".
- **Refund Entries:** Refunds and order cancellations need to be subtracted from total spending instead of being ignored or added as regular expenses.
- **Month-End Dates:** Late-night transactions around the end of a month (for example, `2025-01-31 23:55:00` and `2025-02-01 00:05:00`) can end up in the wrong month if timestamps are not handled carefully.

This project solves these problems by cleaning the raw CSV data in Python, checking monthly totals against the source file, flagging budget breaches in Oracle PL/SQL, and showing the final insights in Power BI.

---

## Tools Used

- **Python** (Pandas, OpenPyXL, Matplotlib, python-docx) – for data generation, cleaning, categorisation, reconciliation, and reports
- **Oracle SQL & PL/SQL** (Oracle Live SQL) – for creating star-schema tables, views, queries, and budget breach alerts
- **Power BI Desktop** – for building the interactive expense and budget dashboard

---

## Folder Structure

```text
expense-budget-tracker/
│
├── data/
│   ├── raw_expenses.csv                # 428 raw expense records (12 months)
│   ├── cleaned_expenses.csv            # Cleaned and reconciled dataset
│   └── reconciliation_dq_report.xlsx   # Excel report with monthly reconciliation & data quality metrics
│
├── scripts/
│   ├── generate_data.py                # Creates the 12-month sample dataset
│   ├── clean_and_reconcile.py          # Cleans data, fills missing categories, nets refunds, checks totals
│   ├── generate_schema_diagram.py      # Creates the star-schema diagram image
│   ├── build_sql_load.py               # Prepares the Oracle INSERT script
│   └── generate_docx_report.py         # Builds the Word project report
│
├── sql/
│   ├── 01_ddl.sql                      # Creates DIM_CATEGORY, DIM_BUDGET, FACT_EXPENSES, BUDGET_ALERTS
│   ├── 02_load.sql                     # Loads 8 categories, 16 budgets, and 61 sample transactions
│   └── 03_views_and_plsql.sql          # Analytical view, queries, and PL/SQL budget check procedure
│
├── docs/
│   ├── star_schema.png                 # Star-schema diagram
│   └── Personal_Expense_Project_Report.docx
│
├── dashboard/
│   ├── Personal_Expense_Dashboard.pbix # Power BI dashboard file
│   └── PowerBI_Dashboard.pdf           # PDF export of the dashboard
│
└── README.md
# expense-budget-tracker
