
    
    

select
    sales_profile_sk as unique_field,
    count(*) as n_records

from "dwh"."gold"."dim_sales_profile"
where sales_profile_sk is not null
group by sales_profile_sk
having count(*) > 1


