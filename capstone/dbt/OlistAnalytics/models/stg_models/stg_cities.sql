
with raw_cities as (
    
    select 
        * 
    from
        {{ ref('cities')}}
)

select * from raw_cities