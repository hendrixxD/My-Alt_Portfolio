-- Create schema if not exists
CREATE SCHEMA IF NOT EXISTS cpstn;

-- Create customers table and import data
CREATE TABLE IF NOT EXISTS cpstn.olist_customers
(
    customer_id uuid,
    customer_unique_id VARCHAR(33),
    customer_zip_code_prefix CHAR(5),
    customer_city VARCHAR(50),
    customer_state CHAR(2)
);

COPY cpstn.olist_customers (customer_id, customer_unique_id, customer_zip_code_prefix, customer_city, customer_state)
FROM '/data/olist_customers_dataset.csv' DELIMITER ',' CSV HEADER;

-- Create geolocation table and import data
CREATE TABLE IF NOT EXISTS cpstn.olist_geolocation
(
    geolocation_zip_code_prefix CHAR(5),
    geolocation_lat NUMERIC(17,14),
    geolocation_lng NUMERIC(17,14),
    geolocation_city VARCHAR(50),
    geolocation_state CHAR(2)
);

COPY cpstn.olist_geolocation (geolocation_zip_code_prefix, geolocation_lat, geolocation_lng, geolocation_city, geolocation_state)
FROM '/data/olist_geolocation_dataset.csv' DELIMITER ',' CSV HEADER;

-- Create order items table and import data
CREATE TABLE IF NOT EXISTS cpstn.olist_order_items
(
    order_id uuid,
    order_item_id SMALLINT,
    product_id uuid,
    seller_id uuid,
    shipping_limit_date TIMESTAMP,
    price NUMERIC(7,2),
    freight_value NUMERIC(6,2)
);

COPY cpstn.olist_order_items (order_id, order_item_id, product_id, seller_id, shipping_limit_date, price, freight_value)
FROM '/data/olist_order_items_dataset.csv' DELIMITER ',' CSV HEADER;

-- Create order payments table and import data
CREATE TABLE IF NOT EXISTS cpstn.olist_order_payments
(
    order_id uuid,
    payment_sequential SMALLINT,
    payment_type VARCHAR(13),
    payment_installments SMALLINT,
    payment_value NUMERIC(8,2)
);

COPY cpstn.olist_order_payments (order_id, payment_sequential, payment_type, payment_installments, payment_value)
FROM '/data/olist_order_payments_dataset.csv' DELIMITER ',' CSV HEADER;

-- Create order reviews table and import data
CREATE TABLE IF NOT EXISTS cpstn.olist_order_reviews
(
    review_id uuid,
    order_id uuid,
    review_score SMALLINT CHECK (review_score BETWEEN 1 AND 5),
    review_comment_title VARCHAR(255),
    review_comment_message TEXT,
    review_creation_date TIMESTAMP,
    review_answer_timestamp TIMESTAMP
);

COPY cpstn.olist_order_reviews (review_id, order_id, review_score, review_comment_title, review_comment_message, review_creation_date, review_answer_timestamp)
FROM '/data/olist_order_reviews_dataset.csv' DELIMITER ',' CSV HEADER;

-- Create orders table and import data
CREATE TABLE IF NOT EXISTS cpstn.olist_orders
(
    order_id uuid,
    customer_id uuid,
    order_status VARCHAR(20),
    order_purchase_timestamp TIMESTAMP,
    order_approved_at TIMESTAMP,
    order_delivered_carrier_date TIMESTAMP,
    order_delivered_customer_date TIMESTAMP,
    order_estimated_delivery_date DATE
);

COPY cpstn.olist_orders (order_id, customer_id, order_status, order_purchase_timestamp, order_approved_at, order_delivered_carrier_date, order_delivered_customer_date, order_estimated_delivery_date)
FROM '/data/olist_orders_dataset.csv' DELIMITER ',' CSV HEADER;

-- Create products table and import data
CREATE TABLE IF NOT EXISTS cpstn.olist_products
(
    product_id uuid,
    product_category_name VARCHAR(50),
    product_name_length INTEGER,
    product_description_length INTEGER,
    product_photos_qty SMALLINT,
    product_weight_g INTEGER,
    product_length_cm NUMERIC(5,2),
    product_height_cm NUMERIC(5,2),
    product_width_cm NUMERIC(5,2)
);

COPY cpstn.olist_products (product_id, product_category_name, product_name_length, product_description_length, product_photos_qty, product_weight_g, product_length_cm, product_height_cm, product_width_cm)
FROM '/data/olist_products_dataset.csv' DELIMITER ',' CSV HEADER;

-- Create sellers table and import data
CREATE TABLE IF NOT EXISTS cpstn.olist_sellers
(
    seller_id uuid,
    seller_zip_code_prefix CHAR(5),
    seller_city VARCHAR(50),
    seller_state CHAR(2)
);

COPY cpstn.olist_sellers (seller_id, seller_zip_code_prefix, seller_city, seller_state)
FROM '/data/olist_sellers_dataset.csv' DELIMITER ',' CSV HEADER;

-- Create product category name translation table and import data
CREATE TABLE IF NOT EXISTS cpstn.product_category_name_translation
(
    category_name VARCHAR(48),
    category_name_english VARCHAR(40)
);

COPY cpstn.product_category_name_translation (category_name, category_name_english)
FROM '/data/product_category_name_translation.csv' DELIMITER ',' CSV HEADER;
