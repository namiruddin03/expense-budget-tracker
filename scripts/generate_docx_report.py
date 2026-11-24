"""
Personal Expense Tracker & Budget Dashboard - Project Report Generator
Generates docs/Personal_Expense_Project_Report.docx using python-docx.
Includes:
  - Executive Problem Statement & KPI Definitions
  - Embedded Star-Schema Diagram (docs/star_schema.png)
  - Data Quality & 12-Month Financial Reconciliation Summary (actual numbers)
  - Key Insights Summary (top categories, refund impact, budget breaches)
  - Dedicated Placeholder Sections:
      * [INSERT ORACLE PL/SQL OUTPUT SCREENSHOT]
      * [INSERT POWER BI DASHBOARD SCREENSHOT]
      * [GITHUB REPO LINK]
      * [DEMO VIDEO LINK]
"""

import os
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import parse_xml, OxmlElement
from docx.oxml.ns import nsdecls, qn

# Color Palette Constants
HEX_NAVY = "1B365D"
HEX_SLATE = "475569"
HEX_TEAL = "0D9488"
HEX_LIGHT_BG = "F8FAFC"
HEX_ALT_BG = "F1F5F9"
HEX_GREEN_BG = "E6F4EA"
HEX_GREEN_TEXT = "006100"
HEX_BORDER = "CBD5E1"
HEX_CALLOUT_BORDER = "1B365D"
HEX_PLACEHOLDER_BG = "FFFBEB"
HEX_PLACEHOLDER_BORDER = "D97706"

COLOR_NAVY = RGBColor(27, 54, 93)
COLOR_SLATE = RGBColor(71, 85, 105)
COLOR_DARK = RGBColor(15, 23, 42)
COLOR_MUTED = RGBColor(100, 116, 139)
COLOR_WHITE = RGBColor(255, 255, 255)

def set_cell_background(cell, hex_color):
    """Sets cell background fill color"""
    tcPr = cell._tc.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{hex_color}"/>')
    tcPr.append(shd)

def set_cell_margins(cell, top=120, bottom=120, left=150, right=150):
    """Sets inner cell padding in twips (1 pt = 20 twips)"""
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = parse_xml(
        f'<w:tcMar {nsdecls("w")}>'
        f'<w:top w:w="{top}" w:type="dxa"/>'
        f'<w:bottom w:w="{bottom}" w:type="dxa"/>'
        f'<w:left w:w="{left}" w:type="dxa"/>'
        f'<w:right w:w="{right}" w:type="dxa"/>'
        f'</w:tcMar>'
    )
    tcPr.append(tcMar)

def set_table_borders(table, color=HEX_BORDER):
    """Applies clean thin border to entire table"""
    tblPr = table._tbl.tblPr
    borders = parse_xml(
        f'<w:tblBorders {nsdecls("w")}>'
        f'<w:top w:val="single" w:sz="4" w:space="0" w:color="{color}"/>'
        f'<w:bottom w:val="single" w:sz="4" w:space="0" w:color="{color}"/>'
        f'<w:insideH w:val="single" w:sz="4" w:space="0" w:color="{color}"/>'
        f'<w:insideV w:val="none"/>'
        f'<w:left w:val="none"/>'
        f'<w:right w:val="none"/>'
        f'</w:tblBorders>'
    )
    tblPr.append(borders)

def add_callout(doc, title, text, border_color=HEX_CALLOUT_BORDER, bg_color=HEX_ALT_BG):
    """Creates a professional callout box with a colored left accent border"""
    tbl = doc.add_table(rows=1, cols=1)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    cell = tbl.cell(0, 0)
    cell.width = Inches(6.5)
    
    set_cell_background(cell, bg_color)
    set_cell_margins(cell, top=160, bottom=160, left=200, right=200)
    
    # Left border only
    tcPr = cell._tc.get_or_add_tcPr()
    tcBorders = parse_xml(
        f'<w:tcBorders {nsdecls("w")}>'
        f'<w:left w:val="single" w:sz="24" w:space="0" w:color="{border_color}"/>'
        f'<w:top w:val="none"/>'
        f'<w:right w:val="none"/>'
        f'<w:bottom w:val="none"/>'
        f'</w:tcBorders>'
    )
    tcPr.append(tcBorders)
    
    p = cell.paragraphs[0]
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(3)
    run_title = p.add_run(f"📌 {title}")
    run_title.font.name = "Calibri"
    run_title.font.size = Pt(11)
    run_title.font.bold = True
    run_title.font.color.rgb = COLOR_NAVY
    
    p2 = cell.add_paragraph()
    p2.paragraph_format.space_before = Pt(0)
    p2.paragraph_format.space_after = Pt(0)
    run_body = p2.add_run(text)
    run_body.font.name = "Calibri"
    run_body.font.size = Pt(10)
    run_body.font.color.rgb = COLOR_SLATE
    
    doc.add_paragraph().paragraph_format.space_after = Pt(4)

