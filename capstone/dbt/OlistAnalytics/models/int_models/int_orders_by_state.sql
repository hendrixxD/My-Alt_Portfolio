-- Count of orders per state.

with orders_count as (
    select 
        o.order_id,
        s.state_name
    from
        {{ ref('stg_orders') }} o
    join
        {{ ref('stg_customers') }} c
    on 
        o.customer_id = c.customer_id
    join
        {{ ref('stg_zip_codes') }} zc
    on
        c.customer_zip_code_prefix = zc.zip_code_prefix
    join
        {{ ref('stg_cities') }} s
    on
        zc.city_id = s.city_id
)

select
    count(*) as num_of_orders,
    state_name
from
	orders_count
group by
	state_name