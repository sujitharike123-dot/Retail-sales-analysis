"""Retail sales analysis: cleaning (Pandas), SQL exploration (SQLite) and charts (Matplotlib).

Usage (from the repo root):
    python src/sales_analysis.py                    # uses data/train.csv
    python src/sales_analysis.py path/to/file.csv   # explicit file

Expects the "Superstore Sales Dataset" train.csv (Kaggle): 9,800 order lines, 2015-2018.
Note: this file has no Profit, Discount or Quantity columns, so the analysis is about sales and customers.
"""
import json
import os
import sqlite3
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
FIG, RES, SQL, DATA = (os.path.join(ROOT, d) for d in ("figures", "results", "sql", "data"))
sns.set_theme(style="whitegrid")
BLUE, GREY = "#2b6cb0", "#a0aec0"

# ------------------------------------------------------------------ 1. load
path = sys.argv[1] if len(sys.argv) > 1 else os.path.join(DATA, "train.csv")
if not os.path.exists(path):
    sys.exit("Missing data/train.csv - download the Superstore Sales Dataset from Kaggle (see README).")
raw = pd.read_csv(path)
print(f"Loaded {len(raw):,} rows x {raw.shape[1]} cols from {os.path.relpath(path, ROOT)}")

# ------------------------------------------------------------------ 2. clean
df = raw.copy()
df["Order Date"] = pd.to_datetime(df["Order Date"], format="%d/%m/%Y")
df["Ship Date"] = pd.to_datetime(df["Ship Date"], format="%d/%m/%Y")
cols_wo_id = [c for c in df.columns if c != "Row ID"]
exact_dupes = int(df.duplicated(subset=cols_wo_id).sum())
df = df.drop_duplicates(subset=cols_wo_id).copy()

missing_postal = int(df["Postal Code"].isna().sum())
fix = df["Postal Code"].isna() & (df["City"] == "Burlington") & (df["State"] == "Vermont")
df.loc[fix, "Postal Code"] = 5401  # Burlington, VT ZIP code 05401
still_missing = int(df["Postal Code"].isna().sum())
df["Postal Code"] = df["Postal Code"].fillna(0).astype(int).astype(str).str.zfill(5)

df["Order Year"] = df["Order Date"].dt.year
df["Order Month"] = df["Order Date"].dt.to_period("M").dt.to_timestamp()
df["Days to Ship"] = (df["Ship Date"] - df["Order Date"]).dt.days
assert (df["Days to Ship"] >= 0).all(), "found ship dates before order dates"
print(f"Cleaning: {exact_dupes} exact duplicate row dropped, {missing_postal} missing postal codes "
      f"({missing_postal - still_missing} filled), dates parsed as DD/MM/YYYY -> {len(df):,} rows")

# ------------------------------------------------------------------ 3. SQL exploration
sql_df = df.rename(columns=lambda c: c.lower().replace(" ", "_").replace("-", "_"))
sql_df["order_date"] = sql_df["order_date"].dt.strftime("%Y-%m-%d")
sql_df["ship_date"] = sql_df["ship_date"].dt.strftime("%Y-%m-%d")
sql_df["order_month"] = sql_df["order_month"].dt.strftime("%Y-%m")
con = sqlite3.connect(":memory:")
sql_df.to_sql("sales", con, index=False)
with open(os.path.join(SQL, "sales_queries.sql")) as f:
    blocks = [b.strip() for b in f.read().split("-- QUERY:")[1:] if b.strip()]  # [0] is the file header
sql_out = {}
for b in blocks:
    title, _, query = b.partition("\n")
    sql_out[title.strip()] = pd.read_sql_query(query, con)
    print(f"\n[SQL] {title.strip()}\n{sql_out[title.strip()].head(6).to_string(index=False)}")
with open(os.path.join(RES, "sql_results.md"), "w") as f:
    for title, res in sql_out.items():
        f.write(f"### {title}\n\n{res.to_markdown(index=False)}\n\n")

# ------------------------------------------------------------------ 4. charts
total_sales = float(df["Sales"].sum())

# yearly sales with YoY labels
yr = df.groupby("Order Year")["Sales"].sum()
yoy = yr.pct_change() * 100
fig, ax = plt.subplots(figsize=(6.5, 4))
bars = ax.bar(yr.index.astype(str), yr.values / 1e3, color=BLUE)
for b_, g in zip(bars, yoy):
    label = f"{b_.get_height():,.0f}K" + ("" if np.isnan(g) else f"\n({g:+.1f}%)")
    ax.text(b_.get_x() + b_.get_width() / 2, b_.get_height() + 8, label, ha="center", fontsize=9)
ax.set_ylabel("Sales (thousands $)"); ax.set_title("Yearly sales and year-over-year growth")
ax.set_ylim(0, yr.max() / 1e3 * 1.18)
plt.tight_layout(); plt.savefig(os.path.join(FIG, "yearly_sales.png"), dpi=130); plt.close()

# monthly trend + 3-month moving average
mo = df.groupby("Order Month")["Sales"].sum()
plt.figure(figsize=(9, 4))
plt.plot(mo.index, mo.values / 1e3, color=GREY, marker="o", ms=3, label="Monthly sales")
plt.plot(mo.index, mo.rolling(3).mean() / 1e3, color=BLUE, lw=2.2, label="3-month moving average")
plt.ylabel("Sales (thousands $)"); plt.title("Monthly sales trend, 2015-2018"); plt.legend()
plt.tight_layout(); plt.savefig(os.path.join(FIG, "monthly_trend.png"), dpi=130); plt.close()