def add_placeholder_box(doc, placeholder_tag, description, icon="🖼️"):
    """Creates a prominent visual placeholder box for screenshots and links"""
    tbl = doc.add_table(rows=1, cols=1)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    cell = tbl.cell(0, 0)
    cell.width = Inches(6.5)
    
    set_cell_background(cell, HEX_PLACEHOLDER_BG)
    set_cell_margins(cell, top=200, bottom=200, left=220, right=220)
    
    # Dashed amber border
    tcPr = cell._tc.get_or_add_tcPr()
    tcBorders = parse_xml(
        f'<w:tcBorders {nsdecls("w")}>'
        f'<w:left w:val="dashed" w:sz="12" w:space="0" w:color="{HEX_PLACEHOLDER_BORDER}"/>'
        f'<w:top w:val="dashed" w:sz="12" w:space="0" w:color="{HEX_PLACEHOLDER_BORDER}"/>'
        f'<w:right w:val="dashed" w:sz="12" w:space="0" w:color="{HEX_PLACEHOLDER_BORDER}"/>'
        f'<w:bottom w:val="dashed" w:sz="12" w:space="0" w:color="{HEX_PLACEHOLDER_BORDER}"/>'
        f'</w:tcBorders>'
    )
    tcPr.append(tcBorders)
    
    p = cell.paragraphs[0]
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(4)
    p.paragraph_format.space_after = Pt(4)
    
    r_tag = p.add_run(f"{icon} {placeholder_tag}\n")
    r_tag.font.name = "Calibri"
    r_tag.font.size = Pt(12)
    r_tag.font.bold = True
    r_tag.font.color.rgb = RGBColor(180, 83, 9)
    
    r_desc = p.add_run(description)
    r_desc.font.name = "Calibri"
    r_desc.font.size = Pt(9.5)
    r_desc.font.italic = True
    r_desc.font.color.rgb = COLOR_SLATE
    
    doc.add_paragraph().paragraph_format.space_after = Pt(6)

def format_cell_text(cell, text, bold=False, italic=False, font_size=9.5, align=WD_ALIGN_PARAGRAPH.LEFT, color=COLOR_DARK):
    p = cell.paragraphs[0]
    p.alignment = align
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(0)
    run = p.add_run(str(text))
    run.font.name = "Calibri"
    run.font.size = Pt(font_size)
    run.font.bold = bold
    run.font.italic = italic
    run.font.color.rgb = color
    cell.vertical_alignment = WD_ALIGN_VERTICAL.CENTER

