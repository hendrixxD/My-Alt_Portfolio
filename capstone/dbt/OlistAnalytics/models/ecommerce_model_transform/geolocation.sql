-- {{ config(materialized='table') }}

SELECT DISTINCT
    geolocation_zip_code_prefix,
    geolocation_lat,
    geolocation_lng
FROM {{ source('ecommerce_model_transform', 'olist_geolocation') }}