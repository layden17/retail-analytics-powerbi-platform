-- 1. Chiffre d'affaires total
SELECT
    ROUND(SUM(total_item_value)::numeric, 2) AS total_revenue
FROM fact_sales
WHERE order_status = 'delivered';


-- 2. Nombre de commandes livrées
SELECT
    COUNT(DISTINCT order_id) AS delivered_orders
FROM fact_sales
WHERE order_status = 'delivered';


-- 3. Panier moyen
SELECT
    ROUND(
        (
            SUM(total_item_value)
            / COUNT(DISTINCT order_id)
        )::numeric,
        2
    ) AS average_order_value
FROM fact_sales
WHERE order_status = 'delivered';


-- 4. Chiffre d'affaires par mois
SELECT
    d.year,
    d.month,
    TRIM(d.month_name) AS month_name,
    ROUND(SUM(f.total_item_value)::numeric, 2) AS revenue,
    COUNT(DISTINCT f.order_id) AS orders
FROM fact_sales f
JOIN dim_date d
    ON f.date_key = d.date_key
WHERE f.order_status = 'delivered'
GROUP BY
    d.year,
    d.month,
    d.month_name
ORDER BY
    d.year,
    d.month;


-- 5. Top 10 catégories produit
SELECT
    p.product_category,
    ROUND(SUM(f.total_item_value)::numeric, 2) AS revenue,
    COUNT(*) AS items_sold,
    COUNT(DISTINCT f.order_id) AS orders
FROM fact_sales f
JOIN dim_product p
    ON f.product_key = p.product_key
WHERE f.order_status = 'delivered'
GROUP BY
    p.product_category
ORDER BY
    revenue DESC
LIMIT 10;