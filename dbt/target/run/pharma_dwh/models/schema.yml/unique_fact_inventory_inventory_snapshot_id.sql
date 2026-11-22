select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
    

select
    inventory_snapshot_id as unique_field,
    count(*) as n_records

from "dwh"."gold"."fact_inventory"
where inventory_snapshot_id is not null
group by inventory_snapshot_id
having count(*) > 1



      
    ) dbt_internal_test