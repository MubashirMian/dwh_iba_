select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
    



select inventory_snapshot_id
from "dwh"."gold"."fact_inventory"
where inventory_snapshot_id is null



      
    ) dbt_internal_test