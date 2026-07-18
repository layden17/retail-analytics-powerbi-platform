DROP TABLE IF EXISTS fact_sales;
DROP TABLE IF EXISTS dim_customer;
DROP TABLE IF EXISTS dim_product;
DROP TABLE IF EXISTS dim_seller;
DROP TABLE IF EXISTS dim_date;

CREATE TABLE dim_customer (
    customer_key SERIAL PRIMARY KEY,
    customer_unique_id TEXT UNIQUE,
    customer_city TEXT,
    customer_state TEXT,
    customer_latitude DOUBLE PRECISION,
    customer_longitude DOUBLE PRECISION
);

CREATE TABLE dim_product (
    product_key SERIAL PRIMARY KEY,
    product_id TEXT UNIQUE,
    product_category TEXT,
    product_weight_g DOUBLE PRECISION,
    product_length_cm DOUBLE PRECISION,
    product_height_cm DOUBLE PRECISION,
    product_width_cm DOUBLE PRECISION
);

CREATE TABLE dim_seller (
    seller_key SERIAL PRIMARY KEY,
    seller_id TEXT UNIQUE,
    seller_city TEXT,
    seller_state TEXT,
    seller_latitude DOUBLE PRECISION,
    seller_longitude DOUBLE PRECISION
);

CREATE TABLE dim_date (
    date_key INTEGER PRIMARY KEY,
    full_date DATE UNIQUE,
    year INTEGER,
    quarter INTEGER,
    month INTEGER,
    month_name TEXT,
    day INTEGER,
    day_of_week TEXT
);

CREATE TABLE fact_sales (
    sales_key BIGSERIAL PRIMARY KEY,
    order_id TEXT,
    order_item_id INTEGER,
    customer_key INTEGER REFERENCES dim_customer(customer_key),
    product_key INTEGER REFERENCES dim_product(product_key),
    seller_key INTEGER REFERENCES dim_seller(seller_key),
    date_key INTEGER REFERENCES dim_date(date_key),
    order_status TEXT,
    price DOUBLE PRECISION,
    freight_value DOUBLE PRECISION,
    total_item_value DOUBLE PRECISION,
    total_payment_value DOUBLE PRECISION,
    review_score DOUBLE PRECISION,
    delivery_time_days DOUBLE PRECISION,
    delivery_lateness_days DOUBLE PRECISION,
    is_late_delivery BOOLEAN,
    main_payment_type TEXT,
    max_payment_installments INTEGER,
    UNIQUE (order_id, order_item_id)
);