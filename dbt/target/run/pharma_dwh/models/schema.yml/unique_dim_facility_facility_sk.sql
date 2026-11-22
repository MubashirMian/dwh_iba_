select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
    

select
    facility_sk as unique_field,
    count(*) as n_records

from "dwh"."gold"."dim_facility"
where facility_sk is not null
group by facility_sk
having count(*) > 1



      
    ) dbt_internal_test