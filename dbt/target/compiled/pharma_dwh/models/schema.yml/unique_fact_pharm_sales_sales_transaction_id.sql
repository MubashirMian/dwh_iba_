
    
    

select
    sales_transaction_id as unique_field,
    count(*) as n_records

from "dwh"."gold"."fact_pharm_sales"
where sales_transaction_id is not null
group by sales_transaction_id
having count(*) > 1


