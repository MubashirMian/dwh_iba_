select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
    



select sales_transaction_id
from "dwh"."gold"."fact_pharm_sales"
where sales_transaction_id is null



      
    ) dbt_internal_test