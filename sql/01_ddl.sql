-- ==============================================================================
-- PERSONAL EXPENSE TRACKER & BUDGET DASHBOARD
-- Script 01: Star-Schema DDL for Oracle Database / Oracle Live SQL
-- Tables: DIM_CATEGORY, DIM_BUDGET, FACT_EXPENSES, BUDGET_ALERTS
-- ==============================================================================

-- ------------------------------------------------------------------------------
-- 1. DROP EXISTING TABLES SAFELY
-- ------------------------------------------------------------------------------
BEGIN
    FOR t IN (
        SELECT table_name 
        FROM user_tables 
        WHERE table_name IN ('BUDGET_ALERTS', 'FACT_EXPENSES', 'DIM_BUDGET', 'DIM_CATEGORY')
    ) LOOP
        EXECUTE IMMEDIATE 'DROP TABLE ' || t.table_name || ' CASCADE CONSTRAINTS PURGE';
    END LOOP;
END;
/

-- ------------------------------------------------------------------------------
-- 2. DIM_CATEGORY: Category Master Dimension Table
-- ------------------------------------------------------------------------------
CREATE TABLE DIM_CATEGORY (
    CATEGORY_ID     NUMBER PRIMARY KEY,
    CATEGORY_NAME   VARCHAR2(50) NOT NULL UNIQUE,
    CATEGORY_GROUP  VARCHAR2(50) NOT NULL, -- 'Essential' vs 'Discretionary'
    DESCRIPTION     VARCHAR2(200),
    IS_ACTIVE       NUMBER(1) DEFAULT 1 CHECK (IS_ACTIVE IN (0, 1))
);

COMMENT ON TABLE DIM_CATEGORY IS 'Master dimension containing standardized spending categories and groupings.';
COMMENT ON COLUMN DIM_CATEGORY.CATEGORY_ID IS 'Surrogate primary key for expense category.';
COMMENT ON COLUMN DIM_CATEGORY.CATEGORY_NAME IS 'Standard category name (e.g., Food & Dining, Groceries).';
COMMENT ON COLUMN DIM_CATEGORY.CATEGORY_GROUP IS 'High-level financial classification (Essential vs Discretionary).';

-- ------------------------------------------------------------------------------
-- 3. DIM_BUDGET: Monthly Budget Planning Dimension Table
-- ------------------------------------------------------------------------------
CREATE TABLE DIM_BUDGET (
    BUDGET_ID       NUMBER PRIMARY KEY,
    YEAR_MONTH      VARCHAR2(7) NOT NULL, -- Format: 'YYYY-MM'
    CATEGORY_ID     NUMBER NOT NULL,
    BUDGET_AMOUNT   NUMBER(12, 2) NOT NULL CHECK (BUDGET_AMOUNT >= 0),
    CREATED_DATE    DATE DEFAULT SYSDATE,
    CONSTRAINT FK_BUDGET_CAT FOREIGN KEY (CATEGORY_ID) REFERENCES DIM_CATEGORY(CATEGORY_ID),
    CONSTRAINT UQ_BUDGET_MONTH_CAT UNIQUE (YEAR_MONTH, CATEGORY_ID)
);

COMMENT ON TABLE DIM_BUDGET IS 'Monthly planned expenditure targets per category for variance analysis.';
COMMENT ON COLUMN DIM_BUDGET.YEAR_MONTH IS 'Calendar budget period formatted as YYYY-MM.';
COMMENT ON COLUMN DIM_BUDGET.BUDGET_AMOUNT IS 'Target spend ceiling allocated in INR.';

