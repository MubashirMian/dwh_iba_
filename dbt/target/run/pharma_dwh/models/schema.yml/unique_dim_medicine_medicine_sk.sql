select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
    

select
    medicine_sk as unique_field,
    count(*) as n_records

from "dwh"."gold"."dim_medicine"
where medicine_sk is not null
group by medicine_sk
having count(*) > 1



      
    ) dbt_internal_test