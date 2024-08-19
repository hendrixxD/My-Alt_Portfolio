-- Aggregated sales data by product category.

with sales as (
    select
        o.order_id,
        p.product_category_name,
        oi.price
    from
        {{ ref('stg_orders') }} o
    join
        {{ ref('stg_order_items') }} oi
    on
        o.order_id = oi.order_id
    join
        {{ ref('stg_products') }} p
    on
        oi.product_id = p.product_id
)
select
    product_category_name,
    sum(price) as total_sales
from
    sales
group by
    product_category_name
