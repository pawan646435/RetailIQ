CREATE TABLE IF NOT EXISTS superstore_orders (
    row_id BIGINT, order_id TEXT NOT NULL, order_date DATE NOT NULL, ship_date DATE,
    ship_mode TEXT, customer_id TEXT, customer_name TEXT, segment TEXT, country TEXT,
    city TEXT, state TEXT, postal_code TEXT, region TEXT, product_id TEXT,
    category TEXT, sub_category TEXT, product_name TEXT, sales NUMERIC(14,2),
    quantity INTEGER, discount NUMERIC(8,4), profit NUMERIC(14,2),
    order_year INTEGER, order_month INTEGER, month_year DATE, profit_margin NUMERIC(12,6),
    shipping_duration INTEGER, order_value NUMERIC(14,2), is_loss BOOLEAN
);
CREATE INDEX IF NOT EXISTS idx_orders_date ON superstore_orders(order_date);
CREATE INDEX IF NOT EXISTS idx_orders_region ON superstore_orders(region);
CREATE INDEX IF NOT EXISTS idx_orders_customer ON superstore_orders(customer_id);
