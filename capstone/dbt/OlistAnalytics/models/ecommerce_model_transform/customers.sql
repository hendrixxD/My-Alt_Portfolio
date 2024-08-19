-- {{ config(materialized='table') }}

SELECT DISTINCT
    customer_id,
    customer_unique_id,
    customer_zip_code_prefix
FROM {{ source('ecommerce_model_transform', 'olist_customers') }}