
with final_avg_dilivery_time_model as (
    select
        *
    from
        {{ ref('int_avg_delivery_time') }}
)

select * from final_avg_dilivery_time_model