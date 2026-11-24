-- ==============================================================================
-- PERSONAL EXPENSE TRACKER & BUDGET DASHBOARD
-- Script 03: Views, Analytical Queries & PL/SQL Budget Breach Engine
-- Dialect: Oracle 19c / 21c / 23ai / Oracle Live SQL Compatible
-- ==============================================================================

SET SERVEROUTPUT ON SIZE 1000000;

-- ------------------------------------------------------------------------------
-- 1. ANALYTICAL VIEW: VW_MONTHLY_SPEND_VS_BUDGET
-- Joins DIM_BUDGET and FACT_EXPENSES to calculate actual net spend, variance, 
-- budget utilisation percentage, and status indicators.
-- ------------------------------------------------------------------------------
CREATE OR REPLACE VIEW VW_MONTHLY_SPEND_VS_BUDGET AS
SELECT 
    b.YEAR_MONTH,
    c.CATEGORY_ID,
    c.CATEGORY_NAME,
    c.CATEGORY_GROUP,
    b.BUDGET_AMOUNT,
    NVL(SUM(f.NET_AMOUNT), 0) AS ACTUAL_NET_SPEND,
    NVL(SUM(f.NET_AMOUNT), 0) - b.BUDGET_AMOUNT AS SPEND_VARIANCE,
    ROUND(
        (NVL(SUM(f.NET_AMOUNT), 0) / NULLIF(b.BUDGET_AMOUNT, 0)) * 100, 
        2
    ) AS UTILISATION_PCT,
    CASE 
        WHEN NVL(SUM(f.NET_AMOUNT), 0) > b.BUDGET_AMOUNT THEN 'OVER BUDGET'
        WHEN NVL(SUM(f.NET_AMOUNT), 0) >= (b.BUDGET_AMOUNT * 0.85) THEN 'NEAR LIMIT (85%+)'
        ELSE 'WITHIN BUDGET'
    END AS BUDGET_STATUS,
    COUNT(f.TRANSACTION_ID) AS TOTAL_TXNS,
    NVL(SUM(CASE WHEN f.TRANSACTION_TYPE = 'Refund' THEN 1 ELSE 0 END), 0) AS REFUND_COUNT,
    NVL(SUM(CASE WHEN f.TRANSACTION_TYPE = 'Refund' THEN ABS(f.NET_AMOUNT) ELSE 0 END), 0) AS REFUND_TOTAL_CREDIT
FROM DIM_BUDGET b
JOIN DIM_CATEGORY c 
    ON b.CATEGORY_ID = c.CATEGORY_ID
LEFT JOIN FACT_EXPENSES f 
    ON b.CATEGORY_ID = f.CATEGORY_ID 
   AND b.YEAR_MONTH = f.YEAR_MONTH
GROUP BY 
    b.YEAR_MONTH, 
    c.CATEGORY_ID, 
    c.CATEGORY_NAME, 
    c.CATEGORY_GROUP, 
    b.BUDGET_AMOUNT;

COMMENT ON TABLE VW_MONTHLY_SPEND_VS_BUDGET IS 'Primary analytical view for spend vs budget variance, utilisation and breach alerts.';

-- ------------------------------------------------------------------------------
-- 2. ENTERPRISE ANALYTICAL QUERIES
-- ------------------------------------------------------------------------------

-- Query 2.1: Category Budget Breach & Variance Summary (Ranked by Overspend)
PROMPT === QUERY 2.1: TOP BUDGET BREACHES & VARIANCE BY CATEGORY ===
SELECT 
    YEAR_MONTH,
    CATEGORY_NAME,
    CATEGORY_GROUP,
    TO_CHAR(BUDGET_AMOUNT, 'FM₹999,990.00') AS BUDGET_INR,
    TO_CHAR(ACTUAL_NET_SPEND, 'FM₹999,990.00') AS ACTUAL_SPEND_INR,
    TO_CHAR(SPEND_VARIANCE, 'FM₹999,990.00') AS VARIANCE_INR,
    TO_CHAR(UTILISATION_PCT, '990.99') || '%' AS UTILISATION_RATE,
    BUDGET_STATUS
