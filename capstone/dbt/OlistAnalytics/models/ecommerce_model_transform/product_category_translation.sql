-- {{ config(materialized='table') }}

SELECT
    category_name,
    category_name_english
FROM {{ source('ecommerce_model_transform', 'product_category_name_translation') }}