TRUNCATE TABLE
    fact_sales,
    dim_customer,
    dim_product,
    dim_seller,
    dim_date
RESTART IDENTITY CASCADE;



INSERT INTO dim_customer (
    customer_unique_id,
    customer_city,
    customer_state,
    customer_latitude,
    customer_longitude
)
SELECT DISTINCT ON (customer_unique_id)
    customer_unique_id,
    customer_city,
    customer_state,
    customer_latitude,
    customer_longitude
FROM staging_sales
WHERE customer_unique_id IS NOT NULL
ORDER BY customer_unique_id, order_purchase_timestamp DESC;


INSERT INTO dim_product (
    product_id,
    product_category,
    product_weight_g,
    product_length_cm,
    product_height_cm,
    product_width_cm
)
SELECT DISTINCT ON (product_id)
    product_id,
    product_category,
    product_weight_g,
    product_length_cm,
    product_height_cm,
    product_width_cm
FROM staging_sales
WHERE product_id IS NOT NULL
ORDER BY product_id;


INSERT INTO dim_seller (
    seller_id,
    seller_city,
    seller_state,
    seller_latitude,
    seller_longitude
)
SELECT DISTINCT ON (seller_id)
    seller_id,
    seller_city,
    seller_state,
    seller_latitude,
    seller_longitude
FROM staging_sales
WHERE seller_id IS NOT NULL
ORDER BY seller_id;


INSERT INTO dim_date (
    date_key,
    full_date,
    year,
    quarter,
    month,
    month_name,
    day,
    day_of_week
)
SELECT DISTINCT ON (order_purchase_timestamp::date)
    TO_CHAR(order_purchase_timestamp, 'YYYYMMDD')::INTEGER,
    order_purchase_timestamp::DATE,
    EXTRACT(YEAR FROM order_purchase_timestamp)::INTEGER,
    EXTRACT(QUARTER FROM order_purchase_timestamp)::INTEGER,
    EXTRACT(MONTH FROM order_purchase_timestamp)::INTEGER,
    TRIM(TO_CHAR(order_purchase_timestamp, 'Month')),
    EXTRACT(DAY FROM order_purchase_timestamp)::INTEGER,
    TRIM(TO_CHAR(order_purchase_timestamp, 'Day'))
FROM staging_sales
WHERE order_purchase_timestamp IS NOT NULL
ORDER BY order_purchase_timestamp::DATE;


INSERT INTO fact_sales (
    order_id,
    order_item_id,
    customer_key,
    product_key,
    seller_key,
    date_key,
    order_status,
    price,
    freight_value,
    total_item_value,
    total_payment_value,
    review_score,
    delivery_time_days,
    delivery_lateness_days,
    is_late_delivery,
    main_payment_type,
    max_payment_installments
)
SELECT
    s.order_id,
    s.order_item_id,
    c.customer_key,
    p.product_key,
    se.seller_key,
    d.date_key,
    s.order_status,
    s.price,
    s.freight_value,
    s.total_item_value,
    s.total_payment_value,
    s.review_score,
    s.delivery_time_days,
    s.delivery_lateness_days,
    s.is_late_delivery,
    s.main_payment_type,
    s.max_payment_installments
FROM (
    SELECT DISTINCT ON (order_id, order_item_id) *
    FROM staging_sales
    ORDER BY order_id, order_item_id
) s
LEFT JOIN dim_customer c
    ON s.customer_unique_id = c.customer_unique_id
LEFT JOIN dim_product p
    ON s.product_id = p.product_id
LEFT JOIN dim_seller se
    ON s.seller_id = se.seller_id
LEFT JOIN dim_date d
    ON s.order_purchase_timestamp::DATE = d.full_date;