# Power BI Personal Expense & Budget Dashboard Guide

This guide provides the blueprint, data model relationships, and complete DAX measures required to build the interactive **Personal Expense Tracker and Budget Dashboard** in Power BI Desktop.

---

## 1. Data Model Relationships (Star Schema)

When importing data from Oracle or CSV (`data/cleaned_expenses.csv`, `sql/02_load.sql`), establish the following 1-to-Many (`1:*`) single-direction relationships:

| From Table (Dimension) | From Key | To Table (Fact) | To Key | Cardinality | Cross Filter |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `DIM_CATEGORY` | `CATEGORY_ID` | `FACT_EXPENSES` | `CATEGORY_ID` | `1 : Many (*)` | Single |
| `DIM_CATEGORY` | `CATEGORY_ID` | `DIM_BUDGET` | `CATEGORY_ID` | `1 : Many (*)` | Single |
| `DIM_CATEGORY` | `CATEGORY_ID` | `BUDGET_ALERTS` | `CATEGORY_ID` | `1 : Many (*)` | Single |
| `DIM_DATE` / Calendar | `Date` / `YearMonth` | `FACT_EXPENSES` | `TRANSACTION_DATE` / `YEAR_MONTH` | `1 : Many (*)` | Single |
| `DIM_DATE` / Calendar | `YearMonth` | `DIM_BUDGET` | `YEAR_MONTH` | `1 : Many (*)` | Single |

---

## 2. Core DAX Measure Library

Create a dedicated measure table `_Measures` and insert the following audited DAX formulas:

### A. Spend Aggregations & Refund Accounting
```dax
// 1. Total Outward Gross Outflow
Total Gross Spend = 
CALCULATE(
    SUM(FACT_EXPENSES[RAW_AMOUNT]),
    FACT_EXPENSES[TRANSACTION_TYPE] = "Expense"
)

// 2. Total Reconciled Refunds Credited
Total Refunds Credited = 
CALCULATE(
    ABS(SUM(FACT_EXPENSES[NET_AMOUNT])),
    FACT_EXPENSES[TRANSACTION_TYPE] = "Refund"
)

// 3. True Economic Net Spend
Total Net Spend = 
SUM(FACT_EXPENSES[NET_AMOUNT])

// 4. Refund Impact Rate
Refund Recovery Rate % = 
DIVIDE([Total Refunds Credited], [Total Gross Spend], 0)
```

### B. Budget vs Actual Variance & Health Indicators
```dax
// 5. Monthly Budget Allocation
Monthly Budget = 
SUM(DIM_BUDGET[BUDGET_AMOUNT])

// 6. Monetary Budget Variance (Positive = Over budget)
Budget Variance = 
[Total Net Spend] - [Monthly Budget]

// 7. Budget Utilisation Rate
Budget Utilisation % = 
DIVIDE([Total Net Spend], [Monthly Budget], 0)

// 8. Categorical Budget Status
Budget Status = 
SWITCH(
    TRUE(),
    ISBLANK([Monthly Budget]), "No Budget Defined",
    [Total Net Spend] > [Monthly Budget], "Over Budget",
    [Budget Utilisation %] >= 0.85, "Near Limit (85%+)",
    "Within Budget"
)

// 9. Dynamic KPI Status Color for Conditional Formatting
Budget Status Color = 
SWITCH(
    TRUE(),
    [Total Net Spend] > [Monthly Budget], "#B91C1C",  // Red
    [Budget Utilisation %] >= 0.85, "#D97706",        // Amber
    "#059669"                                        // Green
)
```

### C. Financial Behavioral & Channel Metrics
```dax
// 10. Essential vs Discretionary Spend
Essential Spend = 
CALCULATE(
    [Total Net Spend],
    DIM_CATEGORY[CATEGORY_GROUP] = "Essential"
)

Discretionary Spend = 
CALCULATE(
    [Total Net Spend],
    DIM_CATEGORY[CATEGORY_GROUP] = "Discretionary"
)

Discretionary Ratio % = 
DIVIDE([Discretionary Spend], [Total Net Spend], 0)

// 11. Cashless Payment Adoption
Cashless Transaction % = 
DIVIDE(
    CALCULATE(COUNTROWS(FACT_EXPENSES), FACT_EXPENSES[PAYMENT_MODE] <> "Cash"),
    COUNTROWS(FACT_EXPENSES),
    0
)
```

---

## 3. Recommended Canvas Layout (1920 x 1080)

1. **Top Navigation Ribbon (Height: 90px)**
   - Dashboard Title: `Personal Expense Tracker & Budget Variance Dashboard`
   - Slicers: `Year-Month` (Dropdown), `Category Group` (Buttons: All / Essential / Discretionary), `Payment Mode` (Tiles).

2. **Row 1: Executive KPI Cards (Height: 120px)**
   - Card 1: `Total Net Spend` (₹934.6K)
   - Card 2: `Allocated Budget` (₹980.0K)
   - Card 3: `Full-Year Variance` (-₹45.4K Under)
   - Card 4: `Refunds Credited` (₹13.5K across 12 txns)
   - Card 5: `Digital Adoption` (95.3% cashless)

3. **Row 2: Monthly Trends & Category Share (Height: 380px)**
   - Left Visual (Width: 60%): **Line & Clustered Column Chart**
     - X-Axis: `YEAR_MONTH`
     - Column Y-Axis: `[Total Net Spend]` vs `[Monthly Budget]`
     - Line Y-Axis: `[Budget Utilisation %]`
   - Right Visual (Width: 40%): **Donut Chart**
     - Legend: `DIM_CATEGORY[CATEGORY_NAME]`
     - Values: `[Total Net Spend]`

4. **Row 3: Variance Deep-Dive & Transaction Ledger (Height: 400px)**
   - Left Visual (Width: 50%): **Clustered Bar Chart**
     - Y-Axis: `DIM_CATEGORY[CATEGORY_NAME]`
     - X-Axis: `[Budget Variance]` (Conditionally formatted: Red if > 0, Green if ≤ 0)
   - Right Visual (Width: 50%): **Matrix / Table**
     - Rows: `TRANSACTION_DATE`, `MERCHANT`, `CATEGORY_NAME`, `PAYMENT_MODE`, `TRANSACTION_TYPE`
     - Values: `RAW_AMOUNT`, `NET_AMOUNT`
     - Highlight: Refund entries in soft red / negative parentheses.
