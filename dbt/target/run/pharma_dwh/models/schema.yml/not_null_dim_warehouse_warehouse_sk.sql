select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
    



select warehouse_sk
from "dwh"."gold"."dim_warehouse"
where warehouse_sk is null



      
    ) dbt_internal_test