# seasonality
cal = df.groupby(df["Order Date"].dt.month)["Sales"].sum()
share = cal / cal.sum() * 100
plt.figure(figsize=(7.5, 4))
cols = [BLUE if s >= share.nlargest(3).min() else GREY for s in share.values]
plt.bar(["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"], share.values, color=cols)
plt.ylabel("Share of total sales (%)"); plt.title("Seasonality: share of sales by calendar month (top 3 highlighted)")
plt.tight_layout(); plt.savefig(os.path.join(FIG, "seasonality.png"), dpi=130); plt.close()

# category / sub-category
sub = df.groupby(["Category", "Sub-Category"])["Sales"].sum().reset_index().sort_values("Sales")
palette = {"Furniture": "#2b6cb0", "Office Supplies": "#dd6b20", "Technology": "#2f855a"}
plt.figure(figsize=(7.5, 6))
plt.barh(sub["Sub-Category"], sub["Sales"] / 1e3, color=[palette[c] for c in sub["Category"]])
handles = [plt.Rectangle((0, 0), 1, 1, color=v) for v in palette.values()]
plt.legend(handles, palette.keys(), loc="lower right"); plt.xlabel("Sales (thousands $)")
plt.title("Sales by sub-category")
plt.tight_layout(); plt.savefig(os.path.join(FIG, "category_subcategory.png"), dpi=130); plt.close()

# region and top states
reg = df.groupby("Region")["Sales"].sum().sort_values()
st = df.groupby("State")["Sales"].sum().nlargest(10).sort_values()
fig, ax = plt.subplots(1, 2, figsize=(12, 4.2))
ax[0].barh(reg.index, reg.values / 1e3, color=BLUE); ax[0].set_title("Sales by region"); ax[0].set_xlabel("Sales (thousands $)")
ax[1].barh(st.index, st.values / 1e3, color=BLUE); ax[1].set_title("Top 10 states by sales"); ax[1].set_xlabel("Sales (thousands $)")
plt.tight_layout(); plt.savefig(os.path.join(FIG, "region_and_states.png"), dpi=130); plt.close()

# customer concentration
q = sql_out["Customer concentration - sales by customer quintile (NTILE)"]
plt.figure(figsize=(6.5, 4))
plt.bar(["Top 20%", "20-40%", "40-60%", "60-80%", "Bottom 20%"], q["pct_of_sales"], color=BLUE)
for i, v in enumerate(q["pct_of_sales"]):
    plt.text(i, v + 0.6, f"{v:.1f}%", ha="center", fontsize=9)
plt.ylabel("Share of total sales (%)"); plt.title("Customer concentration: sales by customer group")
plt.tight_layout(); plt.savefig(os.path.join(FIG, "customer_concentration.png"), dpi=130); plt.close()

# ------------------------------------------------------------------ 5. key numbers for the README
orders = df["Order ID"].nunique()
order_val = df.groupby("Order ID")["Sales"].sum()
best_cal = share.sort_values(ascending=False)
cat = df.groupby("Category")["Sales"].sum().sort_values(ascending=False)
subs = df.groupby("Sub-Category")["Sales"].sum().sort_values(ascending=False)
top_prod = df.groupby("Product Name")["Sales"].sum().nlargest(1)
names = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
summary = {
    "rows_loaded": int(len(raw)), "rows_after_cleaning": int(len(df)), "exact_duplicates_dropped": exact_dupes,
    "missing_postal_codes_filled": missing_postal - still_missing,
    "date_range": [str(df["Order Date"].min().date()), str(df["Order Date"].max().date())],
    "orders": int(orders), "customers": int(df["Customer ID"].nunique()), "products": int(df["Product ID"].nunique()),
    "total_sales": round(total_sales, 2), "avg_order_value": round(float(order_val.mean()), 2),
    "yearly_sales": {int(k): round(float(v), 0) for k, v in yr.items()},
    "yoy_growth_pct": {int(k): round(float(v), 1) for k, v in yoy.dropna().items()},
    "top_3_calendar_months_share_pct": {names[m - 1]: round(float(s), 1) for m, s in best_cal.head(3).items()},
    "category_share_pct": {k: round(100 * float(v) / total_sales, 1) for k, v in cat.items()},
    "top_subcategories": {k: round(float(v), 0) for k, v in subs.head(3).items()},
    "top_product": {top_prod.index[0]: round(float(top_prod.iloc[0]), 0)},
    "region_share_pct": {k: round(100 * float(v) / total_sales, 1) for k, v in reg.sort_values(ascending=False).items()},
    "top_customer_quintile_share_pct": float(q["pct_of_sales"].iloc[0]),
}
with open(os.path.join(RES, "summary.json"), "w") as f:
    json.dump(summary, f, indent=2)
# cleaned export (used by the Excel dashboard builder)
df.sort_values(["Order ID", "Row ID"]).to_csv(os.path.join(RES, "cleaned_sales.csv"), index=False)
print("\nSaved results/summary.json, results/sql_results.md, results/cleaned_sales.csv and figures/*.png")
print(json.dumps(summary, indent=2))
