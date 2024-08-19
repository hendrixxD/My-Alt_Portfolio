-- 1. Customers
CREATE TABLE customers (
    customer_id uuid PRIMARY KEY,
    customer_unique_id uuid,
    customer_zip_code_prefix varchar(6)
);

-- Explanation: This table is in 2NF because all attributes depend on the entire primary key (customer_id).

-- 2. Geolocation
CREATE TABLE geolocation (
    geolocation_zip_code_prefix varchar PRIMARY KEY,
    geolocation_lat decimal,
    geolocation_lng decimal
);

-- Explanation: This table is in 2NF because all attributes depend on the entire primary key (geolocation_zip_code_prefix).

-- 3. Cities
CREATE TABLE cities (
    city_id SERIAL PRIMARY KEY,
    city_name varchar,
    state_name varchar
);

-- Explanation: This table is in 2NF because all attributes depend on the entire primary key (city_id).

-- 4. Zip_Codes
CREATE TABLE zip_codes (
    zip_code_prefix varchar PRIMARY KEY,
    city_id int REFERENCES cities(city_id)
);

-- Explanation: This table is in 2NF because all attributes depend on the entire primary key (zip_code_prefix).

-- 5. Sellers
CREATE TABLE sellers (
    seller_id uuid PRIMARY KEY,
    seller_zip_code_prefix varchar REFERENCES zip_codes(zip_code_prefix)
);

-- Explanation: This table is in 2NF because all attributes depend on the entire primary key (seller_id).

-- 6. Products
CREATE TABLE products (
    product_id uuid PRIMARY KEY,
    product_category_name varchar(250),
    product_name_length integer,
    product_description_length integer,
    product_photos_qty integer,
    product_weight_g integer,
    product_length_cm integer,
    product_height_cm integer,
    product_width_cm integer
);

-- Explanation: This table is in 2NF because all attributes depend on the entire primary key (product_id).

-- 7. Product_Category_Translation
CREATE TABLE product_category_translation (
    product_category_name varchar(250) PRIMARY KEY,
    product_category_name_english varchar(250)
);

-- Explanation: This table is in 2NF because all attributes depend on the entire primary key (product_category_name).

-- 8. Orders
CREATE TABLE orders (
    order_id uuid PRIMARY KEY,
    customer_id uuid REFERENCES customers(customer_id),
    order_status varchar(50),
    order_purchase_timestamp timestamp,
    order_approved_at timestamp,
    order_delivered_carrier_date timestamp,
    order_delivered_customer_date timestamp,
    order_estimated_delivery_date timestamp
);

-- Explanation: This table is in 2NF because all attributes depend on the entire primary key (order_id).

-- 9. Order_Items
CREATE TABLE order_items (
    order_id uuid,
    order_item_id integer,
    product_id uuid REFERENCES products(product_id),
    seller_id uuid REFERENCES sellers(seller_id),
    shipping_limit_date timestamp,
    price decimal,
    freight_value decimal,
    PRIMARY KEY (order_id, order_item_id)
);

-- Explanation: This table is in 2NF because all attributes depend on the entire composite primary key (order_id, order_item_id).

-- 10. Order_Payments
CREATE TABLE order_payments (
    order_id uuid REFERENCES orders(order_id),
    payment_sequential integer,
    payment_type varchar,
    payment_installments integer,
    payment_value decimal,
    PRIMARY KEY (order_id, payment_sequential)
);

-- Explanation: This table is in 2NF because all attributes depend on the entire composite primary key (order_id, payment_sequential).

-- 11. Order_Reviews
CREATE TABLE order_reviews (
    review_id uuid PRIMARY KEY,
    order_id uuid REFERENCES orders(order_id),
    review_score integer,
    review_comment_title varchar,
    review_comment_message text,
    review_creation_date timestamp,
    review_answer_timestamp timestamp
);

-- Explanation: This table is in 2NF because all attributes depend on the entire primary key (review_id).