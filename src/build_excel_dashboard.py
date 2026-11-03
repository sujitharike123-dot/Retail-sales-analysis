"""Build excel/Retail_Sales_Dashboard.xlsx from results/cleaned_sales.csv.

Run src/sales_analysis.py first (it writes results/cleaned_sales.csv).
The dashboard's KPIs and summary tables are live Excel formulas (SUMIFS / SUMPRODUCT / INDEX-MATCH)
over the 'Data' sheet, so they recalculate if the data changes. Charts are native Excel charts.
"""
import os

import pandas as pd
from openpyxl import Workbook
from openpyxl.chart import BarChart, LineChart, Reference
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side

ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
SRC = os.path.join(ROOT, "results", "cleaned_sales.csv")
OUT = os.path.join(ROOT, "excel", "Retail_Sales_Dashboard.xlsx")
if not os.path.exists(SRC):
    raise SystemExit("Run src/sales_analysis.py first - results/cleaned_sales.csv is missing.")

df = pd.read_csv(SRC, parse_dates=["Order Date", "Order Month"])
df = df.sort_values(["Order ID", "Row ID"]).reset_index(drop=True)  # sorted so the order-count helper works
N = len(df)
LAST = N + 1  # last data row on the Data sheet

NAVY, BLUE, LIGHT, GREY = "153E5B", "2B6CB0", "EAF1F8", "6B7280"
F = lambda **kw: Font(name="Arial", **kw)
HDR_FILL = PatternFill("solid", fgColor=NAVY)
CARD_FILL = PatternFill("solid", fgColor=LIGHT)
thin = Side(style="thin", color="D0D7DE")

wb = Workbook()
dash = wb.active
dash.title = "Dashboard"
summ = wb.create_sheet("Summary")
data = wb.create_sheet("Data")

# ------------------------------------------------------------------ Data sheet
cols = ["Order ID", "Order Date", "Order Year", "Order Month", "Ship Mode", "Segment", "Region", "State",
        "Category", "Sub-Category", "Customer ID", "Product Name", "Sales"]
letters = {name: chr(ord("A") + i) for i, name in enumerate(cols)}  # Sales -> M
S, YR, MON = letters["Sales"], letters["Order Year"], letters["Order Month"]
FLAG = "N"
for j, name in enumerate(cols + ["New Order Flag"], start=1):
    c = data.cell(row=1, column=j, value=name)
    c.font = F(bold=True, color="FFFFFF"); c.fill = HDR_FILL; c.alignment = Alignment(horizontal="center")
for i, row in enumerate(df[cols].itertuples(index=False), start=2):
    for j, v in enumerate(row, start=1):
        if isinstance(v, pd.Timestamp):
            v = v.to_pydatetime()
        c = data.cell(row=i, column=j, value=v)
        c.font = F(size=10)
    data.cell(row=i, column=2).number_format = "yyyy-mm-dd"
    data.cell(row=i, column=4).number_format = "mmm yyyy"
    data.cell(row=i, column=13).number_format = "#,##0.00"
    f = data.cell(row=i, column=14, value=f"=IF(A{i}=A{i-1},0,1)")  # 1 on the first line of each order
    f.font = F(size=10)
for col, w in zip("ABCDEFGHIJKLMN", [16, 12, 11, 12, 15, 13, 10, 18, 16, 14, 13, 50, 11, 15]):
    data.column_dimensions[col].width = w
data.freeze_panes = "A2"
data.auto_filter.ref = f"A1:N{LAST}"


def rng(col):
    return f"Data!${col}$2:${col}${LAST}"


# ------------------------------------------------------------------ Summary sheet
summ.sheet_view.showGridLines = False
summ["A1"] = "Summary tables (live formulas over the Data sheet)"
summ["A1"].font = F(bold=True, size=14, color=NAVY)
summ["A2"] = "Sales = revenue in USD. Every number below is a formula; edit the Data sheet and these update."
summ["A2"].font = F(italic=True, size=9, color=GREY)
for col, w in zip("ABCDEFG", [44, 14, 12, 12, 3, 12, 14]):
    summ.column_dimensions[col].width = w


def title(ws, r, col, text):
    c = ws.cell(row=r, column=col, value=text)
    c.font = F(bold=True, size=11, color=NAVY)


def header(ws, r, col, labels):
    for k, lab in enumerate(labels):
        c = ws.cell(row=r, column=col + k, value=lab)
        c.font = F(bold=True, color="FFFFFF", size=10); c.fill = HDR_FILL
        c.alignment = Alignment(horizontal="center" if k else "left")


def style_body(ws, r, col, ncols, fmts):
    for k in range(ncols):
        c = ws.cell(row=r, column=col + k)
        c.font = F(size=10)
        c.border = Border(bottom=thin)
        if fmts[k]:
            c.number_format = fmts[k]


tables = {}
r = 4


