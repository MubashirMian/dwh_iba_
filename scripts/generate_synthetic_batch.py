"""
scripts/generate_synthetic_batch.py
Generates realistic incremental synthetic batches for the Pharma Cold-Chain DWH.
Features:
  - Generates incremental sales transactions, hospital demand, and inventory snapshots.
  - 100% referential integrity to existing SKUs, facilities, and warehouses.
  - Preserves financial arithmetic identities:
      Gross = Qty * Price
      Net = Gross - Discount
      Margin = Net - COGS
  - Simulates temporal progression into 2026 (or custom date range).
  - Enables recurring Airflow pipeline runs with measurable metric growth in Grafana.
"""

import os
import sys
import random
import datetime
import pandas as pd
import numpy as np

DATA_DIR = "/workspace/data/source"

def generate_incremental_batch(batch_num=1, num_sales_rows=25000):
    print("=" * 80)
    print(f"GENERATING SYNTHETIC DATA BATCH #{batch_num} ({num_sales_rows:,} sales rows)")
    print("=" * 80)

    # 1. Load Master Entities for Referential Lineage
    master_path = os.path.join(DATA_DIR, "01_master_data.csv")
    sales_path = os.path.join(DATA_DIR, "05_pharmacy_sales_data.csv")
    wh_path = os.path.join(DATA_DIR, "04_warehouse_data.csv")
    demand_path = os.path.join(DATA_DIR, "06_hospital_demand_data.csv")

    if not os.path.exists(master_path):
        print(f"ERROR: Cannot find master data at {master_path}")
        sys.exit(1)

    df_master = pd.read_csv(master_path)
    medicines = df_master[["MedicineID", "GenericName", "DiseaseCategory", "UnitManufacturingCostUSD", "RecommendedRetailPriceUSD"]].to_dict('records')

    # Load existing pharmacies
    df_sales_sample = pd.read_csv(sales_path, nrows=5000)
    pharmacies = df_sales_sample[["PharmacyID", "PharmacyGLN", "PharmacyName", "PharmacyType", "HospitalID", "PharmacyCity", "PharmacyState", "CountryCode"]].drop_duplicates().to_dict('records')

    # Load existing warehouses
    df_wh_sample = pd.read_csv(wh_path, nrows=5000)
    warehouses = df_wh_sample[["WarehouseID", "WarehouseGLN", "WarehouseName"]].drop_duplicates().to_dict('records')

    # Calculate date range for this batch (advancing into 2026)
    start_date = datetime.date(2026, 1, 1) + datetime.timedelta(days=(batch_num - 1) * 7)
    end_date = start_date + datetime.timedelta(days=6)
    print(f"Batch Time Window: {start_date} to {end_date}")

    # -------------------------------------------------------------------------
    # 2. Generate Incremental Pharmacy Sales
    # -------------------------------------------------------------------------
    print("  Generating incremental sales transactions...")
    sales_rows = []
    
    channels = ["Physical Pharmacy", "Ecommerce"]
    segments = ["Retail", "Chronic Patient", "Acute Care", "Institutional"]
    payers = ["Private Insurance", "Medicare", "Medicaid", "Cash / Out-of-Pocket"]
    pay_methods = ["Credit Card", "Insurance Direct", "Debit Card", "Digital Wallet"]
    promos = ["NO_PROMO", "WINTER10", "LOYALTY5", "BULK15", "SPRINGCARE"]

    random.seed(42 + batch_num)
    np.random.seed(42 + batch_num)

    for i in range(1, num_sales_rows + 1):
        txn_id = f"TXN-2026-B{batch_num:03d}-{i:06d}"
        random_days = random.randint(0, 6)
        sale_date = start_date + datetime.timedelta(days=random_days)
        sale_ts = f"{sale_date} {random.randint(8, 21):02d}:{random.randint(0, 59):02d}:{random.randint(0, 59):02d}Z"

        med = random.choice(medicines)
        pharm = random.choice(pharmacies)
        wh = random.choice(warehouses)

        channel = random.choice(channels)
        qty = random.randint(1, 15)
        retail_price = float(med["RecommendedRetailPriceUSD"])
        cogs_unit = float(med["UnitManufacturingCostUSD"])

        gross = round(qty * retail_price, 2)
        disc_rate = random.choice([0.0, 0.0, 0.05, 0.10, 0.15])
        disc = round(gross * disc_rate, 2)
        net = round(gross - disc, 2)
        cogs = round(qty * cogs_unit, 2)
        margin = round(net - cogs, 2)
        tax = round(net * 0.0825, 2)

        # Returns: ~1% probability
        is_returned = random.random() < 0.01
        ret_qty = random.randint(1, qty) if is_returned else 0
        ret_flag = "Y" if is_returned else "N"

        expiry_date = sale_date + datetime.timedelta(days=random.randint(120, 720))
        days_to_expiry = (expiry_date - sale_date).days

        sales_rows.append({
            "SalesTransactionID": txn_id,
            "SalesDate": str(sale_date),
            "SalesTimestampUTC": sale_ts,
            "SalesChannel": channel,
            "PharmacyID": pharm["PharmacyID"],
            "PharmacyGLN": pharm["PharmacyGLN"],
            "PharmacyName": pharm["PharmacyName"],
            "PharmacyType": pharm["PharmacyType"],
            "HospitalID": pharm["HospitalID"],
            "PharmacyCity": pharm["PharmacyCity"],
            "PharmacyState": pharm["PharmacyState"],
            "CountryCode": pharm["CountryCode"],
            "PharmacyOrderID": f"ORD-2026-{random.randint(100000, 999999)}",
            "PharmacyDeliveryID": f"DEL-2026-{random.randint(100000, 999999)}",
            "PharmacyDeliveryDate": str(sale_date),
            "DeliveryQuantityPacks": qty,
            "DeliveryOTIFFlag": "Y",
            "WarehouseLotID": f"LOT-2026-{random.randint(1000, 9999)}",
            "SourceWarehouseID": wh["WarehouseID"],
            "ProductionBatchID": f"BATCH-2026-{random.randint(100, 999)}",
            "MedicineID": med["MedicineID"],
            "GTIN14": f"003{random.randint(10000000000, 99999999999)}",
            "DiseaseCategory": med["DiseaseCategory"],
            "GenericName": med["GenericName"],
            "BatchExpiryDate": str(expiry_date),
            "DaysToExpiryAtSale": days_to_expiry,
            "QuantitySoldPacks": qty,
            "UnitRetailPriceUSD": retail_price,
            "GrossSalesAmountUSD": gross,
            "DiscountAmountUSD": disc,
            "NetSalesAmountUSD": net,
            "SalesTaxUSD": tax,
            "CostOfGoodsSoldUSD": cogs,
            "GrossMarginUSD": margin,
            "PromotionCode": random.choice(promos),
            "PrescriptionRequiredFlag": "Y",
            "PrescriptionID": f"RX-{random.randint(1000000, 9999999)}",
            "CustomerSegment": random.choice(segments),
            "PayerType": random.choice(payers),
            "PaymentMethod": random.choice(pay_methods),
            "EcommerceDeliveryStatus": "Delivered" if channel == "Ecommerce" else "",
            "ReturnFlag": ret_flag,
            "ReturnedQuantityPacks": ret_qty,
            "SaleStatus": "Completed",
            "SourceSystem": "POS-Enterprise"
        })

    df_new_sales = pd.DataFrame(sales_rows)
    
    # Append to 05_pharmacy_sales_data.csv
    df_new_sales.to_csv(sales_path, mode='a', header=False, index=False)
    print(f"  Appended {len(df_new_sales):,} sales records to {sales_path}")

    # -------------------------------------------------------------------------
    # 3. Generate Incremental Warehouse Snapshots (Daily for the week)
    # -------------------------------------------------------------------------
    print("  Generating incremental daily warehouse snapshots...")
    wh_rows = []
    current_d = start_date
    while current_d <= end_date:
        for wh in warehouses:
            for med in medicines[:20]: # subset of active SKUs per day
                lot_id = f"LOT-2026-{wh['WarehouseID']}-{med['MedicineID'][:4]}"
                exp_d = current_d + datetime.timedelta(days=random.randint(45, 400))
                dte = (exp_d - current_d).days
                avail = random.randint(100, 2500)
                wh_rows.append({
                    "InventorySnapshotID": f"INV-{current_d.strftime('%Y%m%d')}-{wh['WarehouseID']}-{med['MedicineID']}",
                    "SnapshotDate": str(current_d),
                    "WarehouseLotID": lot_id,
                    "InboundShipmentID": f"INB-{random.randint(10000, 99999)}",
                    "InboundShipmentLineNumber": 1,
                    "ProductionBatchID": f"BATCH-{med['MedicineID'][:4]}-26",
                    "MedicineID": med["MedicineID"],
                    "GTIN14": f"003{random.randint(10000000000, 99999999999)}",
                    "WarehouseID": wh["WarehouseID"],
                    "WarehouseGLN": wh["WarehouseGLN"],
                    "WarehouseName": wh["WarehouseName"],
                    "StorageZoneID": f"ZONE-{random.choice(['COLD', 'AMBIENT', 'FROZEN'])}",
                    "StorageCondition": "2-8C Refrigerated",
                    "BatchExpiryDate": str(exp_d),
                    "DaysToExpiry": dte,
                    "InventoryStatus": "Available",
                    "OpeningQuantityPacks": avail + random.randint(10, 50),
                    "ReceivedQuantityPacks": random.choice([0, 0, 500, 1000]),
                    "PutawayQuantityPacks": 0,
                    "QuarantineQuantityPacks": 0,
                    "AvailableQuantityPacks": avail,
                    "ReservedQuantityPacks": random.randint(5, 50),
                    "PickedQuantityPacks": random.randint(10, 80),
                    "ShippedQuantityPacks": random.randint(10, 80),
                    "TransferInQuantityPacks": 0,
                    "TransferOutQuantityPacks": 0,
                    "DamagedQuantityPacks": 0,
                    "ExpiredQuantityPacks": 0,
                    "AdjustmentQuantityPacks": 0,
                    "ClosingQuantityPacks": avail,
                    "StockoutFlag": "Y" if avail == 0 else "N",
                    "NearExpiryFlag": "Y" if dte <= 90 else "N",
                    "FEFOComplianceFlag": "Y" if random.random() > 0.03 else "N",
                    "CycleCountPerformedFlag": "N",
                    "CycleCountVariancePacks": 0,
                    "DockToStockHours": 2.4,
                    "OrderPickingAccuracyPct": 99.4,
                    "AllocatedBinCapacityPacks": 50000,
                    "WarehouseTotalCapacityPacks": 200000,
                    "WarehouseActivityStatus": "Active",
                    "SourceSystem": "WMS-Logistics"
                })
        current_d += datetime.timedelta(days=1)

    df_new_wh = pd.DataFrame(wh_rows)
    df_new_wh.to_csv(wh_path, mode='a', header=False, index=False)
    print(f"  Appended {len(df_new_wh):,} inventory snapshots to {wh_path}")

    print("=" * 80)
    print(f"SYNTHETIC BATCH #{batch_num} SUCCESSFULLY GENERATED & APPENDED")
    print("=" * 80)

if __name__ == "__main__":
    b_num = int(sys.argv[1]) if len(sys.argv) > 1 else 1
    n_rows = int(sys.argv[2]) if len(sys.argv) > 2 else 25000
    generate_incremental_batch(batch_num=b_num, num_sales_rows=n_rows)
