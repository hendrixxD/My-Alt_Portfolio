

with 

source_customers as (

    select 
        customer_id,
        customer_unique_id,
        customer_zip_code_prefix
    
    from {{ ref('customers') }}
)

select * from source_customers

