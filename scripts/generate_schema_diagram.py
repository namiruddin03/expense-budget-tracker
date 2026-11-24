"""
Star Schema Diagram Generator for Personal Expense Tracker
Generates a crisp, publication-quality entity relationship star schema diagram (docs/star_schema.png).
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
import os

def generate_star_schema_diagram(output_path="docs/star_schema.png"):
    fig, ax = plt.subplots(figsize=(14, 10), dpi=300)
    ax.set_xlim(0, 14)
    ax.set_ylim(0, 10)
    ax.axis("off")

    # Background color
    fig.patch.set_facecolor("#F8FAFC")
    ax.set_facecolor("#F8FAFC")

    # Title Banner
    ax.text(7.0, 9.55, "Personal Expense Tracker - Star Schema Architecture", 
            ha="center", va="center", fontsize=18, fontweight="bold", color="#0F172A", fontfamily="sans-serif")
    ax.text(7.0, 9.20, "Oracle Enterprise Data Model | Fact, Dimension & Budget Alert Tables", 
            ha="center", va="center", fontsize=11, color="#475569", fontfamily="sans-serif")

    # Helper function to draw table box
    def draw_table(x, y, w, h, title, cols, header_bg, border_color="#CBD5E1"):
        # Outer Card Box
        card = patches.FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.08,rounding_size=0.15",
                                      facecolor="#FFFFFF", edgecolor=border_color, linewidth=1.5, zorder=2)
        ax.add_patch(card)
        
        # Header Box
        header_h = 0.58
        header = patches.FancyBboxPatch((x, y + h - header_h), w, header_h,
                                        boxstyle="round,pad=0.08,rounding_size=0.15",
                                        facecolor=header_bg, edgecolor=header_bg, linewidth=1, zorder=3)
        ax.add_patch(header)
        
        # Header square patch to clip bottom roundings of header
        header_clip = patches.Rectangle((x, y + h - header_h), w, 0.2,
                                        facecolor=header_bg, edgecolor=header_bg, zorder=3)
        ax.add_patch(header_clip)

        # Title Text
        ax.text(x + w / 2.0, y + h - header_h / 2.0, title,
                ha="center", va="center", fontsize=11, fontweight="bold", color="#FFFFFF", zorder=4)

        # Separator line
        ax.plot([x, x + w], [y + h - header_h, y + h - header_h], color=border_color, lw=1, zorder=4)

        # Draw Columns
        curr_y = y + h - header_h - 0.28
        for col_name, col_type, key_type in cols:
            # Key badge
            if key_type == "PK":
                badge_bg = "#EF4444"  # Red
                badge_text = "PK"
            elif key_type == "FK":
                badge_bg = "#3B82F6"  # Blue
                badge_text = "FK"
            elif key_type == "UK":
                badge_bg = "#8B5CF6"  # Purple
                badge_text = "UK"
            else:
                badge_bg = None
                badge_text = ""

            if badge_bg:
                b_patch = patches.FancyBboxPatch((x + 0.15, curr_y - 0.10), 0.5, 0.22,
                                                 boxstyle="round,pad=0.02,rounding_size=0.05",
                                                 facecolor=badge_bg, edgecolor="none", zorder=4)
                ax.add_patch(b_patch)
                ax.text(x + 0.40, curr_y + 0.01, badge_text,
                        ha="center", va="center", fontsize=7.5, fontweight="bold", color="#FFFFFF", zorder=5)

            # Col name
            txt_x = x + 0.75 if badge_bg else x + 0.25
            font_weight = "bold" if key_type in ["PK", "FK"] else "normal"
            text_color = "#0F172A" if font_weight == "bold" else "#334155"
            ax.text(txt_x, curr_y + 0.01, col_name, ha="left", va="center",
                    fontsize=8.5, fontweight=font_weight, color=text_color, zorder=4)

            # Col type
            ax.text(x + w - 0.20, curr_y + 0.01, col_type, ha="right", va="center",
                    fontsize=7.8, color="#64748B", zorder=4, style="italic")

            curr_y -= 0.27

    # 1. DIM_CATEGORY (Top-Left)
    cat_cols = [
        ("CATEGORY_ID", "NUMBER", "PK"),
        ("CATEGORY_NAME", "VARCHAR2(50)", "UK"),
        ("CATEGORY_GROUP", "VARCHAR2(50)", ""),
        ("DESCRIPTION", "VARCHAR2(200)", ""),
        ("IS_ACTIVE", "NUMBER(1)", "")
    ]
    draw_table(0.8, 5.5, 3.6, 2.3, "DIM_CATEGORY (Dimension)", cat_cols, "#1E3A8A")

    # 2. DIM_BUDGET (Top-Right)
    budget_cols = [
        ("BUDGET_ID", "NUMBER", "PK"),
        ("YEAR_MONTH", "VARCHAR2(7)", "UK"),
        ("CATEGORY_ID", "NUMBER", "FK"),
        ("BUDGET_AMOUNT", "NUMBER(12,2)", ""),
        ("CREATED_DATE", "DATE", "")
    ]
    draw_table(9.6, 5.5, 3.6, 2.3, "DIM_BUDGET (Dimension)", budget_cols, "#0D9488")

    # 3. FACT_EXPENSES (Center Core)
    fact_cols = [
        ("TRANSACTION_ID", "VARCHAR2(20)", "PK"),
        ("TRANSACTION_DATE", "TIMESTAMP", ""),
        ("YEAR_MONTH", "VARCHAR2(7)", ""),
        ("CATEGORY_ID", "NUMBER", "FK"),
        ("MERCHANT", "VARCHAR2(100)", ""),
        ("DESCRIPTION", "VARCHAR2(255)", ""),
        ("PAYMENT_MODE", "VARCHAR2(30)", ""),
        ("TRANSACTION_TYPE", "VARCHAR2(20)", ""),
        ("RAW_AMOUNT", "NUMBER(12,2)", ""),
        ("NET_AMOUNT", "NUMBER(12,2)", ""),
        ("IS_AUTO_CATEGORISED", "NUMBER(1)", ""),
        ("CREATED_AT", "DATE", "")
    ]
    draw_table(4.7, 2.0, 4.6, 4.2, "FACT_EXPENSES (Central Fact)", fact_cols, "#1E293B")

    # 4. BUDGET_ALERTS (Bottom-Right)
    alert_cols = [
        ("ALERT_ID", "NUMBER", "PK"),
        ("YEAR_MONTH", "VARCHAR2(7)", ""),
        ("CATEGORY_ID", "NUMBER", "FK"),
        ("ACTUAL_SPEND", "NUMBER(12,2)", ""),
        ("BUDGET_AMOUNT", "NUMBER(12,2)", ""),
        ("VARIANCE_AMOUNT", "NUMBER(12,2)", ""),
        ("VARIANCE_PCT", "NUMBER(5,2)", ""),
        ("SEVERITY", "VARCHAR2(20)", ""),
        ("ALERT_MESSAGE", "VARCHAR2(500)", ""),
        ("GENERATED_AT", "TIMESTAMP", "")
    ]
    draw_table(9.6, 1.0, 3.6, 3.6, "BUDGET_ALERTS (Breach Audit)", alert_cols, "#B91C1C")

    # 5. VW_MONTHLY_SPEND_VS_BUDGET (Bottom-Left Analytic View Box)
    view_cols = [
        ("YEAR_MONTH", "VARCHAR2(7)", ""),
        ("CATEGORY_NAME", "VARCHAR2(50)", ""),
        ("CATEGORY_GROUP", "VARCHAR2(50)", ""),
        ("MONTHLY_BUDGET", "NUMBER(12,2)", ""),
        ("ACTUAL_NET_SPEND", "NUMBER(12,2)", ""),
        ("SPEND_VARIANCE", "NUMBER(12,2)", ""),
        ("UTILISATION_PCT", "NUMBER(6,2)", ""),
        ("BUDGET_STATUS", "VARCHAR2(30)", "")
    ]
    draw_table(0.8, 1.4, 3.6, 3.2, "VW_MONTHLY_SPEND_VS_BUDGET", view_cols, "#475569")

    # Connectors & Relationships
    # (1) DIM_CATEGORY to FACT_EXPENSES
    # Line from (4.4, 6.4) to (4.7, 5.0)
    ax.annotate("", xy=(4.7, 5.2), xytext=(4.4, 6.4),
                arrowprops=dict(arrowstyle="-|>", color="#1E3A8A", lw=2.2, mutation_scale=15))
    ax.text(4.45, 6.55, "1", fontsize=10, fontweight="bold", color="#1E3A8A")
    ax.text(4.55, 5.28, "N", fontsize=10, fontweight="bold", color="#1E3A8A")
    ax.text(3.9, 5.75, "FK: CATEGORY_ID", fontsize=7.5, color="#1E3A8A", fontweight="bold", rotation=-24)

    # (2) DIM_CATEGORY to DIM_BUDGET
    # Horizontal line from (4.4, 6.9) to (9.6, 6.9)
    ax.plot([4.4, 9.6], [6.9, 6.9], color="#0D9488", lw=1.8, linestyle="--")
    ax.annotate("", xy=(9.6, 6.9), xytext=(4.4, 6.9),
                arrowprops=dict(arrowstyle="-|>", color="#0D9488", lw=2.0, mutation_scale=15))
    ax.text(4.5, 7.05, "1", fontsize=10, fontweight="bold", color="#0D9488")
    ax.text(9.45, 7.05, "N", fontsize=10, fontweight="bold", color="#0D9488")
    ax.text(6.6, 7.05, "FK: CATEGORY_ID", fontsize=8, color="#0D9488", fontweight="bold", ha="center")

    # (3) FACT_EXPENSES & DIM_BUDGET to BUDGET_ALERTS (PL/SQL Evaluation Engine)
    # Line from FACT_EXPENSES (9.3, 3.5) to BUDGET_ALERTS (9.6, 3.5)
    ax.annotate("", xy=(9.6, 3.5), xytext=(9.3, 3.5),
                arrowprops=dict(arrowstyle="-|>", color="#B91C1C", lw=2.0, mutation_scale=15))
    ax.text(9.45, 3.65, "N", fontsize=9, fontweight="bold", color="#B91C1C")

    # Line from DIM_BUDGET (11.4, 5.5) to BUDGET_ALERTS (11.4, 4.6)
    ax.annotate("", xy=(11.4, 4.6), xytext=(11.4, 5.5),
                arrowprops=dict(arrowstyle="-|>", color="#B91C1C", lw=2.0, mutation_scale=15))
    ax.text(11.5, 4.95, "PL/SQL Breach Check", fontsize=7.5, color="#B91C1C", fontweight="bold")

    # (4) FACT_EXPENSES to Analytic View
    ax.annotate("", xy=(4.4, 3.0), xytext=(4.7, 3.0),
                arrowprops=dict(arrowstyle="-|>", color="#475569", lw=1.8, linestyle=":", mutation_scale=14))
    ax.text(4.0, 3.15, "Aggregates to View", fontsize=7.5, color="#475569", style="italic")

    # Legend / Key
    legend_bg = patches.FancyBboxPatch((0.8, 0.2), 12.4, 0.6,
                                       boxstyle="round,pad=0.05,rounding_size=0.08",
                                       facecolor="#FFFFFF", edgecolor="#CBD5E1", lw=1)
    ax.add_patch(legend_bg)
    ax.text(1.2, 0.5, "Schema Legend:", fontsize=8.5, fontweight="bold", color="#0F172A", va="center")
    
    # Legend PK
    p1 = patches.FancyBboxPatch((2.4, 0.40), 0.4, 0.2, boxstyle="round,pad=0.01", facecolor="#EF4444", edgecolor="none")
    ax.add_patch(p1)
    ax.text(2.6, 0.5, "PK", color="white", fontsize=7, fontweight="bold", ha="center", va="center")
    ax.text(2.9, 0.5, "Primary Key", fontsize=8, color="#334155", va="center")

    # Legend FK
    p2 = patches.FancyBboxPatch((4.2, 0.40), 0.4, 0.2, boxstyle="round,pad=0.01", facecolor="#3B82F6", edgecolor="none")
    ax.add_patch(p2)
    ax.text(4.4, 0.5, "FK", color="white", fontsize=7, fontweight="bold", ha="center", va="center")
    ax.text(4.7, 0.5, "Foreign Key", fontsize=8, color="#334155", va="center")

    # Legend UK
    p3 = patches.FancyBboxPatch((6.0, 0.40), 0.4, 0.2, boxstyle="round,pad=0.01", facecolor="#8B5CF6", edgecolor="none")
    ax.add_patch(p3)
    ax.text(6.2, 0.5, "UK", color="white", fontsize=7, fontweight="bold", ha="center", va="center")
    ax.text(6.5, 0.5, "Unique Constraint", fontsize=8, color="#334155", va="center")

    # Card
    ax.text(8.2, 0.5, "Cardinality: 1 : N (One-to-Many Relationships)", fontsize=8, color="#475569", va="center")
    ax.text(12.6, 0.5, "Dialect: Oracle 19c / 21c / 23ai", fontsize=8, color="#64748B", ha="right", va="center", style="italic")

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    plt.tight_layout()
    plt.savefig(output_path, dpi=300, facecolor=fig.get_facecolor(), edgecolor="none")
    plt.close()
    print(f"Star-Schema diagram successfully saved to '{output_path}'.")

if __name__ == "__main__":
    generate_star_schema_diagram()