def sales_table(key, name, label_col_name, labels, share_of="table", orders=False, sumproduct_col=None):
    """Write a table of labels with SUMIFS sales, share %, and optionally order counts."""
    global r
    title(summ, r, 1, name); r += 1
    hdrs = [label_col_name, "Sales ($)", "Share of sales"] + (["Orders"] if orders else [])
    header(summ, r, 1, hdrs); hdr_row = r; r += 1
    first = r
    last = first + len(labels) - 1
    for lab in labels:
        summ.cell(row=r, column=1, value=lab)
        if sumproduct_col:  # exact-match sum, safe for text containing wildcard characters
            summ.cell(row=r, column=2, value=f"=SUMPRODUCT(({rng(sumproduct_col)}=$A{r})*{rng(S)})")
        else:
            summ.cell(row=r, column=2, value=f"=SUMIFS({rng(S)},{rng(letters[label_col_name])},$A{r})")
        denom = f"SUM($B${first}:$B${last})" if share_of == "table" else f"SUM({rng(S)})"
        summ.cell(row=r, column=3, value=f"=B{r}/{denom}")
        if orders:
            summ.cell(row=r, column=4, value=f"=SUMIFS({rng(FLAG)},{rng(letters[label_col_name])},$A{r})")
        style_body(summ, r, 1, len(hdrs), [None, "$#,##0", "0.0%", "#,##0"][:len(hdrs)])
        r += 1
    tables[key] = (hdr_row, first, last)
    r += 1


# yearly with YoY
years = sorted(df["Order Year"].unique())
title(summ, r, 1, "Yearly sales and growth"); r += 1
header(summ, r, 1, ["Year", "Sales ($)", "YoY growth"]); y_hdr = r; r += 1
y_first = r
for k, y in enumerate(years):
    summ.cell(row=r, column=1, value=int(y))
    summ.cell(row=r, column=2, value=f"=SUMIFS({rng(S)},{rng(YR)},$A{r})")
    summ.cell(row=r, column=3, value=(f"=B{r}/B{r-1}-1" if k else "n/a"))
    style_body(summ, r, 1, 3, ["0", "$#,##0", "0.0%"])
    summ.cell(row=r, column=3).alignment = Alignment(horizontal="right")
    r += 1
tables["year"] = (y_hdr, y_first, r - 1)
r += 1

order_by = lambda col: df.groupby(col)["Sales"].sum().sort_values(ascending=False).index.tolist()
sales_table("cat", "Sales by category", "Category", order_by("Category"))
sales_table("region", "Sales by region", "Region", order_by("Region"))
sales_table("segment", "Sales by customer segment", "Segment", order_by("Segment"), orders=True)
sales_table("ship", "Orders by ship mode", "Ship Mode", order_by("Ship Mode"), orders=True)
sales_table("sub", "Sales by sub-category", "Sub-Category", order_by("Sub-Category"))
sales_table("state", "Top 10 states by sales (share of total sales)", "State", order_by("State")[:10], share_of="total")
sales_table("prod", "Top 10 products by sales (share of total sales)", "Product Name", order_by("Product Name")[:10],
            share_of="total", sumproduct_col=letters["Product Name"])

# monthly (columns F:G)
title(summ, 4, 6, "Monthly sales")
header(summ, 5, 6, ["Month", "Sales ($)"])
months = sorted(df["Order Month"].unique())
for k, m in enumerate(months):
    rr = 6 + k
    summ.cell(row=rr, column=6, value=pd.Timestamp(m).to_pydatetime())
    summ.cell(row=rr, column=7, value=f"=SUMIFS({rng(S)},{rng(MON)},$F{rr})")
    style_body(summ, rr, 6, 2, ["mmm yyyy", "$#,##0"])
m_first, m_last = 6, 5 + len(months)

# ------------------------------------------------------------------ Dashboard sheet
dash.sheet_view.showGridLines = False
for k in range(1, 13):
    dash.column_dimensions[chr(64 + k)].width = 14
dash["A1"] = "Retail Sales Dashboard"
dash["A1"].font = F(bold=True, size=20, color=NAVY)
dash["A2"] = "Superstore sales data, 2015-2018. All figures are sales revenue in USD (the dataset has no profit column)."
dash["A2"].font = F(italic=True, size=10, color=GREY)

