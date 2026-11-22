
    
    

with child as (
    select facility_sk as from_field
    from "dwh"."gold"."fact_pharm_sales"
    where facility_sk is not null
),

parent as (
    select facility_sk as to_field
    from "dwh"."gold"."dim_facility"
)

select
    from_field

from child
left join parent
    on child.from_field = parent.to_field

where parent.to_field is null


