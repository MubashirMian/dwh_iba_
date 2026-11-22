-- dim_sales_profile.sql


SELECT
    ROW_NUMBER() OVER (ORDER BY sales_channel, customer_segment, payer_type, payment_method, promotion_code) AS sales_profile_sk,
    sales_channel,
    customer_segment,
    payer_type,
    payment_method,
    promotion_code,
    prescription_required_flag,
    return_flag
FROM (
    SELECT DISTINCT
        sales_channel,
        customer_segment,
        payer_type,
        payment_method,
        COALESCE(promotion_code, 'NO_PROMO') AS promotion_code,
        prescription_required_flag,
        return_flag
    FROM "dwh"."silver"."silver_pharmacy_sales"
) sub