-- ------------------------------------------------------------------------------
-- 4. FACT_EXPENSES: Central Granular Expense Fact Table
-- ------------------------------------------------------------------------------
CREATE TABLE FACT_EXPENSES (
    TRANSACTION_ID       VARCHAR2(20) PRIMARY KEY,
    TRANSACTION_DATE     TIMESTAMP NOT NULL,
    YEAR_MONTH           VARCHAR2(7) NOT NULL, -- Derived YYYY-MM boundary partition key
    CATEGORY_ID          NUMBER NOT NULL,
    MERCHANT             VARCHAR2(100) NOT NULL,
    DESCRIPTION          VARCHAR2(255),
    PAYMENT_MODE         VARCHAR2(30) NOT NULL, -- 'UPI', 'Credit Card', 'Debit Card', 'Net Banking', 'Cash'
    TRANSACTION_TYPE     VARCHAR2(20) NOT NULL CHECK (TRANSACTION_TYPE IN ('Expense', 'Refund')),
    RAW_AMOUNT           NUMBER(12, 2) NOT NULL,
    NET_AMOUNT           NUMBER(12, 2) NOT NULL, -- Strictly negative for Refund, positive for Expense
    IS_AUTO_CATEGORISED  NUMBER(1) DEFAULT 0 CHECK (IS_AUTO_CATEGORISED IN (0, 1)),
    CREATED_AT           DATE DEFAULT SYSDATE,
    CONSTRAINT FK_EXPENSE_CAT FOREIGN KEY (CATEGORY_ID) REFERENCES DIM_CATEGORY(CATEGORY_ID)
);

COMMENT ON TABLE FACT_EXPENSES IS 'Central transactional fact table recording audited debit & refund entries.';
COMMENT ON COLUMN FACT_EXPENSES.TRANSACTION_ID IS 'Unique business identifier for transaction (e.g. TXN10001).';
COMMENT ON COLUMN FACT_EXPENSES.NET_AMOUNT IS 'Reconciled net amount (positive for expense debits, negative for refund credits).';
COMMENT ON COLUMN FACT_EXPENSES.IS_AUTO_CATEGORISED IS 'Flag indicating whether category was resolved by automated keyword rules (1=Yes, 0=No).';

-- Indexes to optimize analytical rollups and star-schema join performance
CREATE INDEX IDX_FACT_YEAR_MONTH ON FACT_EXPENSES(YEAR_MONTH);
CREATE INDEX IDX_FACT_CATEGORY_ID ON FACT_EXPENSES(CATEGORY_ID);
CREATE INDEX IDX_FACT_TXN_DATE ON FACT_EXPENSES(TRANSACTION_DATE);

-- ------------------------------------------------------------------------------
-- 5. BUDGET_ALERTS: Automated Breach Detection and Audit Log Table
-- ------------------------------------------------------------------------------
CREATE TABLE BUDGET_ALERTS (
    ALERT_ID         NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    YEAR_MONTH       VARCHAR2(7) NOT NULL,
    CATEGORY_ID      NUMBER NOT NULL,
    ACTUAL_SPEND     NUMBER(12, 2) NOT NULL,
    BUDGET_AMOUNT    NUMBER(12, 2) NOT NULL,
    VARIANCE_AMOUNT  NUMBER(12, 2) NOT NULL, -- ACTUAL_SPEND - BUDGET_AMOUNT
    VARIANCE_PCT     NUMBER(6, 2) NOT NULL,  -- Over-budget percentage
    SEVERITY         VARCHAR2(20) NOT NULL CHECK (SEVERITY IN ('WARNING', 'CRITICAL')),
    ALERT_MESSAGE    VARCHAR2(500) NOT NULL,
    GENERATED_AT     TIMESTAMP DEFAULT SYSTIMESTAMP NOT NULL,
    CONSTRAINT FK_ALERT_CAT FOREIGN KEY (CATEGORY_ID) REFERENCES DIM_CATEGORY(CATEGORY_ID)
);

COMMENT ON TABLE BUDGET_ALERTS IS 'Audit table populated by automated PL/SQL procedures when actual monthly spend exceeds budget.';

-- Verification of created objects
SELECT table_name, status, num_rows 
FROM user_tables 
WHERE table_name IN ('DIM_CATEGORY', 'DIM_BUDGET', 'FACT_EXPENSES', 'BUDGET_ALERTS')
ORDER BY table_name;
