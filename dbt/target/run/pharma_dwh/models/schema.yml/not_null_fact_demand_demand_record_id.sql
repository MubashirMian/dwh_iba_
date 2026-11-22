select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
    



select demand_record_id
from "dwh"."gold"."fact_demand"
where demand_record_id is null



      
    ) dbt_internal_test