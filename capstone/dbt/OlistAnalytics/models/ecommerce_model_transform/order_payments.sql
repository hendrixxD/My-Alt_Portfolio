-- {{ config(materialized='table') }}

SELECT
    order_id,
    payment_sequential,
    payment_type,
    payment_installments,
    payment_value
FROM {{ source('ecommerce_model_transform', 'olist_order_payments') }}