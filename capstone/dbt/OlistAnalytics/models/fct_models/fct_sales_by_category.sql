
with final_orders_by_state_model as (
    select
        *
    from
        {{ ref('int_orders_by_state') }}
)

select * from final_orders_by_state_model