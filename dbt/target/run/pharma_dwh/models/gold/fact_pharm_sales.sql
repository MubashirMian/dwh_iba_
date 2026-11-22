
  
    

  create  table "dwh"."gold"."fact_pharm_sales__dbt_tmp"
  
  
    as
  
  (
    -- fact_pharm_sales.sql


SELECT
    s.sales_transaction_id,
    d.date_key,
    m.medicine_sk,
    f.facility_sk,
    w.warehouse_sk,
    sp.sales_profile_sk,
    s.warehouse_lot_id,
    s.production_batch_id,
    s.quantity_sold_packs,
    s.unit_retail_price_usd,
    s.gross_sales_amount_usd,
    s.discount_amount_usd,
    s.net_sales_amount_usd,
    s.sales_tax_usd,
    s.cost_of_goods_sold_usd,
    s.gross_margin_usd,
    s.returned_quantity_packs,
    s.days_to_expiry_at_sale
FROM "dwh"."silver"."silver_pharmacy_sales" s
JOIN "dwh"."gold"."dim_date" d 
  ON d.date_key = TO_CHAR(s.sales_date, 'YYYYMMDD')::INT
JOIN "dwh"."gold"."dim_medicine" m 
  ON s.medicine_id = m.medicine_id 
 AND s.sales_date >= m.effective_start_date 
 AND s.sales_date < m.effective_end_date
JOIN "dwh"."gold"."dim_facility" f 
  ON s.pharmacy_id = f.facility_id
LEFT JOIN "dwh"."gold"."dim_warehouse" w 
  ON s.source_warehouse_id = w.warehouse_id
JOIN "dwh"."gold"."dim_sales_profile" sp
  ON s.sales_channel = sp.sales_channel
 AND s.customer_segment = sp.customer_segment
 AND s.payer_type = sp.payer_type
 AND s.payment_method = sp.payment_method
 AND COALESCE(s.promotion_code, 'NO_PROMO') = sp.promotion_code
 AND s.prescription_required_flag = sp.prescription_required_flag
 AND s.return_flag = sp.return_flag
  );
  