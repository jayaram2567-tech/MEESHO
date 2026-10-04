/*monthly revenue by category*/

SELECT
    month,
    category,
    ROUND(SUM(quantity * unit_price), 2) AS revenue,
    COUNT(*) AS n_orders
FROM orders
GROUP BY month, category
ORDER BY month, category;

/* region wise revenue*/

SELECT
    r.region,
    ROUND(SUM(o.quantity * o.unit_price), 2) AS total_revenue,
    COUNT(*) AS order_count
FROM orders o
JOIN resellers r
    ON o.reseller_id = r.reseller_id
GROUP BY r.region
ORDER BY total_revenue DESC;

/* Top five resellers*/

SELECT
    o.reseller_id,
    r.reseller_name,
    ROUND(SUM(o.quantity * o.unit_price), 2) AS total_spend
FROM orders o
JOIN resellers r
    ON o.reseller_id = r.reseller_id
GROUP BY o.reseller_id, r.reseller_name
HAVING total_spend > 50000
ORDER BY total_spend DESC
LIMIT 5;

/* resellers who NEVER placed an  orders*/

SELECT
    r.reseller_id,
    r.reseller_name,
    r.city,
    r.region
FROM resellers r
LEFT JOIN orders o
    ON r.reseller_id = o.reseller_id
WHERE o.order_id IS NULL;

/* COUNT (*) VS COUNT (order_id)*/

SELECT
    r.reseller_id,
    COUNT(*) AS count_star,
    COUNT(o.order_id) AS count_order_id
FROM resellers r
LEFT JOIN orders o
    ON r.reseller_id = o.reseller_id
WHERE r.reseller_id = (
    SELECT r2.reseller_id
    FROM resellers r2
    LEFT JOIN orders o2
        ON r2.reseller_id = o2.reseller_id
    WHERE o2.order_id IS NULL
)
GROUP BY r.reseller_id;


/*June deliverd AOV(average order value)*/

SELECT
    ROUND(
        SUM(quantity * unit_price) / COUNT(*),
        2
    ) AS june_delivered_aov
FROM orders
WHERE month = 'June'
  AND status = 'Delivered';

  /* Region total sum as match as the Grand total*/

  SELECT 
    r.region AS Region,
    ROUND(SUM(o.quantity * o.unit_price), 2) AS Total_Revenue
FROM orders o
JOIN resellers r 
    ON o.reseller_id = r.reseller_id
GROUP BY r.region

UNION ALL

-- Grand Total Row (All Regions Sum)
SELECT 
    'Grand Total' AS Region,
    ROUND(SUM(o.quantity * o.unit_price), 2) AS Total_Revenue
FROM orders o
JOIN resellers r 
    ON o.reseller_id = r.reseller_id;

--Top five orders

SELECT * FROM ORDERS LIMIT 5;

