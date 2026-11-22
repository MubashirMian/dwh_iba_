
    
    

select
    facility_sk as unique_field,
    count(*) as n_records

from "dwh"."gold"."dim_facility"
where facility_sk is not null
group by facility_sk
having count(*) > 1


