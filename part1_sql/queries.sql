-- Query 1: Monthly revenue by category

SELECT
    month,
    category,
    ROUND(SUM(quantity * unit_price), 2) AS revenue,
    COUNT(*) AS n_orders
FROM orders
GROUP BY month, category
ORDER BY month, category;

-- Query 2: Region-wise total revenue and order count

SELECT
    r.region,
    ROUND(SUM(o.quantity * o.unit_price), 2) AS total_revenue,
    COUNT(*) AS n_orders
FROM orders o
JOIN resellers r
    ON o.reseller_id = r.reseller_id
GROUP BY r.region
ORDER BY total_revenue DESC;

-- Query 3: Top 5 resellers by total spend

SELECT
    r.reseller_id,
    r.reseller_name,
    ROUND(SUM(o.quantity * o.unit_price), 2) AS total_spend
FROM orders o
JOIN resellers r
    ON o.reseller_id = r.reseller_id
GROUP BY r.reseller_id, r.reseller_name
HAVING total_spend > 50000
ORDER BY total_spend DESC
LIMIT 5;

-- Query 4: Resellers who never placed an order

SELECT
    r.reseller_id,
    r.reseller_name,
    r.region
FROM resellers r
LEFT JOIN orders o
    ON r.reseller_id = o.reseller_id
WHERE o.order_id IS NULL;

-- Query 4B: COUNT(*) vs COUNT(order_id)
-- EXPLANATION: When performing a LEFT JOIN for reseller RS024 (who has zero orders),
-- SQLite produces a single result row containing RS024 attributes and NULL for all order columns.
-- COUNT(*) counts the total number of rows in the group, returning 1 (counting the single NULL-padded row).
-- COUNT(o.order_id) counts non-NULL values in the order_id column, returning 0.
-- This explicitly demonstrates why COUNT(*) CANNOT be used to test for a zero-match LEFT JOIN row.

SELECT
    r.reseller_id,
    r.reseller_name,
    COUNT(*) AS count_star,
    COUNT(o.order_id) AS count_order_id
FROM resellers r
LEFT JOIN orders o
    ON r.reseller_id = o.reseller_id
WHERE r.reseller_id = 'RS024'
GROUP BY r.reseller_id, r.reseller_name;

-- Query 5: June Delivered AOV

SELECT
    ROUND(
        SUM(quantity * unit_price) / COUNT(*),
        2
    ) AS june_delivered_aov
FROM orders
WHERE month = 'June'
  AND status = 'Delivered';