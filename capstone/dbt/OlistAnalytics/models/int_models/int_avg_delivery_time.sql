
-- -- calculated average delivery time for each order
-- -- thia is the average delivery time is the difference between the order_delivered_customer_date and the order_purchase_timestamp

-- with avg_delivery_time as (
--     select 
--         o.order_id,
--         o.order_purchase_timestamp as opts,
--         o.order_delivered_customer_date as odcs,
--         timestamp_diff(odcs, opts, day) dilivery_time_diff
--     from
--         {{ ref('stg_orders') }} o
--     where
--         order_status = 'delivered'
--     and
--         -- this ensures that only orders that have been delivered
--         o.order_delivered_customer_date is not null
--     and order_delivered_customer_date > order_purchase_timestamp
-- )

-- select 
--     order_id,
--     avg(dilivery_time_diff) average_dilivery_time_per_order
-- from
--     avg_delivery_time
-- group by
--     order_id
-- order by
--     average_dilivery_time_per_order


-- calculated average delivery time for each order
-- thia is the average delivery time is the difference between the order_delivered_customer_date and the order_purchase_timestamp

with avg_delivery_time as (
    select 
        o.order_id,
        o.order_purchase_timestamp,
        o.order_delivered_customer_date,
        timestamp_diff(order_delivered_customer_date, order_purchase_timestamp, MINUTE) dilivery_time_min_diff
    from
        {{ ref('stg_orders') }} o
    where
    	o.order_status = 'delivered' and
        o.order_delivered_customer_date is not null
        and o.order_delivered_customer_date > o.order_purchase_timestamp
)

select 
    order_id,
    avg(dilivery_time_min_diff) average_dilivery_time_per_order,
    avg(dilivery_time_min_diff) / 60 as avg_delivery_time_hours,
    avg(dilivery_time_min_diff) / (60 * 24) as avg_delivery_time_days
from
	avg_delivery_time
group by
	order_id
order by
	average_dilivery_time_per_order