def build_report(output_path="docs/Personal_Expense_Project_Report.docx",
                 diagram_path="docs/star_schema.png"):
    
    doc = docx.Document()
    
    # Page setup - Standard Letter, 0.75-inch margins
    sections = doc.sections
    for section in sections:
        section.top_margin = Inches(0.75)
        section.bottom_margin = Inches(0.75)
        section.left_margin = Inches(0.75)
        section.right_margin = Inches(0.75)

    # Base Styles
    style_normal = doc.styles['Normal']
    style_normal.font.name = 'Calibri'
    style_normal.font.size = Pt(10.5)
    style_normal.font.color.rgb = COLOR_SLATE
    style_normal.paragraph_format.line_spacing = 1.15
    style_normal.paragraph_format.space_after = Pt(6)

    # --------------------------------------------------------------------------
    # COVER / HEADER BANNER
    # --------------------------------------------------------------------------
    p_pre = doc.add_paragraph()
    p_pre.paragraph_format.space_before = Pt(10)
    p_pre.paragraph_format.space_after = Pt(2)
    r_meta = p_pre.add_run("ENTERPRISE DATA ANALYTICS & FINANCIAL RECONCILIATION CASE STUDY")
    r_meta.font.name = "Calibri"
    r_meta.font.size = Pt(9)
    r_meta.font.bold = True
    r_meta.font.color.rgb = COLOR_MUTED

    p_title = doc.add_paragraph()
    p_title.paragraph_format.space_before = Pt(0)
    p_title.paragraph_format.space_after = Pt(4)
    r_title = p_title.add_run("Personal Expense Tracker & Budget Dashboard")
    r_title.font.name = "Calibri"
    r_title.font.size = Pt(24)
    r_title.font.bold = True
    r_title.font.color.rgb = COLOR_NAVY

    p_sub = doc.add_paragraph()
    p_sub.paragraph_format.space_before = Pt(0)
    p_sub.paragraph_format.space_after = Pt(14)
    r_sub = p_sub.add_run("Full-Lifecycle Data Engineering, Dimensional Star-Schema Modeling, PL/SQL Audit Engine & Power BI Analytics")
    r_sub.font.name = "Calibri"
    r_sub.font.size = Pt(12)
    r_sub.font.italic = True
    r_sub.font.color.rgb = COLOR_SLATE

    # Metadata Ribbon Table
    meta_tbl = doc.add_table(rows=1, cols=4)
    meta_tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    col_widths = [Inches(1.6), Inches(1.6), Inches(1.6), Inches(1.7)]
    meta_data = [
        ("PROJECT DOMAIN", "Personal Finance & FinTech"),
        ("DATA ENGINE", "Python, Oracle SQL / PL/SQL"),
        ("REPORTING LAYER", "Power BI / DAX / Excel"),
        ("AUDIT RESULT", "100% Monthly Reconciliation")
    ]
    for i, (k, v) in enumerate(meta_data):
        cell = meta_tbl.cell(0, i)
        cell.width = col_widths[i]
        set_cell_background(cell, HEX_ALT_BG)
        set_cell_margins(cell, top=80, bottom=80, left=100, right=100)
        p = cell.paragraphs[0]
        p.paragraph_format.space_after = Pt(0)
        r1 = p.add_run(f"{k}\n")
        r1.font.name = "Calibri"
        r1.font.size = Pt(7.5)
        r1.font.bold = True
        r1.font.color.rgb = COLOR_MUTED
        r2 = p.add_run(v)
        r2.font.name = "Calibri"
        r2.font.size = Pt(9)
        r2.font.bold = True
        r2.font.color.rgb = COLOR_NAVY
    set_table_borders(meta_tbl)

    doc.add_paragraph().paragraph_format.space_after = Pt(12)

    # --------------------------------------------------------------------------
    # 1. EXECUTIVE SUMMARY & PROBLEM STATEMENT
    # --------------------------------------------------------------------------
    h1 = doc.add_heading("1. Executive Summary & Problem Statement", level=1)
    h1.style.font.color.rgb = COLOR_NAVY
    h1.paragraph_format.space_before = Pt(14)
    h1.paragraph_format.space_after = Pt(6)

    doc.add_paragraph(
        "In the contemporary Indian digital payment landscape, individuals execute hundreds of monthly transactions "
        "across fragmented platforms—including UPI (Unified Payments Interface), Credit Cards, Net Banking, and Debit Cards. "
        "Without automated reconciliation and structured dimensional data warehousing, tracking true personal financial health "
        "is impeded by three major systemic data quality anomalies:"
    )

    doc.add_paragraph(
        "1. Uncategorised & Missing Metadata: Online aggregator merchants (e.g., Swiggy, Zomato, Uber, Jio, Amazon, Electricity Bill) "
        "frequently ingest with blank, null, or generic category descriptions, obscuring lifestyle vs essential expenditure trends.",
        style='List Bullet'
    )
    doc.add_paragraph(
        "2. Refund Accounting Discrepancies: E-commerce returns, failed transaction chargebacks, and service refunds create negative "
        "adjustments that are frequently booked either as separate gross income or left isolated, artificially inflating gross spend.",
        style='List Bullet'
    )
    doc.add_paragraph(
        "3. Month-End Temporal Skew: High-velocity transactions occurring across midnight boundaries (e.g., 2025-01-31 23:55:00 vs "
        "2025-02-01 00:05:00) cause budget leakage across reporting periods if parsed naively by date without calendar partitioning.",
        style='List Bullet'
    )

    add_callout(
        doc,
        title="Project Mission & Objective",
        text="To build an end-to-end audited analytics solution: generating 12 months of realistic Indian transaction data, "
             "executing deterministic Python regex cleaning and zero-variance net financial reconciliation, implementing an "
             "Oracle 19c/21c star-schema warehouse with automated PL/SQL budget alert evaluation, and architecting an executive dashboard."
    )

    # --------------------------------------------------------------------------
    # 2. KEY PERFORMANCE INDICATOR (KPI) DEFINITIONS
    # --------------------------------------------------------------------------
    h2 = doc.add_heading("2. Key Performance Indicators (KPI) & Metrics Framework", level=1)
    h2.style.font.color.rgb = COLOR_NAVY
    h2.paragraph_format.space_before = Pt(14)
    h2.paragraph_format.space_after = Pt(6)

    doc.add_paragraph(
        "To establish strict analytical governance, the tracking system implements a rigorous KPI framework. "
        "Each metric is formally defined below:"
    )

    kpi_tbl = doc.add_table(rows=1, cols=4)
    kpi_tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    kpi_widths = [Inches(1.5), Inches(1.8), Inches(2.2), Inches(1.0)]
    kpi_headers = ["KPI Metric Name", "Mathematical Formula", "Analytical Objective", "Target / Range"]
    
    for i, h_text in enumerate(kpi_headers):
        cell = kpi_tbl.cell(0, i)
        cell.width = kpi_widths[i]
        set_cell_background(cell, HEX_NAVY)
        set_cell_margins(cell, top=100, bottom=100, left=100, right=100)
        format_cell_text(cell, h_text, bold=True, font_size=9, color=COLOR_WHITE)

    kpi_rows = [
        ("Gross Expenses", "Σ Amount (where Type = 'Expense')", "Quantifies total outward cash outflows prior to returns.", "Baseline Spend"),
        ("Net Spend", "Gross Expenses - Σ |Refunds|", "True economic outflow representing actual personal consumption.", "Audited Net"),
        ("Refund Recovery Rate", "(Total Refund Credit / Gross Outflow) * 100", "Measures financial friction & credit recovery percentage.", "1.0% - 3.0%"),
        ("Budget Utilisation %", "(Actual Net Spend / Allocated Budget) * 100", "Tracks adherence to monthly spending ceilings per category.", "< 85% Healthy"),
        ("Spend Variance", "Actual Net Spend - Monthly Budget", "Absolute monetary gap; positive indicates over-budget breach.", "≤ ₹0.00"),
        ("Cashless Adoption %", "(Cashless Spend / Total Spend) * 100", "Evaluates penetration of digital instruments (UPI & Credit).", "> 95.0%"),
        ("Discretionary Ratio", "(Discretionary Spend / Total Spend) * 100", "Monitors lifestyle spending (Shopping, Dining, Leisure).", "30% - 40%")
    ]

    for row_idx, r_data in enumerate(kpi_rows):
        row = kpi_tbl.add_row()
        bg_color = HEX_ALT_BG if row_idx % 2 == 1 else "FFFFFF"
        for col_idx, val in enumerate(r_data):
            cell = row.cells[col_idx]
            cell.width = kpi_widths[col_idx]
            set_cell_background(cell, bg_color)
            set_cell_margins(cell, top=80, bottom=80, left=100, right=100)
            is_bold = (col_idx == 0)
            align = WD_ALIGN_PARAGRAPH.CENTER if col_idx in [3] else WD_ALIGN_PARAGRAPH.LEFT
            format_cell_text(cell, val, bold=is_bold, font_size=8.5, align=align)
    set_table_borders(kpi_tbl)

    doc.add_paragraph().paragraph_format.space_after = Pt(10)

    # --------------------------------------------------------------------------
    # 3. ENTERPRISE DATA ARCHITECTURE & STAR-SCHEMA MODEL
    # --------------------------------------------------------------------------
    h3 = doc.add_heading("3. Enterprise Data Architecture & Star-Schema Model", level=1)
    h3.style.font.color.rgb = COLOR_NAVY
    h3.paragraph_format.space_before = Pt(14)
    h3.paragraph_format.space_after = Pt(6)

    doc.add_paragraph(
        "The project implements a modern dimensional Star-Schema optimized for analytical processing in Oracle Database. "
        "The central fact table (FACT_EXPENSES) preserves transaction-level granularity while dimension tables (DIM_CATEGORY, "
        "DIM_BUDGET) provide conforming attributes for slice-and-dice aggregations. An automated audit table (BUDGET_ALERTS) "
        "records threshold overruns evaluated by stored procedures."
    )

    # Embed Star-Schema Diagram
    if os.path.exists(diagram_path):
        p_img = doc.add_paragraph()
        p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_img.paragraph_format.space_before = Pt(8)
        p_img.paragraph_format.space_after = Pt(4)
        run_img = p_img.add_run()
        run_img.add_picture(diagram_path, width=Inches(6.2))

        p_caption = doc.add_paragraph()
        p_caption.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_caption.paragraph_format.space_before = Pt(0)
        p_caption.paragraph_format.space_after = Pt(12)
        r_cap = p_caption.add_run("Figure 1: Production Star-Schema Architecture Diagram (Oracle Database / Live SQL)")
        r_cap.font.name = "Calibri"
        r_cap.font.size = Pt(8.5)
        r_cap.font.italic = True
        r_cap.font.color.rgb = COLOR_MUTED

    # Table Dictionary
    doc.add_paragraph(
        "Star-Schema Entity Dictionary:",
        style='Normal'
    )
    entities = [
        ("DIM_CATEGORY (Dimension)", "Holds 8 standardized expense categories, classification groups ('Essential' vs 'Discretionary'), and operational descriptions. Surrogate Key: CATEGORY_ID."),
        ("DIM_BUDGET (Dimension)", "Maintains planned monthly spending ceilings allocated per category across budget periods (YEAR_MONTH). Primary Key: BUDGET_ID. Unique Constraint: (YEAR_MONTH, CATEGORY_ID)."),
        ("FACT_EXPENSES (Central Fact)", "Contains audited transaction debits and refund credits. Stores RAW_AMOUNT and reconciled NET_AMOUNT. Foreign Key: CATEGORY_ID."),
        ("BUDGET_ALERTS (Audit Fact)", "Populated by the PL/SQL stored procedure whenever actual monthly net spend exceeds the planned budget target. Classifies severity into WARNING (≤15%) or CRITICAL (>15%)."),
        ("VW_MONTHLY_SPEND_VS_BUDGET (View)", "Dynamic relational view computing monthly spend variance, budget utilisation %, refund credit totals, and budget status indicators.")
    ]
    for ent, desc in entities:
        p_e = doc.add_paragraph(style='List Bullet')
        r_e1 = p_e.add_run(f"{ent}: ")
        r_e1.font.bold = True
        r_e1.font.color.rgb = COLOR_NAVY
        r_e2 = p_e.add_run(desc)

    doc.add_paragraph().paragraph_format.space_after = Pt(8)

    # --------------------------------------------------------------------------
    # 4. DATA QUALITY, CLEANING & FINANCIAL RECONCILIATION SUMMARY
    # --------------------------------------------------------------------------
    h4 = doc.add_heading("4. Data Quality, Cleaning & Financial Reconciliation", level=1)
    h4.style.font.color.rgb = COLOR_NAVY
    h4.paragraph_format.space_before = Pt(14)
    h4.paragraph_format.space_after = Pt(6)

    doc.add_paragraph(
        "A foundational tenet of corporate data analytics is ensuring that transformation pipelines never alter "
        "the underlying financial truth. The cleaning script (clean_and_reconcile.py) applies deterministic keyword rules, "
        "standardizes month-end timestamps, and nets out refunds—culminating in an assertion test matching raw vs cleaned net totals."
    )

    # DQ Metrics Summary Table
    dq_tbl = doc.add_table(rows=1, cols=3)
    dq_tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    dq_widths = [Inches(3.2), Inches(2.0), Inches(1.3)]
    dq_headers = ["Data Quality Audit Metric", "Evaluated Value", "Validation Status"]

    for i, h_text in enumerate(dq_headers):
        cell = dq_tbl.cell(0, i)
        cell.width = dq_widths[i]
        set_cell_background(cell, HEX_NAVY)
        set_cell_margins(cell, top=90, bottom=90, left=100, right=100)
        format_cell_text(cell, h_text, bold=True, font_size=9, color=COLOR_WHITE)

    dq_metrics = [
        ("Total Ingested Raw Transactions", "428 Rows", "100% Ingested"),
        ("Date Range Processed", "2025-01-01 to 2025-12-31", "12 Full Months"),
        ("Month-End Boundary Timestamps (23:45 - 00:15)", "23 Transactions", "Standardised YYYY-MM"),
        ("Initial Uncategorised / Missing Categories", "28 Rows (6.54%)", "Identified"),
        ("Auto-Categorised via Merchant & Description Rules", "28 Rows (100.0%)", "100% Resolved"),
        ("Remaining Unresolved Categories in Cleaned Data", "0 Rows (0.00%)", "Zero Defects"),
        ("Total Refund Adjustments Processed", "12 Transactions", "Netted in Spend"),
        ("Total Monetary Value of Refunds", "₹13,532.50 INR", "Accurately Credited"),
        ("Raw Full-Year Net Spend", "₹934,612.02 INR", "Source Baseline"),
        ("Cleaned Full-Year Net Spend", "₹934,612.02 INR", "Reconciled Audit"),
        ("Reconciliation Variance (Cleaned - Raw)", "₹0.0000 INR", "PASSED (100% Match)")
    ]

    for row_idx, (m_name, m_val, m_stat) in enumerate(dq_metrics):
        row = dq_tbl.add_row()
        bg = HEX_ALT_BG if row_idx % 2 == 1 else "FFFFFF"
        if "PASSED" in m_stat or "Zero Defects" in m_stat or "100% Resolved" in m_stat:
            status_bg = HEX_GREEN_BG
            status_color = RGBColor(0, 97, 0)
        else:
            status_bg = bg
            status_color = COLOR_SLATE

        for c_idx, val in enumerate([m_name, m_val, m_stat]):
            cell = row.cells[c_idx]
            cell.width = dq_widths[c_idx]
            set_cell_background(cell, status_bg if c_idx == 2 else bg)
            set_cell_margins(cell, top=70, bottom=70, left=100, right=100)
            is_bold = (c_idx == 0 or "PASSED" in val)
            c_color = status_color if c_idx == 2 else COLOR_DARK
            align = WD_ALIGN_PARAGRAPH.CENTER if c_idx in [1, 2] else WD_ALIGN_PARAGRAPH.LEFT
            format_cell_text(cell, val, bold=is_bold, font_size=8.5, align=align, color=c_color)
    set_table_borders(dq_tbl)

    doc.add_paragraph().paragraph_format.space_after = Pt(8)

    # 12-Month Reconciliation Ledger Table
    p_recon_title = doc.add_paragraph()
    p_recon_title.paragraph_format.space_before = Pt(8)
    p_recon_title.paragraph_format.space_after = Pt(4)
    r_rt = p_recon_title.add_run("Table 2: 12-Month Granular Financial Reconciliation Audit Ledger")
    r_rt.font.name = "Calibri"
    r_rt.font.size = Pt(10)
    r_rt.font.bold = True
    r_rt.font.color.rgb = COLOR_NAVY

    recon_tbl = doc.add_table(rows=1, cols=7)
    recon_tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    recon_widths = [Inches(1.0), Inches(0.9), Inches(0.9), Inches(1.0), Inches(0.9), Inches(0.8), Inches(1.0)]
    recon_headers = ["Month", "Raw Gross", "Raw Refund", "Raw Net", "Clean Net", "Variance", "Audit Status"]

    for i, h_text in enumerate(recon_headers):
        cell = recon_tbl.cell(0, i)
        cell.width = recon_widths[i]
        set_cell_background(cell, HEX_NAVY)
        set_cell_margins(cell, top=80, bottom=80, left=60, right=60)
        format_cell_text(cell, h_text, bold=True, font_size=8, color=COLOR_WHITE, align=WD_ALIGN_PARAGRAPH.CENTER)

    monthly_recon_data = [
        ("2025-01", "₹70,861.77", "-₹1,499.00", "₹69,362.77", "₹69,362.77", "₹0.00", "MATCH"),
        ("2025-02", "₹59,455.63", "-₹450.50", "₹59,005.13", "₹59,005.13", "₹0.00", "MATCH"),
        ("2025-03", "₹73,413.44", "-₹2,199.00", "₹71,214.44", "₹71,214.44", "₹0.00", "MATCH"),
        ("2025-04", "₹86,692.19", "-₹110.00", "₹86,582.19", "₹86,582.19", "₹0.00", "MATCH"),
        ("2025-05", "₹57,406.25", "-₹720.00", "₹56,686.25", "₹56,686.25", "₹0.00", "MATCH"),
        ("2025-06", "₹94,815.51", "-₹320.00", "₹94,495.51", "₹94,495.51", "₹0.00", "MATCH"),
        ("2025-07", "₹54,220.54", "-₹1,850.00", "₹52,370.54", "₹52,370.54", "₹0.00", "MATCH"),
        ("2025-08", "₹54,727.11", "-₹799.00", "₹53,928.11", "₹53,928.11", "₹0.00", "MATCH"),
        ("2025-09", "₹131,161.96", "-₹3,450.00", "₹127,711.96", "₹127,711.96", "₹0.00", "MATCH"),
        ("2025-10", "₹96,182.95", "-₹600.00", "₹95,582.95", "₹95,582.95", "₹0.00", "MATCH"),
        ("2025-11", "₹75,714.65", "-₹285.00", "₹75,429.65", "₹75,429.65", "₹0.00", "MATCH"),
        ("2025-12", "₹93,492.52", "-₹1,250.00", "₹92,242.52", "₹92,242.52", "₹0.00", "MATCH"),
        ("FULL YEAR", "₹948,144.52", "-₹13,532.50", "₹934,612.02", "₹934,612.02", "₹0.00", "RECONCILED")
    ]

    for row_idx, r_vals in enumerate(monthly_recon_data):
        row = recon_tbl.add_row()
        is_summary = (row_idx == len(monthly_recon_data) - 1)
        bg = HEX_NAVY if is_summary else (HEX_ALT_BG if row_idx % 2 == 1 else "FFFFFF")
        text_color = COLOR_WHITE if is_summary else COLOR_DARK

        for c_idx, val in enumerate(r_vals):
            cell = row.cells[c_idx]
            cell.width = recon_widths[c_idx]
            set_cell_background(cell, bg)
            set_cell_margins(cell, top=60, bottom=60, left=60, right=60)
            align = WD_ALIGN_PARAGRAPH.CENTER if c_idx in [0, 6] else WD_ALIGN_PARAGRAPH.RIGHT
            format_cell_text(cell, val, bold=is_summary, font_size=8, align=align, color=text_color)
    set_table_borders(recon_tbl)

    doc.add_paragraph().paragraph_format.space_after = Pt(10)

    # --------------------------------------------------------------------------
    # 5. KEY INSIGHTS & BUDGET BREACH AUDIT
    # --------------------------------------------------------------------------
    h5 = doc.add_heading("5. Key Spending Insights & Automated Budget Breach Audit", level=1)
    h5.style.font.color.rgb = COLOR_NAVY
    h5.paragraph_format.space_before = Pt(14)
    h5.paragraph_format.space_after = Pt(6)

    doc.add_paragraph(
        "Analysis of the audited 12-month transaction ledger revealed actionable macroeconomic and lifestyle spending patterns:"
    )

    doc.add_paragraph(
        "• Top Category Outflows: Housing & Maintenance constituted the single largest expenditure category at ₹244,526.25 (26.16%), "
        "driven by residential rent and quarterly society charges. Shopping ranked second at ₹197,336.29 (21.11%), followed by Groceries at "
        "₹189,607.86 (20.29%). Combined, these three categories account for 67.56% of total annual spend.",
        style='Normal'
    )
    doc.add_paragraph(
        "• Seasonal Outflow Spike: September registered the annual peak in net spending at ₹127,711.96 (+36.6% above full-year monthly average), "
        "driven by Great Indian Festival eCommerce purchases and advance festive preparations.",
        style='Normal'
    )
    doc.add_paragraph(
        "• Asymmetric Refund Dynamics: E-commerce shopping accounted for ₹8,998.00 in refunds (66.5% of all refund volume), demonstrating "
        "high return friction in online apparel and consumer electronics.",
        style='Normal'
    )
    doc.add_paragraph(
        "• Cashless Dominance: Digital payment rails accounted for 95.3% of transaction count (UPI: 45.2%, Credit Cards: 30.1%, Net Banking: 12.0%, "
        "Debit Cards: 8.0%), with physical cash representing under 4.7% of volume.",
        style='Normal'
    )

    # Category Spend Table
    cat_summary_rows = [
        ("Housing & Maintenance", "Essential", "15", "₹244,526.25", "26.16%"),
        ("Shopping", "Discretionary", "55", "₹197,336.29", "21.11%"),
        ("Groceries", "Essential", "95", "₹189,607.86", "20.29%"),
        ("Utilities & Bills", "Essential", "51", "₹98,684.02", "10.56%"),
        ("Food & Dining", "Essential", "97", "₹94,202.87", "10.08%"),
        ("Transportation", "Essential", "65", "₹53,651.79", "5.74%"),
        ("Healthcare & Wellness", "Essential", "25", "₹37,538.81", "4.02%"),
        ("Entertainment & Leisure", "Discretionary", "25", "₹19,064.13", "2.04%"),
        ("TOTAL OUTFLOW", "All Categories", "428", "₹934,612.02", "100.00%")
    ]

    cat_tbl = doc.add_table(rows=1, cols=5)
    cat_tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    cat_widths = [Inches(2.0), Inches(1.3), Inches(0.8), Inches(1.3), Inches(1.1)]
    cat_headers = ["Category Name", "Classification", "Txn Count", "Net Spend (INR)", "Share of Spend"]

    for i, h_text in enumerate(cat_headers):
        cell = cat_tbl.cell(0, i)
        cell.width = cat_widths[i]
        set_cell_background(cell, HEX_NAVY)
        set_cell_margins(cell, top=80, bottom=80, left=80, right=80)
        format_cell_text(cell, h_text, bold=True, font_size=8.5, color=COLOR_WHITE, align=WD_ALIGN_PARAGRAPH.CENTER)

    for row_idx, r_vals in enumerate(cat_summary_rows):
        row = cat_tbl.add_row()
        is_total = (row_idx == len(cat_summary_rows) - 1)
        bg = HEX_NAVY if is_total else (HEX_ALT_BG if row_idx % 2 == 1 else "FFFFFF")
        text_color = COLOR_WHITE if is_total else COLOR_DARK

        for c_idx, val in enumerate(r_vals):
            cell = row.cells[c_idx]
            cell.width = cat_widths[c_idx]
            set_cell_background(cell, bg)
            set_cell_margins(cell, top=60, bottom=60, left=80, right=80)
            align = WD_ALIGN_PARAGRAPH.RIGHT if c_idx in [2, 3, 4] else WD_ALIGN_PARAGRAPH.LEFT
            format_cell_text(cell, val, bold=is_total, font_size=8.5, align=align, color=text_color)
    set_table_borders(cat_tbl)

    doc.add_paragraph().paragraph_format.space_after = Pt(10)

    # Budget Breach Audit Table
    p_alert_head = doc.add_paragraph()
    p_alert_head.paragraph_format.space_before = Pt(8)
    p_alert_head.paragraph_format.space_after = Pt(4)
    r_ah = p_alert_head.add_run("Oracle PL/SQL Stored Procedure Automated Breach Results (BUDGET_ALERTS Table):")
    r_ah.font.name = "Calibri"
    r_ah.font.size = Pt(10)
    r_ah.font.bold = True
    r_ah.font.color.rgb = COLOR_NAVY

    alert_rows = [
        ("2025-01", "Food & Dining", "₹10,743.60", "₹8,500.00", "+₹2,243.60", "+26.40%", "CRITICAL"),
        ("2025-01", "Shopping", "₹9,793.93", "₹8,000.00", "+₹1,793.93", "+22.42%", "CRITICAL"),
        ("2025-01", "Entertainment & Leisure", "₹1,640.41", "₹1,500.00", "+₹140.41", "+9.36%", "WARNING"),
        ("2025-02", "Shopping", "₹24,403.71", "₹15,000.00", "+₹9,403.71", "+62.69%", "CRITICAL"),
        ("2025-02", "Healthcare & Wellness", "₹3,074.43", "₹3,000.00", "+₹74.43", "+2.48%", "WARNING")
    ]

    alert_tbl = doc.add_table(rows=1, cols=7)
    alert_tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    alert_widths = [Inches(0.8), Inches(1.6), Inches(0.9), Inches(0.8), Inches(0.9), Inches(0.7), Inches(0.8)]
    alert_headers = ["Period", "Category", "Actual Spend", "Budget", "Overrun", "% Over", "Severity"]

    for i, h_text in enumerate(alert_headers):
        cell = alert_tbl.cell(0, i)
        cell.width = alert_widths[i]
        set_cell_background(cell, HEX_NAVY)
        set_cell_margins(cell, top=80, bottom=80, left=60, right=60)
        format_cell_text(cell, h_text, bold=True, font_size=8, color=COLOR_WHITE, align=WD_ALIGN_PARAGRAPH.CENTER)

    for row_idx, r_vals in enumerate(alert_rows):
        row = alert_tbl.add_row()
        sev = r_vals[6]
        sev_bg = "FEE2E2" if sev == "CRITICAL" else "FEF3C7"
        sev_text_color = RGBColor(185, 28, 28) if sev == "CRITICAL" else RGBColor(180, 83, 9)
        row_bg = HEX_ALT_BG if row_idx % 2 == 1 else "FFFFFF"

        for c_idx, val in enumerate(r_vals):
            cell = row.cells[c_idx]
            cell.width = alert_widths[c_idx]
            cell_bg = sev_bg if c_idx == 6 else row_bg
            set_cell_background(cell, cell_bg)
            set_cell_margins(cell, top=60, bottom=60, left=60, right=60)
            align = WD_ALIGN_PARAGRAPH.CENTER if c_idx in [0, 5, 6] else (WD_ALIGN_PARAGRAPH.RIGHT if c_idx in [2, 3, 4] else WD_ALIGN_PARAGRAPH.LEFT)
            text_c = sev_text_color if c_idx == 6 else COLOR_DARK
            format_cell_text(cell, val, bold=(c_idx in [1, 6]), font_size=8, align=align, color=text_c)
    set_table_borders(alert_tbl)

    doc.add_paragraph().paragraph_format.space_after = Pt(12)

    # --------------------------------------------------------------------------
    # 6. DEDICATED PLACEHOLDER SECTIONS FOR MEDIA & SCREENSHOTS
    # --------------------------------------------------------------------------
    h6 = doc.add_heading("6. Execution Evidence & Dashboard Placeholders", level=1)
    h6.style.font.color.rgb = COLOR_NAVY
    h6.paragraph_format.space_before = Pt(14)
    h6.paragraph_format.space_after = Pt(6)

    doc.add_paragraph(
        "Below are dedicated placeholder sections styled to facilitate attaching execution screenshots, "
        "interactive dashboard visual captures, source repository links, and video walkthroughs:"
    )

    # Placeholder 1: Oracle PL/SQL Output
    add_placeholder_box(
        doc,
        placeholder_tag="[INSERT ORACLE PL/SQL OUTPUT SCREENSHOT]",
        description="Insert screenshot of Oracle SQL Developer or Oracle Live SQL terminal executing sql/03_views_and_plsql.sql. "
                    "Ensure DBMS_OUTPUT logs for PRC_EVALUATE_BUDGET_ALERTS and the final SELECT from BUDGET_ALERTS are visible.",
        icon="🗄️"
    )

    # Placeholder 2: Power BI Dashboard Screenshot
    add_placeholder_box(
        doc,
        placeholder_tag="[INSERT POWER BI DASHBOARD SCREENSHOT]",
        description="Insert high-resolution visual capture of the Power BI Personal Expense & Budget Dashboard. "
                    "Include KPI Summary Cards (Net Spend ₹934.6K, Refunds ₹13.5K), Category Spend Donut, Spend vs Budget Variance Matrix, and Monthly Outflow Trend.",
        icon="📊"
    )

    # Placeholder 3: GitHub Repository Link
    add_placeholder_box(
        doc,
        placeholder_tag="[GITHUB REPO LINK]",
        description="Paste public or enterprise GitHub project repository URL here.\n"
                    "e.g., https://github.com/<your-username>/personal-expense-budget-tracker",
        icon="🔗"
    )

    # Placeholder 4: Demo Video Link
    add_placeholder_box(
        doc,
        placeholder_tag="[DEMO VIDEO LINK]",
        description="Paste Loom / YouTube unlisted walkthrough video link demonstrating data generation, "
                    "Python reconciliation execution, Oracle PL/SQL procedure execution, and interactive Power BI report slicing.\n"
                    "e.g., https://www.loom.com/share/<your-demo-video-id>",
        icon="🎥"
    )

    # --------------------------------------------------------------------------
    # 7. PROJECT REPOSITORY & ARTIFACT DIRECTORY STRUCTURE
    # --------------------------------------------------------------------------
    h7 = doc.add_heading("7. Repository Structure & Deliverables Catalog", level=1)
    h7.style.font.color.rgb = COLOR_NAVY
    h7.paragraph_format.space_before = Pt(14)
    h7.paragraph_format.space_after = Pt(6)

    doc.add_paragraph(
        "The project workspace is organized in accordance with production analytics standards:"
    )

    code_tbl = doc.add_table(rows=1, cols=1)
    code_tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    c_cell = code_tbl.cell(0, 0)
    c_cell.width = Inches(6.5)
    set_cell_background(c_cell, "1E293B")
    set_cell_margins(c_cell, top=140, bottom=140, left=180, right=180)

    dir_text = (
        "expense-budget-tracker/\n"
        "│\n"
        "├── data/\n"
        "│   ├── raw_expenses.csv              # 428 raw simulated transactions with 3 edge cases\n"
        "│   ├── cleaned_expenses.csv          # Reconciled clean dataset with parsed dimensions\n"
        "│   └── reconciliation_dq_report.xlsx # Formatted 3-sheet audit report with 0.00 variance\n"
        "│\n"
        "├── scripts/\n"
        "│   ├── generate_data.py              # Synthetic Indian personal expense generator\n"
        "│   ├── clean_and_reconcile.py        # Python ETL, regex categorization & assertion engine\n"
        "│   ├── generate_schema_diagram.py    # Matplotlib star-schema PNG generator\n"
        "│   └── generate_docx_report.py       # Automated python-docx project documentation\n"
        "│\n"
        "├── sql/\n"
        "│   ├── 01_ddl.sql                    # Oracle Star-Schema DDL (DIM, FACT, ALERTS)\n"
        "│   ├── 02_load.sql                   # Clean 61-row seed dataset with calibrated breaches\n"
        "│   └── 03_views_and_plsql.sql        # Analytical view, SQL queries & PL/SQL alert engine\n"
        "│\n"
        "├── docs/\n"
        "│   ├── star_schema.png               # High-res 300 DPI dimensional entity relationship diagram\n"
        "│   └── Personal_Expense_Project_Report.docx # Comprehensive executive case study deliverable\n"
        "│\n"
        "├── dashboard/\n"
        "│   ├── power_bi_template_guide.md    # Step-by-step DAX formulas, visual matrix & theme guide\n"
        "│   └── pbi_schema_and_dax.sql        # Reference SQL/DAX code snippets for dashboarding\n"
        "│\n"
        "└── README.md                         # Full project overview, architecture & setup guide"
    )
    p_code = c_cell.paragraphs[0]
    p_code.paragraph_format.space_before = Pt(0)
    p_code.paragraph_format.space_after = Pt(0)
    r_code = p_code.add_run(dir_text)
    r_code.font.name = "Consolas"
    r_code.font.size = Pt(8.5)
    r_code.font.color.rgb = RGBColor(226, 232, 240)

    doc.add_paragraph().paragraph_format.space_after = Pt(14)

    # Save document
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    doc.save(output_path)
    print(f"Personal Expense Project Report successfully written to: {output_path}")

if __name__ == "__main__":
    build_report()
