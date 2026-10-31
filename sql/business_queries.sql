-- 1. Total sales, profit and distinct orders
SELECT SUM(sales) revenue, SUM(profit) profit, COUNT(DISTINCT order_id) orders FROM superstore_orders;

-- 2. Monthly revenue and profit
SELECT DATE_TRUNC('month', order_date)::date month, SUM(sales) revenue, SUM(profit) profit
FROM superstore_orders GROUP BY 1 ORDER BY 1;

-- 3. Year-over-year sales growth
WITH y AS (SELECT EXTRACT(YEAR FROM order_date)::int year, SUM(sales) sales FROM superstore_orders GROUP BY 1)
SELECT year, sales, LAG(sales) OVER (ORDER BY year) prior_sales,
       ROUND(100.0*(sales-LAG(sales) OVER (ORDER BY year))/NULLIF(LAG(sales) OVER (ORDER BY year),0),2) growth_pct
FROM y ORDER BY year;

-- 4. Top 10 products by sales
SELECT product_id, product_name, SUM(sales) revenue FROM superstore_orders GROUP BY 1,2 ORDER BY revenue DESC LIMIT 10;

-- 5. Most profitable categories
SELECT category, SUM(profit) profit FROM superstore_orders GROUP BY category ORDER BY profit DESC;

-- 6. Sales by customer segment
SELECT segment, SUM(sales) revenue FROM superstore_orders GROUP BY segment ORDER BY revenue DESC;

-- 7. Regional sales and profitability
SELECT region, SUM(sales) revenue, SUM(profit) profit, SUM(profit)/NULLIF(SUM(sales),0) margin
FROM superstore_orders GROUP BY region ORDER BY revenue DESC;

-- 8. Top 10 customers
SELECT customer_id, customer_name, SUM(sales) revenue FROM superstore_orders GROUP BY 1,2 ORDER BY revenue DESC LIMIT 10;

-- 9. Repeat versus one-time customers (distinct orders, not line items)
WITH c AS (SELECT customer_id, COUNT(DISTINCT order_id) orders, SUM(sales) revenue FROM superstore_orders GROUP BY customer_id)
SELECT CASE WHEN orders>1 THEN 'Repeat' ELSE 'One-time' END customer_type, COUNT(*) customers, SUM(revenue) revenue
FROM c GROUP BY 1;

-- 10. Discount versus profitability
SELECT discount, COUNT(*) line_items, AVG(profit) avg_profit, SUM(profit) total_profit
FROM superstore_orders GROUP BY discount ORDER BY discount;

-- 11. Loss-making products
-- 11. Loss-making products
SELECT
    product_id,
    product_name,
    SUM(profit) AS total_profit
FROM superstore_orders
GROUP BY product_id, product_name
HAVING SUM(profit) < 0
ORDER BY total_profit;

-- 12. Average order value: aggregate lines to order level first
SELECT AVG(order_sales) average_order_value FROM
(SELECT order_id, SUM(sales) order_sales FROM superstore_orders GROUP BY order_id) orders;
