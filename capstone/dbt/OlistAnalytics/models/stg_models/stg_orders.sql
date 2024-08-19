

with source_orders as (

    select 
        order_id,
        customer_id,
        order_status,
        order_purchase_timestamp,
        order_approved_at,
        order_delivered_carrier_date,
        order_delivered_customer_date,
        order_estimated_delivery_date
    
    from {{ ref('orders') }}   
),

dbt_olist_raw_orders_data as (
    select * from source_orders
)

select * from dbt_olist_raw_orders_data

