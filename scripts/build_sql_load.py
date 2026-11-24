"""
Builds sql/02_load.sql containing seed data for Oracle Database / Live SQL:
- DIM_CATEGORY (8 rows)
- DIM_BUDGET (16 rows)
- FACT_EXPENSES (61 rows from cleaned_expenses.csv)
"""

import pandas as pd

def build_load_script(cleaned_path="data/cleaned_expenses.csv", output_path="sql/02_load.sql"):
    df = pd.read_csv(cleaned_path)
    subset = df.iloc[0:61].copy()

    cat_map = {
        'Food & Dining': 1,
        'Groceries': 2,
        'Utilities & Bills': 3,
        'Transportation': 4,
        'Shopping': 5,
        'Entertainment & Leisure': 6,
        'Healthcare & Wellness': 7,
        'Housing & Maintenance': 8
    }

    lines = []
    lines.append('-- ==============================================================================')
    lines.append('-- PERSONAL EXPENSE TRACKER & BUDGET DASHBOARD')
    lines.append('-- Script 02: Seed Data Load for Oracle Database / Oracle Live SQL')
    lines.append(f'-- Loads DIM_CATEGORY (8 rows), DIM_BUDGET (16 rows), FACT_EXPENSES ({len(subset)} rows)')
    lines.append('-- ==============================================================================\n')

    lines.append('-- ------------------------------------------------------------------------------')
    lines.append('-- 1. SEED DIM_CATEGORY (8 Standardised Categories)')
    lines.append('-- ------------------------------------------------------------------------------')
    categories_data = [
        (1, 'Food & Dining', 'Essential', 'Restaurants, cloud kitchens, fast food, coffee & daily dining', 1),
        (2, 'Groceries', 'Essential', 'Supermarket, dairy, fresh vegetables & household staples', 1),
        (3, 'Utilities & Bills', 'Essential', 'Electricity, water, piped gas, broadband & phone recharges', 1),
        (4, 'Transportation', 'Essential', 'Cab rides, metro, fuel, tolls and vehicle commuting', 1),
        (5, 'Shopping', 'Discretionary', 'Apparel, footwear, electronics, lifestyle and eCommerce', 1),
        (6, 'Entertainment & Leisure', 'Discretionary', 'OTT subscriptions, movies, theater and leisure outings', 1),
        (7, 'Healthcare & Wellness', 'Essential', 'Pharmacy, doctor consultation, wellness and medical supplies', 1),
        (8, 'Housing & Maintenance', 'Essential', 'Apartment rent, domestic help and society maintenance', 1)
    ]

    for cid, cname, cgrp, cdesc, act in categories_data:
        lines.append(f"INSERT INTO DIM_CATEGORY (CATEGORY_ID, CATEGORY_NAME, CATEGORY_GROUP, DESCRIPTION, IS_ACTIVE) VALUES ({cid}, '{cname}', '{cgrp}', '{cdesc}', {act});")

    lines.append('\n-- ------------------------------------------------------------------------------')
    lines.append('-- 2. SEED DIM_BUDGET (Monthly Target Allocations for 2025-01 and 2025-02)')
    lines.append('-- Calibrated with real breaches: 2025-01 Food & Dining, Shopping, Entertainment; 2025-02 Shopping, Healthcare')
    lines.append('-- ------------------------------------------------------------------------------')

    budgets_data = [
        # 2025-01 Budgets
        (1, '2025-01', 1, 8500.00),   # Food & Dining: Spend 10,743.60 -> Breach of 2,243.60 (+26.40% -> CRITICAL)
        (2, '2025-01', 2, 35000.00),  # Groceries: Spend 32,845.98 -> Within budget (93.85%)
        (3, '2025-01', 3, 8000.00),   # Utilities & Bills: Spend 7,189.18 -> Within budget (89.86%)
        (4, '2025-01', 4, 5000.00),   # Transportation: Spend 4,424.66 -> Within budget (88.49%)
        (5, '2025-01', 5, 8000.00),   # Shopping: Spend 9,793.93 -> Breach of 1,793.93 (+22.42% -> CRITICAL)
        (6, '2025-01', 6, 1500.00),   # Entertainment & Leisure: Spend 1,640.41 -> Breach of 140.41 (+9.36% -> WARNING)
        (7, '2025-01', 7, 3000.00),   # Healthcare & Wellness: Spend 2,725.01 -> Within budget (90.83%)
        (8, '2025-01', 8, 30000.00),  # Housing & Maintenance: Spend 0.00 -> Within budget
        
        # 2025-02 Budgets
        (9,  '2025-02', 1, 4000.00),   # Food & Dining: Spend 3,007.90 -> Within budget (75.20%)
        (10, '2025-02', 2, 15000.00),  # Groceries: Spend 13,342.44 -> Within budget (88.95%)
        (11, '2025-02', 3, 4000.00),   # Utilities & Bills: Spend 3,115.90 -> Within budget (77.90%)
        (12, '2025-02', 4, 2000.00),   # Transportation: Spend 1,083.27 -> Within budget (54.16%)
        (13, '2025-02', 5, 15000.00),  # Shopping: Spend 24,403.71 -> Breach of 9,403.71 (+62.69% -> CRITICAL)
        (14, '2025-02', 6, 1000.00),   # Entertainment & Leisure: Spend 687.10 -> Within budget (68.71%)
        (15, '2025-02', 7, 3000.00),   # Healthcare & Wellness: Spend 3,074.43 -> Breach of 74.43 (+2.48% -> WARNING)
        (16, '2025-02', 8, 30000.00)   # Housing & Maintenance: Spend 0.00 -> Within budget
    ]

    for bid, ym, cid, b_amt in budgets_data:
        lines.append(f"INSERT INTO DIM_BUDGET (BUDGET_ID, YEAR_MONTH, CATEGORY_ID, BUDGET_AMOUNT, CREATED_DATE) VALUES ({bid}, '{ym}', {cid}, {b_amt:.2f}, TO_DATE('2025-01-01', 'YYYY-MM-DD'));")

    lines.append('\n-- ------------------------------------------------------------------------------')
    lines.append(f'-- 3. SEED FACT_EXPENSES ({len(subset)} Transactions covering 2025-01 and 2025-02)')
    lines.append('-- Explicitly captures:')
    lines.append('--  a) Auto-categorised rows (4 rows)')
    lines.append('--  b) Refund entries (TXN10023 Amazon -1499.00 and TXN10061 Swiggy -450.50)')
    lines.append('--  c) Month-end boundaries (TXN10038 2025-01-31 23:55:00 and TXN10039 2025-02-01 00:05:00)')
    lines.append('-- ------------------------------------------------------------------------------')

    for idx, row in subset.iterrows():
        tid = row['transaction_id']
        tdt = row['transaction_date']
        ym = row['year_month']
        cid = cat_map[row['category']]
        merch = str(row['merchant']).replace("'", "''")
        desc = str(row['description']).replace("'", "''")
        pmode = row['payment_mode']
        ttype = row['transaction_type']
        raw_amt = row['raw_amount']
        net_amt = row['net_amount']
        auto_cat = 1 if row['is_auto_categorised'] else 0
        
        sql_stmt = (
            f"INSERT INTO FACT_EXPENSES (TRANSACTION_ID, TRANSACTION_DATE, YEAR_MONTH, CATEGORY_ID, MERCHANT, DESCRIPTION, PAYMENT_MODE, TRANSACTION_TYPE, RAW_AMOUNT, NET_AMOUNT, IS_AUTO_CATEGORISED) "
            f"VALUES ('{tid}', TO_TIMESTAMP('{tdt}', 'YYYY-MM-DD HH24:MI:SS'), '{ym}', {cid}, '{merch}', '{desc}', '{pmode}', '{ttype}', {raw_amt:.2f}, {net_amt:.2f}, {auto_cat});"
        )
        lines.append(sql_stmt)

    lines.append('\n-- Commit all inserted records')
    lines.append('COMMIT;')
    lines.append('\n-- Verify loaded record counts')
    lines.append("SELECT 'DIM_CATEGORY' AS TABLE_NAME, COUNT(*) AS ROW_COUNT FROM DIM_CATEGORY")
    lines.append("UNION ALL")
    lines.append("SELECT 'DIM_BUDGET', COUNT(*) FROM DIM_BUDGET")
    lines.append("UNION ALL")
    lines.append("SELECT 'FACT_EXPENSES', COUNT(*) FROM FACT_EXPENSES;\n")

    content = '\n'.join(lines)
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"Generated '{output_path}' with {len(subset)} fact rows and 16 budget rows.")

if __name__ == "__main__":
    build_load_script()