FROM VW_MONTHLY_SPEND_VS_BUDGET
WHERE ACTUAL_NET_SPEND > BUDGET_AMOUNT
ORDER BY SPEND_VARIANCE DESC;

-- Query 2.2: Essential vs Discretionary Spend Distribution
PROMPT === QUERY 2.2: ESSENTIAL VS DISCRETIONARY SPEND BREAKDOWN ===
SELECT 
    YEAR_MONTH,
    CATEGORY_GROUP,
    COUNT(DISTINCT CATEGORY_ID) AS CATEGORIES_COUNT,
    TO_CHAR(SUM(BUDGET_AMOUNT), 'FM₹999,990.00') AS TOTAL_BUDGET,
    TO_CHAR(SUM(ACTUAL_NET_SPEND), 'FM₹999,990.00') AS TOTAL_NET_SPEND,
    ROUND((SUM(ACTUAL_NET_SPEND) / SUM(SUM(ACTUAL_NET_SPEND)) OVER (PARTITION BY YEAR_MONTH)) * 100, 2) || '%' AS PCT_OF_TOTAL_SPEND
FROM VW_MONTHLY_SPEND_VS_BUDGET
GROUP BY YEAR_MONTH, CATEGORY_GROUP
ORDER BY YEAR_MONTH, CATEGORY_GROUP;

-- Query 2.3: Payment Mode Distribution & Digital Adoption Rate
PROMPT === QUERY 2.3: PAYMENT MODE SHARE AND DIGITAL ADOPTION ===
SELECT 
    PAYMENT_MODE,
    COUNT(TRANSACTION_ID) AS TXN_COUNT,
    ROUND((COUNT(TRANSACTION_ID) / SUM(COUNT(TRANSACTION_ID)) OVER ()) * 100, 2) || '%' AS TXN_SHARE,
    TO_CHAR(SUM(NET_AMOUNT), 'FM₹999,990.00') AS TOTAL_NET_AMOUNT,
    ROUND((SUM(NET_AMOUNT) / SUM(SUM(NET_AMOUNT)) OVER ()) * 100, 2) || '%' AS SPEND_SHARE
FROM FACT_EXPENSES
GROUP BY PAYMENT_MODE
ORDER BY SUM(NET_AMOUNT) DESC;

-- Query 2.4: Month-End Boundary Audit (Transactions within 15 min of Midnight)
PROMPT === QUERY 2.4: MONTH-END BOUNDARY RECONCILIATION AUDIT ===
SELECT 
    TRANSACTION_ID,
    TO_CHAR(TRANSACTION_DATE, 'YYYY-MM-DD HH24:MI:SS') AS TXN_TIMESTAMP,
    YEAR_MONTH AS ASSIGNED_PERIOD,
    MERCHANT,
    TRANSACTION_TYPE,
    TO_CHAR(NET_AMOUNT, 'FM₹999,990.00') AS NET_AMOUNT_INR
FROM FACT_EXPENSES
WHERE (TO_CHAR(TRANSACTION_DATE, 'DD HH24:MI') >= '31 23:45' AND TO_CHAR(TRANSACTION_DATE, 'DD') IN ('30', '31', '28'))
   OR (TO_CHAR(TRANSACTION_DATE, 'DD HH24:MI') <= '01 00:15')
ORDER BY TRANSACTION_DATE;

