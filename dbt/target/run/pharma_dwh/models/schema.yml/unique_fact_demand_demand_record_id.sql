select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
    

select
    demand_record_id as unique_field,
    count(*) as n_records

from "dwh"."gold"."fact_demand"
where demand_record_id is not null
group by demand_record_id
having count(*) > 1



      
    ) dbt_internal_test