

with raw_zipcodes as (
    
    select 
        * 
    from
        {{ ref('zip_codes')}}
)

select * from raw_zipcodes