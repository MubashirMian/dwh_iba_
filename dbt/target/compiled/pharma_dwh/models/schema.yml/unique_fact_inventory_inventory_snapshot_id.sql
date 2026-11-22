
    
    

select
    inventory_snapshot_id as unique_field,
    count(*) as n_records

from "dwh"."gold"."fact_inventory"
where inventory_snapshot_id is not null
group by inventory_snapshot_id
having count(*) > 1


