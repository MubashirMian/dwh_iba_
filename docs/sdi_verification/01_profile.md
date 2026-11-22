# Data Profile Report: Pharmaceutical Cold Chain Datasets
Generated automatically by `scripts/verify_sdi.py`.

## 1. File Inventory and Row Count Verification

| File Name | Documented Spec Rows | Actual Discovered Rows | Status | Primary Key Check |
|---|---|---|---|---|
| `01_master_data.csv` | 63 | 63 | **MATCH** | 100% UNIQUE |
| `02_manufacturing_data.csv` | 561 | 561 | **MATCH** | 100% UNIQUE |
| `03_manufacturer_delivery_data.csv` | 999 | 999 | **MATCH** | 102 DUPLICATES |
| `04_warehouse_data.csv` | 112,184 | 112,184 | **MATCH** | 100% UNIQUE |
| `05_pharmacy_sales_data.csv` | 500,000 | 500,000 | **MATCH** | 100% UNIQUE |
| `06_hospital_demand_data.csv` | 27,216 | 27,216 | **MATCH** | 100% UNIQUE |
| `07_iot_streaming_data.csv` | 293,425 | 293,425 | **MATCH** | 100% UNIQUE |
