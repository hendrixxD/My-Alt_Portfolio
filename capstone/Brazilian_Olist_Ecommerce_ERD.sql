CREATE TABLE "olist_customers" (
  "customer_id" uuid PRIMARY KEY,
  "customer_unique_id" uuid,
  "customer_zip_code_prefix" varchar(6),
  "customer_city" varchar(50),
  "customer_state" varchar(50)
);

CREATE TABLE "olist_geolocation" (
  "geolocation_zip_code_prefix" varchar,
  "geolocation_lat" integer,
  "geolocation_lng" integer,
  "geolocation_city" varchar,
  "geolocation_state" varchar
);

CREATE TABLE "olist_order_items" (
  "order_id" uuid,
  "order_item_id" integer PRIMARY KEY,
  "product_id" uuid,
  "seller_id" uuid,
  "shipping_limit_data" timestamp,
  "price" integer,
  "freight_value" integer
);

CREATE TABLE "olist_order_payments" (
  "order_id" uuid PRIMARY KEY,
  "payment_sequential" integer,
  "payment_type" varchar,
  "payment_installments" integer,
  "payment_value" integer
);

CREATE TABLE "olist_order_reviews" (
  "review_id" uuid PRIMARY KEY,
  "order_id" uuid,
  "review_score" integer,
  "review_comment_title" varchar,
  "review_comment_message" text,
  "review_creation_date" datetime,
  "review_answer_timestamp" datetime
);

CREATE TABLE "olist_orders" (
  "order_id" uuid PRIMARY KEY,
  "customer_id" uuid,
  "order_status" varchar(50),
  "order_purchase_timestamp" datetime,
  "order_approved_at" datetime,
  "order_delivered_carrier_date" datetime,
  "order_delivered_customer_date" datetime,
  "order_estimated_delievry_date" datetime
);

CREATE TABLE "olist_products" (
  "prodcut_id" uuid PRIMARY KEY,
  "product_categoty_name" varchar(250),
  "product_name_length" integer,
  "product_description_length" integer,
  "product_photos_qty" integer,
  "product_weight_g" integer,
  "product_length_cm" integer,
  "product_height_cm" integer,
  "product_width_cm" integer
);

CREATE TABLE "olist_sellers" (
  "seller_id" uuid PRIMARY KEY,
  "seller_zip_code_prefix" integer,
  "seller_city" varchar(70),
  "seller_state" char(3)
);

CREATE TABLE "olist_product_category_name_translation" (
  "category_name" varchar(250),
  "category_name_english" varchar(250)
);

COMMENT ON COLUMN "olist_order_reviews"."review_comment_title" IS 'Content of the post';

ALTER TABLE "olist_customers" ADD FOREIGN KEY ("customer_state") REFERENCES "olist_geolocation" ("geolocation_state");

ALTER TABLE "olist_order_reviews" ADD FOREIGN KEY ("order_id") REFERENCES "olist_orders" ("order_id");

ALTER TABLE "olist_order_items" ADD FOREIGN KEY ("product_id") REFERENCES "olist_products" ("prodcut_id");

ALTER TABLE "olist_order_payments" ADD FOREIGN KEY ("order_id") REFERENCES "olist_order_items" ("order_id");

ALTER TABLE "olist_orders" ADD FOREIGN KEY ("order_id") REFERENCES "olist_order_payments" ("order_id");

ALTER TABLE "olist_orders" ADD FOREIGN KEY ("customer_id") REFERENCES "olist_customers" ("customer_id");

ALTER TABLE "olist_products" ADD FOREIGN KEY ("product_categoty_name") REFERENCES "olist_product_category_name_translation" ("category_name");

ALTER TABLE "olist_order_items" ADD FOREIGN KEY ("seller_id") REFERENCES "olist_sellers" ("seller_id");
