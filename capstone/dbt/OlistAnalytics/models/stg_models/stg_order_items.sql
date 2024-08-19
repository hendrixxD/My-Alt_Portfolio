
with raw_order_items as (
    select 
        * 
    from
        {{ ref('order_items') }} 
)

select * from raw_order_items