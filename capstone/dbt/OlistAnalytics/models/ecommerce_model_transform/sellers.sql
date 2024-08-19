-- {{ config(materialized='table') }}

SELECT DISTINCT
    seller_id,
    seller_zip_code_prefix
FROM {{ source('ecommerce_model_transform', 'olist_sellers') }}