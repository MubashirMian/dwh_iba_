-- silver_pharmacy_sales.sql


SELECT
    
    NULLIF(NULLIF(NULLIF(TRIM("salestransactionid"), ''), '\N'), 'NULL')
 AS sales_transaction_id,
    
    NULLIF(NULLIF(NULLIF(TRIM("salesdate"), ''), '\N'), 'NULL')
::DATE AS sales_date,
    
    NULLIF(NULLIF(NULLIF(TRIM("salestimestamputc"), ''), '\N'), 'NULL')
::TIMESTAMPTZ AS sales_timestamp_utc,
    
    NULLIF(NULLIF(NULLIF(TRIM("saleschannel"), ''), '\N'), 'NULL')
 AS sales_channel,
    
    NULLIF(NULLIF(NULLIF(TRIM("pharmacyid"), ''), '\N'), 'NULL')
 AS pharmacy_id,
    
    NULLIF(NULLIF(NULLIF(TRIM("pharmacygln"), ''), '\N'), 'NULL')
 AS pharmacy_gln,
    
    NULLIF(NULLIF(NULLIF(TRIM("pharmacyname"), ''), '\N'), 'NULL')
 AS pharmacy_name,
    
    NULLIF(NULLIF(NULLIF(TRIM("pharmacytype"), ''), '\N'), 'NULL')
 AS pharmacy_type,
    
    NULLIF(NULLIF(NULLIF(TRIM("hospitalid"), ''), '\N'), 'NULL')
 AS hospital_id,
    
    NULLIF(NULLIF(NULLIF(TRIM("pharmacycity"), ''), '\N'), 'NULL')
 AS city,
    
    NULLIF(NULLIF(NULLIF(TRIM("pharmacystate"), ''), '\N'), 'NULL')
 AS state,
    
    NULLIF(NULLIF(NULLIF(TRIM("countrycode"), ''), '\N'), 'NULL')
 AS country_code,
    
    NULLIF(NULLIF(NULLIF(TRIM("warehouselotid"), ''), '\N'), 'NULL')
 AS warehouse_lot_id,
    
    NULLIF(NULLIF(NULLIF(TRIM("sourcewarehouseid"), ''), '\N'), 'NULL')
 AS source_warehouse_id,
    
    NULLIF(NULLIF(NULLIF(TRIM("productionbatchid"), ''), '\N'), 'NULL')
 AS production_batch_id,
    
    NULLIF(NULLIF(NULLIF(TRIM("medicineid"), ''), '\N'), 'NULL')
 AS medicine_id,
    
    NULLIF(NULLIF(NULLIF(TRIM("gtin14"), ''), '\N'), 'NULL')
 AS gtin14,
    
    NULLIF(NULLIF(NULLIF(TRIM("diseasecategory"), ''), '\N'), 'NULL')
 AS disease_category,
    
    NULLIF(NULLIF(NULLIF(TRIM("genericname"), ''), '\N'), 'NULL')
 AS generic_name,
    
    NULLIF(NULLIF(NULLIF(TRIM("batchexpirydate"), ''), '\N'), 'NULL')
::DATE AS batch_expiry_date,
    
    NULLIF(NULLIF(NULLIF(TRIM("daystoexpiryatsale"), ''), '\N'), 'NULL')
::INT AS days_to_expiry_at_sale,
    
    NULLIF(NULLIF(NULLIF(TRIM("quantitysoldpacks"), ''), '\N'), 'NULL')
::INT AS quantity_sold_packs,
    
    NULLIF(NULLIF(NULLIF(TRIM("unitretailpriceusd"), ''), '\N'), 'NULL')
::NUMERIC(12, 2) AS unit_retail_price_usd,
    
    NULLIF(NULLIF(NULLIF(TRIM("grosssalesamountusd"), ''), '\N'), 'NULL')
::NUMERIC(14, 2) AS gross_sales_amount_usd,
    
    NULLIF(NULLIF(NULLIF(TRIM("discountamountusd"), ''), '\N'), 'NULL')
::NUMERIC(14, 2) AS discount_amount_usd,
    
    NULLIF(NULLIF(NULLIF(TRIM("netsalesamountusd"), ''), '\N'), 'NULL')
::NUMERIC(14, 2) AS net_sales_amount_usd,
    
    NULLIF(NULLIF(NULLIF(TRIM("salestaxusd"), ''), '\N'), 'NULL')
::NUMERIC(14, 2) AS sales_tax_usd,
    
    NULLIF(NULLIF(NULLIF(TRIM("costofgoodssoldusd"), ''), '\N'), 'NULL')
::NUMERIC(14, 2) AS cost_of_goods_sold_usd,
    
    NULLIF(NULLIF(NULLIF(TRIM("grossmarginusd"), ''), '\N'), 'NULL')
::NUMERIC(14, 2) AS gross_margin_usd,
    COALESCE(
    NULLIF(NULLIF(NULLIF(TRIM("promotioncode"), ''), '\N'), 'NULL')
, 'NO_PROMO') AS promotion_code,
    
    NULLIF(NULLIF(NULLIF(TRIM("prescriptionrequiredflag"), ''), '\N'), 'NULL')
 AS prescription_required_flag,
    
    NULLIF(NULLIF(NULLIF(TRIM("customersegment"), ''), '\N'), 'NULL')
 AS customer_segment,
    
    NULLIF(NULLIF(NULLIF(TRIM("payertype"), ''), '\N'), 'NULL')
 AS payer_type,
    
    NULLIF(NULLIF(NULLIF(TRIM("paymentmethod"), ''), '\N'), 'NULL')
 AS payment_method,
    
    NULLIF(NULLIF(NULLIF(TRIM("returnflag"), ''), '\N'), 'NULL')
 AS return_flag,
    
    NULLIF(NULLIF(NULLIF(TRIM("returnedquantitypacks"), ''), '\N'), 'NULL')
::INT AS returned_quantity_packs,
    
    NULLIF(NULLIF(NULLIF(TRIM("salestatus"), ''), '\N'), 'NULL')
 AS sale_status,
    _loaded_at,
    _row_id
FROM bronze.pharmacy_sales_data
WHERE 
    NULLIF(NULLIF(NULLIF(TRIM("salestransactionid"), ''), '\N'), 'NULL')
 IS NOT NULL