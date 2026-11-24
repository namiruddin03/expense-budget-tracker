"""
Personal Expense Tracker - Dataset Generator
Generates a realistic 12-month Indian personal expense dataset (~400 rows, INR amounts)
with explicit edge cases (uncategorised rows, refunds, month-end boundary timestamps).
"""

import os
import random
from datetime import datetime, timedelta
import pandas as pd
import numpy as np

def generate_dataset(output_path="data/raw_expenses.csv", seed=42):
    random.seed(seed)
    np.random.seed(seed)
    
    # 1. Base Merchant Catalog with Standard Categories & Descriptions
    merchant_catalog = {
        "Food & Dining": [
            ("Swiggy", "Online food delivery order"),
            ("Zomato", "Restaurant meal delivery"),
            ("Starbucks", "Coffee and snacks"),
            ("Chai Point", "Evening tea and snacks"),
            ("McDonald's", "Burgers and fries meal"),
            ("Dominos", "Weekend pizza party"),
            ("Haldiram's", "Lunch thali & sweets")
        ],
        "Groceries": [
            ("Blinkit", "Instant grocery essentials"),
            ("Zepto", "Fruits, milk and vegetables"),
            ("BigBasket", "Monthly grocery staples"),
            ("D-Mart", "Supermarket bulk provisions"),
            ("Nature's Basket", "Organic snacks & gourmet items")
        ],
        "Utilities & Bills": [
            ("Electricity Bill", "Monthly home electricity payment"),
            ("Jio", "Fiber broadband & 5G recharge"),
            ("Airtel", "Postpaid mobile bill"),
            ("Adani Gas", "Piped natural gas monthly utility"),
            ("ACT Fibernet", "Home high-speed internet subscription"),
            ("Bescom", "Bangalore power utility payment")
        ],
        "Transportation": [
            ("Uber", "Cab ride to workplace/airport"),
            ("Ola", "Auto ride city commute"),
            ("Rapido", "Bike taxi ride"),
            ("Indian Oil", "Vehicle fuel petrol pump"),
            ("Shell", "Premium petrol refill"),
            ("Delhi Metro", "Smart card top-up"),
            ("FASTag", "National highway toll recharge")
        ],
        "Shopping": [
            ("Amazon", "Electronics and home essentials"),
            ("Flipkart", "Books and household items"),
            ("Myntra", "Apparel, footwear and fashion"),
            ("Nykaa", "Skincare & grooming products"),
            ("Croma", "Gadgets and mobile accessories"),
            ("Zara", "Casual clothing purchase")
        ],
        "Entertainment & Leisure": [
            ("Netflix", "Monthly 4K streaming plan"),
            ("Spotify", "Music streaming subscription"),
            ("BookMyShow", "Cinema weekend movie tickets"),
            ("PVR Cinemas", "IMAX tickets and popcorn combo"),
            ("Hotstar", "Annual sports & entertainment pack")
        ],
        "Healthcare & Wellness": [
            ("Apollo Pharmacy", "Prescription medicines & vitamins"),
            ("Practo", "Doctor consultation fee"),
            ("Cult.fit", "Monthly fitness center access"),
            ("Pharmeasy", "Healthcare supplements & first aid")
        ],
        "Housing & Maintenance": [
            ("Society Maintenance", "Apartment monthly society dues"),
            ("Urban Company", "Home deep cleaning & AC repair"),
            ("Maid Salary", "Monthly domestic helper remuneration"),
            ("House Rent", "Monthly apartment residential rent")
        ]
    }
    
    payment_modes = ["UPI", "Credit Card", "Debit Card", "Net Banking", "Cash"]
    payment_weights = [0.45, 0.30, 0.12, 0.08, 0.05]
    
    # Amount distributions per category (INR)
    amount_ranges = {
        "Food & Dining": (150, 1850),
        "Groceries": (250, 4200),
        "Utilities & Bills": (450, 3800),
        "Transportation": (70, 1600),
        "Shopping": (500, 8500),
        "Entertainment & Leisure": (199, 1400),
        "Healthcare & Wellness": (200, 3200),
        "Housing & Maintenance": (1200, 28000)
    }

    records = []
    txn_id_counter = 10001
    
    # Generate ~30-34 transactions per month across 12 months (2025-01 to 2025-12)
    start_date = datetime(2025, 1, 1)
    
    for month in range(1, 13):
        # Determine number of regular transactions in this month (~28-32)
        n_month_txns = random.randint(28, 33)
        
        # Calculate days in this month
        if month in [1, 3, 5, 7, 8, 10, 12]:
            days_in_month = 31
        elif month == 2:
            days_in_month = 28
        else:
            days_in_month = 30
            
        for _ in range(n_month_txns):
            # Select random day and random time (keeping inside standard hours)
            day = random.randint(1, days_in_month)
            hour = random.randint(8, 22)
            minute = random.randint(0, 59)
            second = random.randint(0, 59)
            txn_dt = datetime(2025, month, day, hour, minute, second)
            
            # Select Category based on realistic expenditure likelihood
            category = random.choices(
                list(merchant_catalog.keys()),
                weights=[0.24, 0.20, 0.12, 0.16, 0.11, 0.07, 0.06, 0.04]
            )[0]
            
            merchant, desc = random.choice(merchant_catalog[category])
            
            # Amount based on category range
            low_amt, high_amt = amount_ranges[category]
            if category == "Housing & Maintenance" and merchant == "House Rent":
                amount = float(random.choice([25000.0, 26000.0, 25500.0]))
            else:
                amount = round(random.uniform(low_amt, high_amt), 2)
                
            pmode = random.choices(payment_modes, weights=payment_weights)[0]
            
            records.append({
                "transaction_id": f"TXN{txn_id_counter}",
                "transaction_date": txn_dt.strftime("%Y-%m-%d %H:%M:%S"),
                "merchant": merchant,
                "description": desc,
                "category": category,
                "payment_mode": pmode,
                "amount": amount,
                "transaction_type": "Expense"
            })
            txn_id_counter += 1

    # --- Edge Case (a): Uncategorised Expenses (~30 rows) ---
    # Rows where category is None, empty string "", or "Uncategorised"
    # for merchants like Swiggy, Zomato, Uber, Jio, Amazon, Electricity Bill
    uncategorised_candidates = [
        ("Swiggy", "Late night snack delivery", "Food & Dining"),
        ("Zomato", "Office team lunch order", "Food & Dining"),
        ("Uber", "Work commute ride to tech park", "Transportation"),
        ("Jio", "Jio Fiber broadband recharge", "Utilities & Bills"),
        ("Amazon", "Wireless mouse and desk organizer", "Shopping"),
        ("Electricity Bill", "Online power utility bill billdesk", "Utilities & Bills"),
        ("Blinkit", "Instant snacks and beverages", "Groceries"),
        ("Netflix", "Monthly streaming plan renew", "Entertainment & Leisure"),
        ("Apollo Pharmacy", "First aid and cold medicines", "Healthcare & Wellness")
    ]
    
    uncat_values = [None, "", "Uncategorised", "NaN"]
    
    for i in range(28):
        m_tuple = random.choice(uncategorised_candidates)
        m_name, m_desc, true_cat = m_tuple
        month = (i % 12) + 1
        day = random.randint(2, 27)
        dt = datetime(2025, month, day, random.randint(9, 21), random.randint(0, 59), random.randint(0, 59))
        
        low_amt, high_amt = amount_ranges[true_cat]
        amount = round(random.uniform(low_amt, min(high_amt, 2500)), 2)
        pmode = random.choice(["UPI", "Credit Card", "Debit Card"])
        cat_repr = uncat_values[i % len(uncat_values)]
        
        records.append({
            "transaction_id": f"TXN{txn_id_counter}",
            "transaction_date": dt.strftime("%Y-%m-%d %H:%M:%S"),
            "merchant": m_name,
            "description": m_desc,
            "category": cat_repr,  # Edge case: blank/null/Uncategorised
            "payment_mode": pmode,
            "amount": amount,
            "transaction_type": "Expense"
        })
        txn_id_counter += 1

    # --- Edge Case (b): Refund Entries (Negative amounts with transaction_type = 'Refund') ---
    # Realistic refund scenarios across different months
    refund_scenarios = [
        ("Amazon", "Return refund for damaged headphones", "Shopping", -1499.00, 1, 15),
        ("Swiggy", "Refund for cancelled dinner order", "Food & Dining", -450.50, 2, 18),
        ("Flipkart", "Return refund credited for apparel", "Shopping", -2199.00, 3, 22),
        ("Uber", "Driver cancellation fee refund", "Transportation", -110.00, 4, 10),
        ("BookMyShow", "Refund for show cancelled by cinema", "Entertainment & Leisure", -720.00, 5, 8),
        ("Zomato", "Missing items refund credited", "Food & Dining", -320.00, 6, 25),
        ("Myntra", "Size exchange return refund", "Shopping", -1850.00, 7, 14),
        ("Airtel", "Double recharge reversal credit", "Utilities & Bills", -799.00, 8, 19),
        ("Amazon", "Festival offer cashback and return credit", "Shopping", -3450.00, 9, 27),
        ("Cult.fit", "Session cancellation refund", "Healthcare & Wellness", -600.00, 10, 12),
        ("Zepto", "Out of stock items refund", "Groceries", -285.00, 11, 16),
        ("MakeMyTrip", "Flight seat upgrade cancellation refund", "Transportation", -1250.00, 12, 20)
    ]
    
    for m_name, m_desc, m_cat, r_amt, r_m, r_d in refund_scenarios:
        dt = datetime(2025, r_m, r_d, random.randint(10, 20), random.randint(0, 59), random.randint(0, 59))
        records.append({
            "transaction_id": f"TXN{txn_id_counter}",
            "transaction_date": dt.strftime("%Y-%m-%d %H:%M:%S"),
            "merchant": m_name,
            "description": m_desc,
            "category": m_cat,
            "payment_mode": "Credit Card" if "Amazon" in m_name or "Flipkart" in m_name else "UPI",
            "amount": r_amt,  # Negative amount
            "transaction_type": "Refund"  # Edge case: Refund type
        })
        txn_id_counter += 1

    # --- Edge Case (c): Month-End Boundary Dates ---
    # Specifically requested: 2025-01-31 23:55:00 and 2025-02-01 00:05:00, plus other boundaries
    boundary_pairs = [
        # (Timestamp string, merchant, desc, cat, amount, pmode)
        ("2025-01-31 23:55:00", "Swiggy", "Late midnight dinner delivery", "Food & Dining", 680.00, "UPI"),
        ("2025-02-01 00:05:00", "Uber", "Midnight return cab from airport", "Transportation", 920.00, "Credit Card"),
        ("2025-02-28 23:52:00", "Blinkit", "Late night ice cream & soda", "Groceries", 340.00, "UPI"),
        ("2025-03-01 00:08:00", "Netflix", "Monthly streaming plan billing", "Entertainment & Leisure", 649.00, "Credit Card"),
        ("2025-03-31 23:58:00", "Amazon", "Midnight flash sale purchase", "Shopping", 2499.00, "Credit Card"),
        ("2025-04-01 00:02:00", "Electricity Bill", "Online power utility bill payment", "Utilities & Bills", 1850.00, "Net Banking"),
        ("2025-04-30 23:45:00", "Zomato", "Late night biryani order", "Food & Dining", 540.00, "UPI"),
        ("2025-05-01 00:15:00", "Jio", "Monthly JioFiber payment renewal", "Utilities & Bills", 1179.00, "UPI"),
        ("2025-05-31 23:54:00", "Shell", "Highway fuel refill late night", "Transportation", 2100.00, "Credit Card"),
        ("2025-06-01 00:06:00", "House Rent", "Monthly residential rent transfer", "Housing & Maintenance", 25000.00, "Net Banking"),
        ("2025-06-30 23:59:00", "Swiggy", "Quarter-end late meal", "Food & Dining", 420.00, "UPI"),
        ("2025-07-01 00:01:00", "Uber", "Early morning cab to railway station", "Transportation", 450.00, "UPI"),
        ("2025-07-31 23:55:00", "BookMyShow", "Weekend movie advance booking", "Entertainment & Leisure", 820.00, "Debit Card"),
        ("2025-08-01 00:05:00", "Apollo Pharmacy", "Emergency night medical supplies", "Healthcare & Wellness", 460.00, "UPI"),
        ("2025-08-31 23:50:00", "Zepto", "Midnight dairy and snacks order", "Groceries", 290.00, "UPI"),
        ("2025-09-01 00:10:00", "Spotify", "Annual premium family plan renewal", "Entertainment & Leisure", 1799.00, "Credit Card"),
        ("2025-09-30 23:48:00", "Amazon", "Great Indian Festival advance cart order", "Shopping", 4999.00, "Credit Card"),
        ("2025-10-01 00:12:00", "Society Maintenance", "Quarter 4 society maintenance charge", "Housing & Maintenance", 4500.00, "Net Banking"),
        ("2025-10-31 23:56:00", "Zomato", "Halloween party food delivery", "Food & Dining", 1450.00, "UPI"),
        ("2025-11-01 00:04:00", "Airtel", "Monthly mobile postpaid recharge", "Utilities & Bills", 599.00, "UPI"),
        ("2025-11-30 23:58:00", "Myntra", "Black Friday end sale shopping", "Shopping", 3200.00, "Credit Card"),
        ("2025-12-01 00:02:00", "House Rent", "December home rent disbursement", "Housing & Maintenance", 25000.00, "Net Banking"),
        ("2025-12-31 23:55:00", "Swiggy", "New Year Eve party food & beverage order", "Food & Dining", 2850.00, "Credit Card")
    ]
    
    for b_dt, b_merch, b_desc, b_cat, b_amt, b_pmode in boundary_pairs:
        records.append({
            "transaction_id": f"TXN{txn_id_counter}",
            "transaction_date": b_dt,
            "merchant": b_merch,
            "description": b_desc,
            "category": b_cat,
            "payment_mode": b_pmode,
            "amount": b_amt,
            "transaction_type": "Expense"
        })
        txn_id_counter += 1

    df = pd.DataFrame(records)
    
    # Sort chronologically by transaction_date to maintain authentic ledger sequence
    df["dt_temp"] = pd.to_datetime(df["transaction_date"])
    df = df.sort_values("dt_temp").reset_index(drop=True)
    df = df.drop(columns=["dt_temp"])
    
    # Re-assign sequential transaction_ids
    df["transaction_id"] = [f"TXN{10000 + i + 1}" for i in range(len(df))]
    
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df.to_csv(output_path, index=False)
    
    print(f"Generated {len(df)} transactions in '{output_path}'.")
    print(f"Date range: {df['transaction_date'].min()} to {df['transaction_date'].max()}")
    print(f"Refunds count: {len(df[df['transaction_type'] == 'Refund'])}")
    print(f"Uncategorised/Blank/Null count: {df['category'].isin(['', 'Uncategorised', 'NaN', None]).sum() + df['category'].isna().sum()}")
    print("Sample rows:")
    print(df.head(5))
    
    return df

if __name__ == "__main__":
    generate_dataset()
