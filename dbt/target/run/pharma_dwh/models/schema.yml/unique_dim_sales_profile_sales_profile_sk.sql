select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
    

select
    sales_profile_sk as unique_field,
    count(*) as n_records

from "dwh"."gold"."dim_sales_profile"
where sales_profile_sk is not null
group by sales_profile_sk
having count(*) > 1



      
    ) dbt_internal_test