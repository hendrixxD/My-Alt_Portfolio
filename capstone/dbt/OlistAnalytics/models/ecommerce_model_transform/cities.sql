-- {{ config(materialized='table') }}

WITH all_cities AS (

    SELECT DISTINCT

        geolocation_city AS city_name,
        geolocation_state AS state_name

    FROM
        {{ source('ecommerce_model_transform', 'olist_geolocation') }}

    UNION ALL

    SELECT DISTINCT 

        customer_city, 
        customer_state

    FROM 

        {{ source('ecommerce_model_transform', 'olist_customers') }}

    UNION ALL

    SELECT DISTINCT 

        seller_city, 
        seller_state

    FROM 
        {{ source('ecommerce_model_transform', 'olist_sellers') }}
)

SELECT

    ROW_NUMBER() OVER (ORDER BY city_name, state_name) AS city_id,
    city_name,
    state_name

FROM 
    all_cities