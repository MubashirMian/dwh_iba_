
    
    

with child as (
    select medicine_sk as from_field
    from "dwh"."gold"."fact_inventory"
    where medicine_sk is not null
),

parent as (
    select medicine_sk as to_field
    from "dwh"."gold"."dim_medicine"
)

select
    from_field

from child
left join parent
    on child.from_field = parent.to_field

where parent.to_field is null


