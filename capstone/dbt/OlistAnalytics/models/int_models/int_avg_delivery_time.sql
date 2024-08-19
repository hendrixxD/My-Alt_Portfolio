

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
