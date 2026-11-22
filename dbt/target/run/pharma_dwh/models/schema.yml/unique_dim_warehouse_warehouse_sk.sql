select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
    

select
    warehouse_sk as unique_field,
    count(*) as n_records

from "dwh"."gold"."dim_warehouse"
where warehouse_sk is not null
group by warehouse_sk
having count(*) > 1



      
    ) dbt_internal_test