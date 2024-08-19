
with final_sales_by_category_model as (
    select
        *
    from
        {{ ref('int_sales_by_category') }}
)

select * from final_sales_by_category_model