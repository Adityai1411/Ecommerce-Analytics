-- 1. Total Revenue
SELECT 
    ROUND(SUM(revenue), 2) AS total_revenue
FROM sales;

--------------------------------------------------

-- 2. Monthly Revenue Trend
SELECT 
    order_month,
    ROUND(SUM(revenue), 2) AS monthly_revenue
FROM sales
GROUP BY order_month
ORDER BY order_month;

--------------------------------------------------

-- 3. Average Order Value (AOV)
SELECT 
    ROUND(AVG(order_total), 2) AS avg_order_value
FROM (
    SELECT 
        invoice_no,
        SUM(revenue) AS order_total
    FROM sales
    GROUP BY invoice_no
);

--------------------------------------------------

-- 4. Customer Lifetime Value (CLV)
SELECT 
    customer_id,
    ROUND(SUM(revenue), 2) AS lifetime_value
FROM sales
GROUP BY customer_id
ORDER BY lifetime_value DESC;

--------------------------------------------------

-- 5. Repeat vs One-Time Customers
SELECT
    CASE 
        WHEN order_count > 1 THEN 'Returning'
        ELSE 'One-Time'
    END AS customer_type,
    COUNT(*) AS customer_count
FROM (
    SELECT 
        customer_id,
        COUNT(DISTINCT invoice_no) AS order_count
    FROM sales
    GROUP BY customer_id
)
GROUP BY customer_type;

--------------------------------------------------

-- 6. Top 10 Products by Revenue
SELECT
    description AS product,
    ROUND(SUM(revenue), 2) AS product_revenue
FROM sales
GROUP BY description
ORDER BY product_revenue DESC
LIMIT 10;

--------------------------------------------------

-- 7. Revenue by Country
SELECT
    country,
    ROUND(SUM(revenue), 2) AS country_revenue
FROM sales
GROUP BY country
ORDER BY country_revenue DESC;
