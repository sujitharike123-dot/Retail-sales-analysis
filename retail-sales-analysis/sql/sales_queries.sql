-- Queries below run against the `sales` table (cleaned data loaded into SQLite by src/sales_analysis.py).
-- Each query is introduced by a title comment line.

-- QUERY: Yearly sales and year-over-year growth (LAG window function)
WITH yearly AS (
    SELECT order_year AS year,
           COUNT(DISTINCT order_id) AS orders,
           ROUND(SUM(sales), 0)     AS sales
    FROM sales
    GROUP BY order_year
)
SELECT year, orders, sales,
       ROUND(100.0 * (sales - LAG(sales) OVER (ORDER BY year)) / LAG(sales) OVER (ORDER BY year), 1) AS yoy_growth_pct
FROM yearly
ORDER BY year;

-- QUERY: Monthly sales, month-over-month growth and 3-month moving average
WITH monthly AS (
    SELECT strftime('%Y-%m', order_date) AS month, SUM(sales) AS sales
    FROM sales
    GROUP BY month
)
SELECT month,
       ROUND(sales, 0) AS sales,
       ROUND(100.0 * (sales - LAG(sales) OVER (ORDER BY month)) / LAG(sales) OVER (ORDER BY month), 1) AS mom_growth_pct,
       ROUND(AVG(sales) OVER (ORDER BY month ROWS BETWEEN 2 PRECEDING AND CURRENT ROW), 0) AS moving_avg_3m
FROM monthly
ORDER BY month;

-- QUERY: Seasonality - share of all sales by calendar month, ranked
WITH m AS (
    SELECT CAST(strftime('%m', order_date) AS INTEGER) AS month_no, SUM(sales) AS sales
    FROM sales
    GROUP BY month_no
)
SELECT month_no, ROUND(sales, 0) AS sales,
       ROUND(100.0 * sales / SUM(sales) OVER (), 1) AS share_pct,
       RANK() OVER (ORDER BY sales DESC) AS sales_rank
FROM m
ORDER BY month_no;

-- QUERY: Category and sub-category share of sales (window over aggregates)
SELECT category, sub_category,
       ROUND(SUM(sales), 0) AS sales,
       ROUND(100.0 * SUM(sales) / SUM(SUM(sales)) OVER (), 1) AS pct_of_total,
       RANK() OVER (PARTITION BY category ORDER BY SUM(sales) DESC) AS rank_in_category
FROM sales
GROUP BY category, sub_category
ORDER BY sales DESC;

-- QUERY: Top 10 products by sales
SELECT RANK() OVER (ORDER BY SUM(sales) DESC) AS sales_rank,
       product_name, category,
       ROUND(SUM(sales), 0) AS sales,
       ROUND(100.0 * SUM(sales) / (SELECT SUM(sales) FROM sales), 2) AS pct_of_total
FROM sales
GROUP BY product_id, product_name, category
ORDER BY sales_rank
LIMIT 10;

-- QUERY: Region by category sales matrix
SELECT region,
       ROUND(SUM(CASE WHEN category = 'Furniture'       THEN sales END), 0) AS furniture,
       ROUND(SUM(CASE WHEN category = 'Office Supplies' THEN sales END), 0) AS office_supplies,
       ROUND(SUM(CASE WHEN category = 'Technology'      THEN sales END), 0) AS technology,
       ROUND(SUM(sales), 0) AS total,
       ROUND(100.0 * SUM(sales) / (SELECT SUM(sales) FROM sales), 1) AS pct_of_total
FROM sales
GROUP BY region
ORDER BY total DESC;

-- QUERY: Top 10 states by sales
SELECT RANK() OVER (ORDER BY SUM(sales) DESC) AS sales_rank,
       state, region,
       ROUND(SUM(sales), 0) AS sales,
       ROUND(100.0 * SUM(sales) / (SELECT SUM(sales) FROM sales), 1) AS pct_of_total
FROM sales
GROUP BY state, region
ORDER BY sales_rank
LIMIT 10;

-- QUERY: Customer concentration - sales by customer quintile (NTILE)
WITH cust AS (
    SELECT customer_id, SUM(sales) AS sales FROM sales GROUP BY customer_id
),
ranked AS (
    SELECT customer_id, sales, NTILE(5) OVER (ORDER BY sales DESC) AS quintile FROM cust
)
SELECT quintile,
       COUNT(*) AS customers,
       ROUND(SUM(sales), 0) AS sales,
       ROUND(100.0 * SUM(sales) / (SELECT SUM(sales) FROM cust), 1) AS pct_of_sales
FROM ranked
GROUP BY quintile
ORDER BY quintile;

-- QUERY: Segment performance with average order value (CTE)
WITH orders AS (
    SELECT order_id, segment, SUM(sales) AS order_value
    FROM sales
    GROUP BY order_id, segment
)
SELECT segment,
       COUNT(*) AS orders,
       ROUND(SUM(order_value), 0) AS sales,
       ROUND(AVG(order_value), 2) AS avg_order_value
FROM orders
GROUP BY segment
ORDER BY sales DESC;

-- QUERY: Shipping speed by ship mode
SELECT ship_mode,
       COUNT(DISTINCT order_id) AS orders,
       ROUND(100.0 * COUNT(DISTINCT order_id) / (SELECT COUNT(DISTINCT order_id) FROM sales), 1) AS pct_of_orders,
       ROUND(AVG(julianday(ship_date) - julianday(order_date)), 1) AS avg_days_to_ship
FROM sales
GROUP BY ship_mode
ORDER BY avg_days_to_ship;
