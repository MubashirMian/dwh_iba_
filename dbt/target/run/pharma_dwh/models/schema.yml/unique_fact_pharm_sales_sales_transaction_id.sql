select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
    

select
    sales_transaction_id as unique_field,
    count(*) as n_records

from "dwh"."gold"."fact_pharm_sales"
where sales_transaction_id is not null
group by sales_transaction_id
having count(*) > 1



      
    ) dbt_internal_test