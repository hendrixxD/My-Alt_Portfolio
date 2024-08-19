-- {{ config(materialized='table') }}

SELECT DISTINCT
    g.geolocation_zip_code_prefix AS zip_code_prefix,
    c.city_id
FROM {{ source('ecommerce_model_transform', 'olist_geolocation') }} g
JOIN {{ ref('cities') }} c
    ON g.geolocation_city = c.city_name
    AND g.geolocation_state = c.state_name