y_hdr, y_first, y_last = tables["year"]
c_hdr, c_first, c_last = tables["cat"]
g_hdr, g_first, g_last = tables["region"]
cards = [
    ("Total sales", f"=SUM({rng(S)})", "$#,##0"),
    ("Orders", f"=SUM({rng(FLAG)})", "#,##0"),
    ("Average order value", "=A5/C5", "$#,##0.00"),
    (f'="Sales growth in "&Summary!A{y_last}', f"=Summary!C{y_last}", "+0.0%;-0.0%"),
    ("Top category", f"=INDEX(Summary!$A${c_first}:$A${c_last},MATCH(MAX(Summary!$B${c_first}:$B${c_last}),Summary!$B${c_first}:$B${c_last},0))", "General"),
    ("Top region", f"=INDEX(Summary!$A${g_first}:$A${g_last},MATCH(MAX(Summary!$B${g_first}:$B${g_last}),Summary!$B${g_first}:$B${g_last},0))", "General"),
]
for k, (lab, formula, fmt) in enumerate(cards):
    col = 1 + 2 * k
    dash.merge_cells(start_row=4, start_column=col, end_row=4, end_column=col + 1)
    dash.merge_cells(start_row=5, start_column=col, end_row=5, end_column=col + 1)
    a, b = dash.cell(row=4, column=col, value=lab), dash.cell(row=5, column=col, value=formula)
    a.font = F(size=9, color=GREY); b.font = F(bold=True, size=16, color=NAVY)
    b.number_format = fmt
    for rr in (4, 5):
        for cc in (col, col + 1):
            dash.cell(row=rr, column=cc).fill = CARD_FILL
    a.alignment = Alignment(horizontal="center"); b.alignment = Alignment(horizontal="center", vertical="center")
dash.row_dimensions[5].height = 30
# Card positions: Total sales = A5, Orders = C5, Average order value = E5 (=A5/C5).


def style_chart(ch, ttl, w, h):
    ch.title = ttl; ch.legend = None; ch.width = w; ch.height = h
    ch.x_axis.delete = False; ch.y_axis.delete = False
    return ch


def bar(hdr, first, last, ttl, anchor, horizontal=False, w=15.5, h=7.5, numfmt='#,##0'):
    ch = BarChart(); ch.type = "bar" if horizontal else "col"
    data_ref = Reference(summ, min_col=2, min_row=hdr, max_row=last)
    cats = Reference(summ, min_col=1, min_row=first, max_row=last)
    ch.add_data(data_ref, titles_from_data=True); ch.set_categories(cats)
    ch.series[0].graphicalProperties.solidFill = BLUE
    style_chart(ch, ttl, w, h)
    if horizontal:
        ch.x_axis.scaling.orientation = "maxMin"
    ch.y_axis.numFmt = numfmt; ch.y_axis.number_format = numfmt
    ch.y_axis.scaling.min = 0  # bars always start at zero so differences are not exaggerated
    ch.gapWidth = 60
    dash.add_chart(ch, anchor)


bar(y_hdr, y_first, y_last, "Yearly sales ($)", "A8")

line = LineChart()
line.add_data(Reference(summ, min_col=7, min_row=5, max_row=m_last), titles_from_data=True)
line.set_categories(Reference(summ, min_col=6, min_row=m_first, max_row=m_last))
line.series[0].graphicalProperties.line.solidFill = BLUE
line.series[0].graphicalProperties.line.width = 22000
line.series[0].smooth = False
style_chart(line, "Monthly sales ($)", 15.5, 7.5)
line.x_axis.number_format = "mmm yy"; line.x_axis.tickLblSkip = 6
line.y_axis.number_format = "#,##0"
dash.add_chart(line, "G8")

bar(c_hdr, c_first, c_last, "Sales by category ($)", "A24")
bar(g_hdr, g_first, g_last, "Sales by region ($)", "G24")
s_hdr, s_first, s_last = tables["sub"]
bar(s_hdr, s_first, s_last, "Sales by sub-category ($)", "A40", horizontal=True, h=10)
t_hdr, t_first, t_last = tables["state"]
bar(t_hdr, t_first, t_last, "Top 10 states by sales ($)", "G40", horizontal=True, h=10)

notes = [
    "Notes and assumptions",
    "Source: Superstore Sales Dataset (Kaggle, train.csv), 9,800 order lines, 2015-2018.",
    "Cleaning (src/sales_analysis.py): 1 exact duplicate row removed; 11 missing postal codes (Burlington, Vermont) filled with 05401; dates parsed as DD/MM/YYYY.",
    "Orders are counted with a helper column on the Data sheet (1 on the first line of each order; Data is sorted by Order ID).",
    "The dataset has no profit, discount or quantity columns, so this dashboard analyses sales revenue only.",
]
for k, t in enumerate(notes):
    c = dash.cell(row=62 + k, column=1, value=t)
    c.font = F(bold=(k == 0), size=9, color=NAVY if k == 0 else GREY)

# print setup: one landscape page for the dashboard
dash.page_setup.orientation = "landscape"
dash.sheet_properties.pageSetUpPr.fitToPage = True
dash.page_setup.fitToWidth = 1
dash.page_setup.fitToHeight = 1

os.makedirs(os.path.dirname(OUT), exist_ok=True)
wb.save(OUT)
print("Saved", os.path.relpath(OUT, ROOT), f"({N:,} data rows)")