-- Query 2.5: Refund Netting and Recovery Analysis
PROMPT === QUERY 2.5: REFUND NETTING AND RECOVERY AUDIT ===
SELECT 
    c.CATEGORY_NAME,
    COUNT(CASE WHEN f.TRANSACTION_TYPE = 'Expense' THEN 1 END) AS EXPENSE_TXNS,
    TO_CHAR(NVL(SUM(CASE WHEN f.TRANSACTION_TYPE = 'Expense' THEN f.RAW_AMOUNT END), 0), 'FM₹999,990.00') AS GROSS_EXPENSE,
    COUNT(CASE WHEN f.TRANSACTION_TYPE = 'Refund' THEN 1 END) AS REFUND_TXNS,
    TO_CHAR(NVL(SUM(CASE WHEN f.TRANSACTION_TYPE = 'Refund' THEN ABS(f.NET_AMOUNT) END), 0), 'FM₹999,990.00') AS REFUNDS_CREDITED,
    TO_CHAR(NVL(SUM(f.NET_AMOUNT), 0), 'FM₹999,990.00') AS FINAL_NET_SPEND
FROM DIM_CATEGORY c
LEFT JOIN FACT_EXPENSES f ON c.CATEGORY_ID = f.CATEGORY_ID
GROUP BY c.CATEGORY_NAME
ORDER BY NVL(SUM(f.NET_AMOUNT), 0) DESC;

-- ------------------------------------------------------------------------------
-- 3. PL/SQL STORED PROCEDURE: PRC_EVALUATE_BUDGET_ALERTS
-- Evaluates monthly category spend against DIM_BUDGET targets and logs any 
-- budget overruns into the BUDGET_ALERTS table with severity classification.
-- ------------------------------------------------------------------------------
CREATE OR REPLACE PROCEDURE PRC_EVALUATE_BUDGET_ALERTS (
    p_year_month IN VARCHAR2
) IS
    v_alert_count       NUMBER := 0;
    v_critical_count    NUMBER := 0;
    v_warning_count     NUMBER := 0;
    v_variance          NUMBER(12, 2);
    v_variance_pct      NUMBER(6, 2);
    v_severity          VARCHAR2(20);
    v_message           VARCHAR2(500);

    -- Cursor iterating through categories where actual net spend exceeds budget
    CURSOR cur_breaches IS
        SELECT 
            b.YEAR_MONTH,
            c.CATEGORY_ID,
            c.CATEGORY_NAME,
            b.BUDGET_AMOUNT,
            NVL(SUM(f.NET_AMOUNT), 0) AS ACTUAL_SPEND
        FROM DIM_BUDGET b
        JOIN DIM_CATEGORY c 
            ON b.CATEGORY_ID = c.CATEGORY_ID
        LEFT JOIN FACT_EXPENSES f 
            ON b.CATEGORY_ID = f.CATEGORY_ID 
           AND b.YEAR_MONTH = f.YEAR_MONTH
        WHERE b.YEAR_MONTH = p_year_month
        GROUP BY b.YEAR_MONTH, c.CATEGORY_ID, c.CATEGORY_NAME, b.BUDGET_AMOUNT
        HAVING NVL(SUM(f.NET_AMOUNT), 0) > b.BUDGET_AMOUNT
        ORDER BY (NVL(SUM(f.NET_AMOUNT), 0) - b.BUDGET_AMOUNT) DESC;

