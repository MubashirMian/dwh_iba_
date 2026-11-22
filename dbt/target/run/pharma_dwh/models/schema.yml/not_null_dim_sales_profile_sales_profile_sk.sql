select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
    



select sales_profile_sk
from "dwh"."gold"."dim_sales_profile"
where sales_profile_sk is null



      
    ) dbt_internal_test