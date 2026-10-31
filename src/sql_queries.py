from sqlalchemy import text

QUERIES = {
"business_totals": "SELECT SUM(sales) AS revenue, SUM(profit) AS profit, COUNT(DISTINCT order_id) AS orders, SUM(sales) / NULLIF(COUNT(DISTINCT order_id),0) AS aov FROM superstore_orders;",
"monthly_trend": "SELECT DATE_TRUNC('month', order_date)::date AS month, SUM(sales) AS revenue, SUM(profit) AS profit FROM superstore_orders GROUP BY 1 ORDER BY 1;",
"yearly_growth": "WITH yearly AS (SELECT EXTRACT(YEAR FROM order_date)::int AS year, SUM(sales) AS sales FROM superstore_orders GROUP BY 1) SELECT year, sales, LAG(sales) OVER (ORDER BY year) AS prior_year_sales, ROUND(100.0 * (sales - LAG(sales) OVER (ORDER BY year)) / NULLIF(LAG(sales) OVER (ORDER BY year),0), 2) AS growth_pct FROM yearly ORDER BY year;",
"top_products": "SELECT product_id, product_name, SUM(sales) AS revenue, SUM(profit) AS profit FROM superstore_orders GROUP BY 1,2 ORDER BY revenue DESC LIMIT 10;",
"category_profit": "SELECT category, SUM(sales) AS revenue, SUM(profit) AS profit, SUM(profit)/NULLIF(SUM(sales),0) AS margin FROM superstore_orders GROUP BY category ORDER BY profit DESC;",
"segment_sales": "SELECT segment, SUM(sales) AS revenue, COUNT(DISTINCT order_id) AS orders FROM superstore_orders GROUP BY segment ORDER BY revenue DESC;",
"regional_performance": "SELECT region, SUM(sales) AS revenue, SUM(profit) AS profit, SUM(profit)/NULLIF(SUM(sales),0) AS margin FROM superstore_orders GROUP BY region ORDER BY revenue DESC;",
"top_customers": "SELECT customer_id, customer_name, SUM(sales) AS revenue, COUNT(DISTINCT order_id) AS orders FROM superstore_orders GROUP BY 1,2 ORDER BY revenue DESC LIMIT 10;",
"repeat_customers": "WITH c AS (SELECT customer_id, COUNT(DISTINCT order_id) AS orders, SUM(sales) AS revenue FROM superstore_orders GROUP BY customer_id) SELECT CASE WHEN orders > 1 THEN 'Repeat' ELSE 'One-time' END AS customer_type, COUNT(*) AS customers, SUM(revenue) AS revenue FROM c GROUP BY 1;",
"discount_profit": "SELECT discount, COUNT(*) AS line_items, AVG(profit) AS avg_profit, SUM(profit) AS total_profit FROM superstore_orders GROUP BY discount ORDER BY discount;",
"loss_products": "SELECT product_id, product_name, SUM(sales) AS revenue, SUM(profit) AS loss FROM superstore_orders GROUP BY 1,2 HAVING SUM(profit) < 0 ORDER BY loss ASC;",
"average_order_value": "SELECT SUM(order_sales) / NULLIF(COUNT(*),0) AS average_order_value FROM (SELECT order_id, SUM(sales) AS order_sales FROM superstore_orders GROUP BY order_id) o;"
}