BEGIN
    DBMS_OUTPUT.PUT_LINE('================================================================');
    DBMS_OUTPUT.PUT_LINE('EXECUTING BUDGET ALERT EVALUATION FOR PERIOD: ' || p_year_month);
    DBMS_OUTPUT.PUT_LINE('================================================================');

    -- Purge previous alerts for the same month to ensure idempotent re-runs
    DELETE FROM BUDGET_ALERTS WHERE YEAR_MONTH = p_year_month;

    -- Evaluate breaches
    FOR r IN cur_breaches LOOP
        v_variance := r.ACTUAL_SPEND - r.BUDGET_AMOUNT;
        v_variance_pct := ROUND((v_variance / r.BUDGET_AMOUNT) * 100, 2);
        
        -- Severity rule: > 15% breach is CRITICAL, <= 15% is WARNING
        IF v_variance_pct > 15.00 THEN
            v_severity := 'CRITICAL';
            v_critical_count := v_critical_count + 1;
        ELSE
            v_severity := 'WARNING';
            v_warning_count := v_warning_count + 1;
        END IF;

        v_message := '[' || v_severity || ' BREACH] ' || r.CATEGORY_NAME || 
                     ' spend (INR ' || TO_CHAR(r.ACTUAL_SPEND, 'FM999,990.00') || 
                     ') exceeded budget (INR ' || TO_CHAR(r.BUDGET_AMOUNT, 'FM999,990.00') || 
                     ') by ' || TO_CHAR(v_variance_pct, 'FM990.99') || '% (+INR ' || 
                     TO_CHAR(v_variance, 'FM999,990.00') || ').';

        -- Insert audit record into BUDGET_ALERTS
        INSERT INTO BUDGET_ALERTS (
            YEAR_MONTH,
            CATEGORY_ID,
            ACTUAL_SPEND,
            BUDGET_AMOUNT,
            VARIANCE_AMOUNT,
            VARIANCE_PCT,
            SEVERITY,
            ALERT_MESSAGE,
            GENERATED_AT
        ) VALUES (
            r.YEAR_MONTH,
            r.CATEGORY_ID,
            r.ACTUAL_SPEND,
            r.BUDGET_AMOUNT,
            v_variance,
            v_variance_pct,
            v_severity,
            v_message,
            SYSTIMESTAMP
        );

        v_alert_count := v_alert_count + 1;
        DBMS_OUTPUT.PUT_LINE('-> Alert Logged: ' || v_message);
    END LOOP;

    COMMIT;

    DBMS_OUTPUT.PUT_LINE('----------------------------------------------------------------');
    DBMS_OUTPUT.PUT_LINE('EVALUATION COMPLETE FOR ' || p_year_month || ':');
    DBMS_OUTPUT.PUT_LINE('  Total Overruns Detected: ' || v_alert_count);
    DBMS_OUTPUT.PUT_LINE('  Critical Alerts (>15%):  ' || v_critical_count);
    DBMS_OUTPUT.PUT_LINE('  Warning Alerts (<=15%):  ' || v_warning_count);
    DBMS_OUTPUT.PUT_LINE('================================================================');

EXCEPTION
    WHEN OTHERS THEN
        ROLLBACK;
        DBMS_OUTPUT.PUT_LINE('ERROR in PRC_EVALUATE_BUDGET_ALERTS: ' || SQLERRM);
        RAISE;
END PRC_EVALUATE_BUDGET_ALERTS;
/

-- ------------------------------------------------------------------------------
-- 4. EXECUTABLE ANONYMOUS BLOCK & ALERT VERIFICATION
-- Runs the procedure for both 2025-01 and 2025-02, then prints the audit table.
-- ------------------------------------------------------------------------------
BEGIN
    PRC_EVALUATE_BUDGET_ALERTS('2025-01');
    PRC_EVALUATE_BUDGET_ALERTS('2025-02');
END;
/

-- Query the resulting audit table
PROMPT === FINAL BUDGET_ALERTS AUDIT LOG TABLE ===
SELECT 
    ALERT_ID,
    YEAR_MONTH,
    CATEGORY_ID,
    SEVERITY,
    TO_CHAR(ACTUAL_SPEND, 'FM₹999,990.00') AS ACTUAL_SPEND,
    TO_CHAR(BUDGET_AMOUNT, 'FM₹999,990.00') AS BUDGET_AMOUNT,
    TO_CHAR(VARIANCE_AMOUNT, 'FM₹999,990.00') AS VARIANCE_AMOUNT,
    TO_CHAR(VARIANCE_PCT, '990.99') || '%' AS VARIANCE_PCT,
    ALERT_MESSAGE
FROM BUDGET_ALERTS
ORDER BY YEAR_MONTH, VARIANCE_AMOUNT DESC;
