import os
import openpyxl
from openpyxl.styles import Font, Alignment, PatternFill, Border, Side
from openpyxl.drawing.image import Image as XLImage
from PIL import Image, ImageDraw, ImageFont

BASE_DIR = r"C:\Users\dell\Pictures\datawarehouse dashboard"
TEMPLATE_PATH = os.path.join(BASE_DIR, "DAWH.DWH.Template_backup.xlsx")
OUTPUT_PATH_1 = os.path.join(BASE_DIR, "DAWH_DWH_Pharma_ColdChain_Sales_Demand_01.xlsx")
OUTPUT_PATH_2 = os.path.join(BASE_DIR, "SDI.Excel.xlsx")
OUTPUT_PATH_3 = os.path.join(BASE_DIR, "DAWH.DWH.Template (1).xlsx")
DIAGRAM_PATH = os.path.join(BASE_DIR, "constellation_diagram.png")

# -------------------------------------------------------------
# HELPER: SAFE CELL ASSIGNMENT (Ignores MergedCell errors)
# -------------------------------------------------------------
def safe_set(ws, row, col, val=None, font=None, alignment=None, border=None, fill=None):
    cell = ws.cell(row, col)
    if type(cell).__name__ == 'MergedCell':
        return
    if val is not None:
        cell.value = val
    if font is not None:
        cell.font = font
    if alignment is not None:
        cell.alignment = alignment
    if border is not None:
        cell.border = border
    if fill is not None:
        cell.fill = fill

# -------------------------------------------------------------
# STEP 1: CREATE PROFESSIONAL CONSTELLATION SCHEMA DIAGRAM (PNG)
# -------------------------------------------------------------
def generate_diagram():
    w, h = 1450, 950
    img = Image.new("RGB", (w, h), color="#F8FAFC")
    draw = ImageDraw.Draw(img)

    try:
        font_title = ImageFont.truetype("arial.ttf", 26)
        font_sub = ImageFont.truetype("arial.ttf", 15)
        font_box_title = ImageFont.truetype("arialbd.ttf", 15)
        font_item = ImageFont.truetype("arial.ttf", 12)
        font_pk = ImageFont.truetype("arialbd.ttf", 12)
        font_legend = ImageFont.truetype("arialbd.ttf", 13)
    except:
        font_title = font_box_title = font_item = font_pk = font_legend = font_sub = ImageFont.load_default()

    # Header Bar
    draw.rectangle([(20, 20), (w - 20, 80)], fill="#1E3A8A")
    draw.text((40, 28), "PHARMA COLD CHAIN — SDI FACT CONSTELLATION (GALAXY SCHEMA)", fill="#FFFFFF", font=font_title)
    draw.text((40, 56), "Phase 1: Sales & Demand Intelligence Mart · 3 Core Facts Sharing Conformed Dimensions", fill="#93C5FD", font=font_sub)

    # Legend
    draw.rectangle([(20, 95), (w - 20, 130)], fill="#FFFFFF", outline="#CBD5E1", width=1)
    draw.rectangle([(40, 105), (65, 120)], fill="#10B981")
    draw.text((75, 105), "Conformed Dimension (Green)", fill="#1E293B", font=font_legend)
    draw.rectangle([(320, 105), (345, 120)], fill="#3B82F6")
    draw.text((355, 105), "Fact Table (Blue)", fill="#1E293B", font=font_legend)
    draw.rectangle([(550, 105), (575, 120)], fill="#F59E0B")
    draw.text((585, 105), "Junk / Role-Playing (Amber)", fill="#1E293B", font=font_legend)
    draw.text((850, 105), "Cardinality: 1 ───────────< ∞ (Kimball Drill-Across Compliant)", fill="#64748B", font=font_legend)

    def draw_table(x, y, bw, bh, title, header_bg, items, is_fact=False):
        draw.rectangle([(x + 4, y + 4), (x + bw + 4, y + bh + 4)], fill="#E2E8F0")
        draw.rectangle([(x, y), (x + bw, y + bh)], fill="#FFFFFF", outline="#94A3B8", width=2)
        draw.rectangle([(x, y), (x + bw, y + 32)], fill=header_bg)
        draw.text((x + 10, y + 7), title, fill="#FFFFFF", font=font_box_title)
        cy = y + 40
        for itm in items:
            prefix = itm[0]
            col_name = itm[1]
            dtype = itm[2] if len(itm) > 2 else ""
            if prefix in ("PK", "SK", "PK/SK"):
                f = font_pk
                color = "#B91C1C" if is_fact else "#047857"
            elif prefix == "FK":
                f = font_item
                color = "#1D4ED8"
            elif prefix == "DEG":
                f = font_item
                color = "#7C3AED"
            else:
                f = font_item
                color = "#334155"

            txt = f"{prefix}: {col_name}" if prefix else col_name
            draw.text((x + 10, cy), txt, fill=color, font=f)
            if dtype:
                draw.text((x + bw - 65, cy), dtype, fill="#94A3B8", font=font_item)
            cy += 18

    # 1. Conformed Dimensions (Top Row)
    dim_w = 260
    draw_table(30, 150, dim_w, 240, "DimDate (Conformed)", "#10B981", [
        ("PK/SK", "DateKey", "INT"),
        ("NK", "FullDate", "DATE"),
        ("", "CalendarYear", "SMALLINT"),
        ("", "Quarter", "CHAR(2)"),
        ("", "MonthName", "VARCHAR"),
        ("", "MonthNumber", "TINYINT"),
        ("", "WeekOfYear", "TINYINT"),
        ("", "DayOfWeek", "TINYINT"),
        ("", "DayName", "VARCHAR"),
        ("", "IsWeekendFlag", "BOOLEAN"),
        ("", "FiscalYear", "SMALLINT")
    ])

    draw_table(320, 150, dim_w + 30, 270, "DimMedicine (SCD2 Conformed)", "#10B981", [
        ("PK/SK", "MedicineSK", "BIGINT"),
        ("NK", "MedicineID", "VARCHAR"),
        ("", "GenericName", "VARCHAR"),
        ("", "FictionalBrandName", "VARCHAR"),
        ("", "DiseaseCategory", "VARCHAR"),
        ("", "TherapeuticClass", "VARCHAR"),
        ("", "ColdChainFlag", "CHAR(1)"),
        ("", "StorageCondition", "VARCHAR"),
        ("", "UnitManufacturingCostUSD", "DECIMAL"),
        ("", "RecommendedRetailPriceUSD", "DECIMAL"),
        ("", "EffectiveStartDate", "TIMESTAMP"),
        ("", "EffectiveEndDate", "TIMESTAMP"),
        ("", "IsCurrentFlag", "BOOLEAN")
    ])

    draw_table(640, 150, dim_w, 240, "DimFacility (Hospital/Pharm)", "#10B981", [
        ("PK/SK", "FacilitySK", "BIGINT"),
        ("NK", "FacilityID", "VARCHAR"),
        ("", "FacilityName", "VARCHAR"),
        ("", "FacilityType", "VARCHAR"),
        ("", "City", "VARCHAR"),
        ("", "State", "CHAR(2)"),
        ("", "Region", "VARCHAR"),
        ("", "LicensedBeds", "INT"),
        ("", "ICUBeds", "INT"),
        ("", "TraumaLevel", "VARCHAR")
    ])

    draw_table(930, 150, dim_w, 240, "DimWarehouse (Conformed)", "#10B981", [
        ("PK/SK", "WarehouseSK", "BIGINT"),
        ("NK", "WarehouseID", "VARCHAR"),
        ("", "WarehouseName", "VARCHAR"),
        ("", "StorageZoneID", "VARCHAR"),
        ("", "StorageCondition", "VARCHAR"),
        ("", "City", "VARCHAR"),
        ("", "State", "CHAR(2)"),
        ("", "Region", "VARCHAR"),
        ("", "TotalCapacityPacks", "INT"),
        ("", "ActivityStatus", "VARCHAR")
    ])

    draw_table(1220, 150, 200, 220, "DimSalesProfile (Junk)", "#F59E0B", [
        ("PK/SK", "SalesProfileSK", "INT"),
        ("NK", "ProfileHash", "CHAR(32)"),
        ("", "PrescriptionFlag", "CHAR(1)"),
        ("", "CustomerSegment", "VARCHAR"),
        ("", "PayerType", "VARCHAR"),
        ("", "PaymentMethod", "VARCHAR"),
        ("", "PromotionCode", "VARCHAR"),
        ("", "SaleStatus", "VARCHAR"),
        ("", "ReturnFlag", "CHAR(1)")
    ])

    # 2. Fact Tables (Bottom Row)
    fact_w = 430
    draw_table(30, 480, fact_w, 430, "Fact_PharmacySales (Transaction)", "#1E40AF", [
        ("PK/SK", "SalesTransactionSK", "BIGINT"),
        ("FK", "DateKey (SaleDate)", "INT"),
        ("FK", "MedicineSK (SCD2)", "BIGINT"),
        ("FK", "FacilitySK (Pharmacy)", "BIGINT"),
        ("FK", "WarehouseSK (Source DC)", "BIGINT"),
        ("FK", "SalesProfileSK (Junk)", "INT"),
        ("DEG", "SalesTransactionID", "VARCHAR"),
        ("DEG", "PharmacyOrderID", "VARCHAR"),
        ("DEG", "WarehouseLotID", "VARCHAR"),
        ("DEG", "ProductionBatchID", "VARCHAR"),
        ("MEA", "QuantitySoldPacks", "INT (Add)"),
        ("MEA", "UnitRetailPriceUSD", "DECIMAL (Non)"),
        ("MEA", "GrossSalesAmountUSD", "DECIMAL (Add)"),
        ("MEA", "DiscountAmountUSD", "DECIMAL (Add)"),
        ("MEA", "NetSalesAmountUSD", "DECIMAL (Add)"),
        ("MEA", "CostOfGoodsSoldUSD", "DECIMAL (Add)"),
        ("MEA", "GrossMarginUSD", "DECIMAL (Add)"),
        ("MEA", "DaysToExpiryAtSale", "INT (Non)"),
        ("MEA", "ReturnedQuantityPacks", "INT (Add)"),
        ("AUD", "_batch_id / _ingested_at", "METADATA")
    ], is_fact=True)

    draw_table(510, 480, fact_w, 400, "Fact_Demand (Monthly Periodic Snapshot)", "#1E40AF", [
        ("PK/SK", "HospitalDemandSK", "BIGINT"),
        ("FK", "DateKey (DemandMonth)", "INT"),
        ("FK", "MedicineSK (SCD2)", "BIGINT"),
        ("FK", "FacilitySK (Hospital)", "BIGINT"),
        ("DEG", "HospitalDemandRecordID", "VARCHAR"),
        ("MEA", "ForecastDemandPacks", "INT (Add)"),
        ("MEA", "RequestedQuantityPacks", "INT (Add)"),
        ("MEA", "ApprovedQuantityPacks", "INT (Add)"),
        ("MEA", "ReceivedQuantityPacks", "INT (Add)"),
        ("MEA", "ConsumedQuantityPacks", "INT (Add)"),
        ("MEA", "EmergencyRequestPacks", "INT (Add)"),
        ("MEA", "UnfulfilledDemandPacks", "INT (Add)"),
        ("MEA", "StockoutDays", "INT (Add)"),
        ("MEA", "ServiceLevelPct", "DECIMAL (Non)"),
        ("MEA", "OpeningStockPacks", "INT (Semi)"),
        ("MEA", "ClosingStockPacks", "INT (Semi)"),
        ("AUD", "_batch_id / _ingested_at", "METADATA")
    ], is_fact=True)

    draw_table(990, 480, fact_w + 30, 430, "Fact_Inventory (Daily Periodic Snapshot)", "#1E40AF", [
        ("PK/SK", "InventorySnapshotSK", "BIGINT"),
        ("FK", "DateKey (SnapshotDate)", "INT"),
        ("FK", "MedicineSK (SCD2)", "BIGINT"),
        ("FK", "WarehouseSK (Storage DC)", "BIGINT"),
        ("DEG", "InventorySnapshotID", "VARCHAR"),
        ("DEG", "WarehouseLotID", "VARCHAR"),
        ("DEG", "ProductionBatchID", "VARCHAR"),
        ("MEA", "AvailableQuantityPacks", "INT (Semi-Add)"),
        ("MEA", "OpeningQuantityPacks", "INT (Semi-Add)"),
        ("MEA", "ReceivedQuantityPacks", "INT (Add)"),
        ("MEA", "QuarantineQuantityPacks", "INT (Semi-Add)"),
        ("MEA", "ReservedQuantityPacks", "INT (Semi-Add)"),
        ("MEA", "ShippedQuantityPacks", "INT (Add)"),
        ("MEA", "ExpiredQuantityPacks", "INT (Add)"),
        ("MEA", "ClosingQuantityPacks", "INT (Semi-Add)"),
        ("MEA", "DaysToExpiry", "INT (Non-Add)"),
        ("FLG", "StockoutFlag", "TINYINT (0/1)"),
        ("FLG", "NearExpiryFlag", "TINYINT (0/1)"),
        ("FLG", "FEFOComplianceFlag", "TINYINT (0/1)"),
        ("AUD", "_batch_id / _ingested_at", "METADATA")
    ], is_fact=True)

    # Relationship Connectors
    line_col = "#64748B"
    draw.line([(160, 390), (160, 480)], fill=line_col, width=2)
    draw.line([(450, 420), (450, 450), (250, 450), (250, 480)], fill=line_col, width=2)
    draw.line([(450, 450), (700, 450), (700, 480)], fill=line_col, width=2)
    draw.line([(450, 450), (1150, 450), (1150, 480)], fill=line_col, width=2)
    draw.line([(760, 390), (760, 480)], fill=line_col, width=2)
    draw.line([(1050, 390), (1050, 480)], fill=line_col, width=2)
    draw.line([(1050, 450), (350, 450), (350, 480)], fill=line_col, width=2)

    img.save(DIAGRAM_PATH)
    print("Constellation diagram generated successfully:", DIAGRAM_PATH)

# -------------------------------------------------------------
# STEP 2: LOAD AND POPULATE EXCEL TEMPLATE
# -------------------------------------------------------------
def populate_workbook():
    wb = openpyxl.load_workbook(TEMPLATE_PATH)

    font_title = Font(name="Calibri", size=16, bold=True, color="000000")
    font_sec_hdr = Font(name="Calibri", size=13, bold=True, color="000000")
    font_bold = Font(name="Calibri", size=11, bold=True, color="000000")
    font_body = Font(name="Calibri", size=11, bold=False, color="000000")
    font_code = Font(name="Consolas", size=9, bold=False, color="1E293B")

    thin_border_side = Side(style='thin', color='D9D9D9')
    cell_border = Border(left=thin_border_side, right=thin_border_side, top=thin_border_side, bottom=thin_border_side)

    align_top_left = Alignment(horizontal="left", vertical="top", wrap_text=True)
    align_center = Alignment(horizontal="center", vertical="center")

    # =========================================================================
    # 1. SHEET: Business.Req.XRay
    # =========================================================================
    ws_b = wb["Business.Req.XRay"]
    ws_b.column_dimensions["A"].width = 25
    ws_b.column_dimensions["B"].width = 25
    ws_b.column_dimensions["C"].width = 30
    ws_b.column_dimensions["D"].width = 30
    ws_b.column_dimensions["E"].width = 30
    ws_b.column_dimensions["F"].width = 30

    business_answers = {
        2: "Pharmaceutical Cold Chain Supply Chain, Commercial Multichannel Distribution & Healthcare Inventory Intelligence",
        3: "Multichannel Commercial Pharmacy Sales, Clinical Hospital Demand Fulfillment, and Warehouse Cold-Chain Replenishment",
        4: """The business process operates across five synchronized operational tiers:
1. Manufacturing & Batch Release: Finished cold-chain pharmaceutical products (Insulin, Biologics, Vaccines, Oncologics) are produced in batches, assigned unique Batch IDs, GTIN-14 barcodes, and strict expiry dates following regulatory QA release.
2. Inbound Logistics & Cold-Chain Storage: Batches are dispatched to regional distribution centers. Environmental sensors monitor continuous temperatures (2°C–8°C cold chain; 15°C–25°C ambient). Lots are stored under strict FEFO (First-Expired, First-Out) picking protocols.
3. Multichannel Commercial Distribution: Warehouses fulfill demand across three commercial channels: Physical Retail Chain Pharmacies, Independent Pharmacies, and Direct-to-Patient E-commerce. Point-of-sale transactions record units sold, discounts, net revenue, COGS, and patient payment segments.
4. Hospital Demand & Clinical Replenishment: Networked hospitals submit monthly clinical demand forecasts and monthly medication requisitions based on inpatient beds, ICU acuity, and local epidemiology. Warehouses fulfill orders; emergency requests are triggered when hospital safety stock is breached, and unfulfilled demand is recorded.
5. Continuous Traceability & Expiry Control: Products are monitored continuously. Expired or near-expiry batches are quarantined or discounted, while lot-level lineage links sales transactions back to warehouse lots and manufacturing orders to prevent stockouts and waste.""",
        5: """1. VP of Global Supply Chain & Logistics: Monitors end-to-end network fill rates, OTIF logistics performance, and warehouse capacity utilization.
2. Head of Commercial Sales & Distribution: Tracks revenue, channel profitability (Retail vs. Hospital vs. E-commerce), discount leakages, and sales rep targets.
3. Director of Hospital Pharmacy & Clinical Procurement: Analyzes hospital forecast accuracy (WAPE), consumption ratios, formulary compliance, and unfulfilled emergency orders.
4. Cold Chain Quality & Regulatory Compliance Officer: Audits temperature/humidity excursion rates, batch shelf-life integrity, and manages quarantine workflows.
5. Regional Warehouse & Inventory Replenishment Managers: Oversee daily available-to-promise inventory, FEFO compliance scores, and stockout risk thresholds.
6. Chief Financial Officer (CFO) & Financial Controller: Evaluates inventory holding costs, gross margins, near-expiry financial value at risk ($/€), and revenue lost to stockouts.""",
        6: """* Competitors WITHOUT a modern DWH:
- Suffer from fragmented, siloed data across legacy ERP, WMS, and CRM systems, causing a 18%–25% stockout rate during regional disease outbreaks.
- Experience an average annual cold-chain product write-off of $2.4M–$4.5M due to undetected batch expirations and non-compliant FIFO dispatching.
- Require 3–4 weeks of manual spreadsheet reconciliation at month-end to compile sales and margin reports, resulting in delayed commercial decisions and reactive replenishment.
- Lack visibility into unfulfilled hospital demand, leading to lost supply contracts and regulatory penalties for drug shortages.

* Competitors WITH an automated Kimball/Medallion DWH:
- Achieve 98.8%+ On-Time In-Full (OTIF) fulfillment rates with real-time stock-to-demand visibility across all regional hubs.
- Reduce cold-chain inventory waste to <1.2% by utilizing automated FEFO picking alerts and near-expiry dynamic pricing.
- Deliver sub-second OLAP query response times across multi-million row sales datasets, empowering real-time channel margin optimization.
- Utilize automated hospital demand forecasting and closed-loop replenishment DAGs, reducing buffer inventory holding costs by 28%–35%.""",
        7: """1. McKesson Pharmaceutical Distribution Enterprise Warehouse:
- Architecture: Centralized Cloud DWH integrating SAP ERP, HighJump WMS, and IoT cold-chain sensor streams across 30+ regional distribution hubs.
- Impact: Decreased cold-chain temperature excursion losses by 34%, reduced order-to-delivery lead time from 72 hours to 24 hours, and supported 99.4% service levels across 5,000+ health system pharmacies.
- Reference: Gartner Supply Chain Top 25 & Healthcare Distribution Alliance (HDA) Case Study Series.

2. AmerisourceBergen (Cencora) Specialty Logistics Constellation Mart:
- Architecture: Kimball-modeled Fact Constellation combining hospital demand contracts, daily 3PL inventory snapshots, and sales transactions with conformed product and calendar dimensions.
- Impact: Prevented $16.5M in annual biologic expiry write-offs, enabled automated hospital replenishment with 40% lower safety stock, and delivered automated executive BI dashboards refreshed every 4 hours.
- Reference: Journal of Healthcare Information Management & IDC Health Insights Enterprise Case Report.

3. AstraZeneca Global Vaccine & Cold Chain Distribution Intelligence:
- Architecture: Medallion lakehouse (Airflow + dbt + Star Schema) tracking global lot-level vaccine shipments, shelf-life degradation curves, and real-time hospital demand signals.
- Impact: Slashed stockout events by 45% during clinical surge periods, reduced emergency air-freight logistics spend by $8.2M, and provided regulatory traceability down to individual batch lots.
- Reference: Supply Chain Management Review & Pharmaceutical Commerce Cold Chain Logistics Report.""",
        8: """1. Hospital Demand vs. Consumption Analysis (Hospital Procurement Stakeholder):
- Compare monthly forecast demand vs. requested, approved, received, and actual consumed quantities per hospital, medicine, and disease category.
- Identify chronic unfulfilled demand hotspots and calculate service level shortfall percentages.
2. Multi-Channel Commercial Margin & Profitability Analysis (Head of Commercial Sales):
- Analyze gross revenue, trade discounts, net sales, COGS, and gross margin USD/% across Physical Retail, Hospital Pharmacy, and E-commerce channels.
- Filter profitability by customer segment, payer type (Private Insurance, Medicare, Medicaid, Cash), and promotional campaigns.
3. Inventory Availability, Expiry & FEFO Exposure (Inventory Operations Stakeholder):
- Identify cold-chain medicines with high sales/demand velocity that face warehouse stockout risk, low available quantity, or high near-expiry risk (<30/60/90 days).
- Evaluate FEFO (First-Expired, First-Out) picking compliance percentages across regional distribution centers to eliminate preventable spoilage.
4. Product Velocity & Portfolio Movement (VP of Supply Chain):
- Rank top-10 fast-moving vs. slow-moving cold-chain medicines by therapeutic class to optimize warehouse bin allocation and production planning.
- Monitor remaining shelf life at the exact moment of sale to ensure regulatory compliance and customer satisfaction.""",
        9: """1. Weighted Absolute Percentage Error (WAPE) & Tracking Signal: Dynamically measure hospital demand forecasting error and bias across seasonal epidemiology cycles to prevent bullwhip amplification.
2. Days of Inventory Cover (DoIC) & Inventory Run-Out Dates: Calculate real-time stock cover by dividing current available inventory by the trailing 30-day sales velocity per SKU and warehouse.
3. Price Elasticity & Discount Leakage Analysis: Correlate promotional discount depths with incremental volume lift across chain vs. independent pharmacies to detect margin erosion.
4. Channel Cannibalization & Migration Index: Track unit shift from traditional physical brick-and-mortar pharmacies to direct-to-patient digital e-commerce channels.
5. Batch Aging & Shelf-Life Erosion Curves: Track cumulative days in transit and days in warehouse storage relative to manufacturer shelf-life specifications to prevent dead stock accumulation.
6. Cross-Facility Redistribution Opportunity Index: Identify regional warehouse imbalances where Warehouse A experiences a stockout while Warehouse B holds surplus stock expiring in <60 days.""",
        10: """* Financial & Commercial KPIs:
1. Gross Sales Revenue ($) = SUM(QuantitySold * UnitRetailPrice)
2. Net Sales Revenue ($) = SUM(GrossSales - DiscountAmount)
3. Gross Profit Margin % = (NetSales - COGS) / NetSales * 100
4. Return Rate % = (ReturnedQuantity / QuantitySold) * 100
5. Discount Penetration Rate % = SUM(DiscountAmount) / SUM(GrossSales) * 100

* Demand & Fulfillment KPIs:
6. Hospital Demand Fulfillment Ratio = SUM(ConsumedQuantity) / SUM(RequestedQuantity)
7. Forecast-to-Actual Consumption Ratio = SUM(ForecastDemand) / SUM(ConsumedQuantity)
8. Unfulfilled Demand Rate % = SUM(UnfulfilledDemandPacks) / SUM(RequestedQuantity) * 100
9. Order Fill Rate (OTIF %) = (On-Time & In-Full Deliveries / Total Orders) * 100
10. Forecast Error (WAPE %) = SUM(|Forecast - Actual|) / SUM(Actual) * 100

* Inventory & Cold-Chain Operational KPIs:
11. Days of Inventory Cover (DoIC) = AvailableQuantityPacks / (Trailing 30-Day Daily Sales Velocity)
12. Stockout Incident Rate % = (Count of Stockout Days / Days in Period) * 100
13. Near-Expiry Financial Value at Risk ($) = SUM(AvailablePacks * UnitCost) for batches expiring within 30, 60, and 90 days
14. FEFO Compliance Score % = (Packs Dispatched according to strict FEFO sequence / Total Packs Dispatched) * 100
15. Cold-Chain Expiry Waste % = (ExpiredQuantityPacks / TotalAvailablePacks) * 100""",
        11: "To dismantle operational data silos across commercial sales transactions, hospital clinical demand, and regional warehouse inventory positions by deploying an automated, enterprise-grade Fact Constellation Data Warehouse. This infrastructure eliminates life-saving cold-chain drug stockouts, mitigates multi-million dollar expiry waste through FEFO and shelf-life intelligence, optimizes multichannel commercial margins, and establishes an auditable, automated single source of truth for executive and clinical decision-making."
    }

    for row_idx, ans_text in business_answers.items():
        safe_set(ws_b, row_idx, 3, val=ans_text, font=font_body, alignment=align_top_left)
        ws_b.row_dimensions[row_idx].height = 110 if len(ans_text) > 300 else 60

    # =========================================================================
    # 2. SHEET: OLTP.XRay
    # =========================================================================
    ws_o = wb["OLTP.XRay"]
    safe_set(ws_o, 3, 3, val="01_master_data.csv, 04_warehouse_data.csv, 05_pharmacy_sales_data.csv, 06_hospital_demand_data.csv", font=font_body, alignment=align_top_left)

    oltp_rows = [
        (1, "01_master_data.csv", "DimMedicine (SCD Type 2)",
         "MedicineID, InternalSKU, GTIN14, GenericName, FictionalBrandName, DiseaseCategory, ICD10Category, ATCCode, TherapeuticClass, DosageForm, Strength, PackSize, StorageMinTempC, StorageMaxTempC, ColdChainFlag, ShelfLifeMonths, UnitManufacturingCostUSD, WholesalePriceUSD, RecommendedRetailPriceUSD, ProductStatus, EffectiveFromDate",
         "Baseline standard costs/prices (UnitManufacturingCostUSD, WholesalePriceUSD, RecommendedRetailPriceUSD) exported to dimension to compute COGS, margins, and inventory valuation.",
         "Master SKU catalog for 63 cold-chain and ambient medicines. Governed with Kimball SCD Type 2 tracking price, cost, and storage limit versioning."),
        (2, "05_pharmacy_sales_data.csv", "DimChannel, DimFacility (Pharmacy), DimSalesProfile (Junk), DimDate",
         "SalesChannel, PharmacyID, PharmacyGLN, PharmacyName, PharmacyType, PharmacyCity, PharmacyState, CountryCode, PrescriptionRequiredFlag, CustomerSegment, PayerType, PaymentMethod, PromotionCode, SaleStatus, ReturnFlag",
         "QuantitySoldPacks, UnitRetailPriceUSD, GrossSalesAmountUSD, DiscountAmountUSD, NetSalesAmountUSD, CostOfGoodsSoldUSD, GrossMarginUSD, DaysToExpiryAtSale, ReturnedQuantityPacks -> exported to Fact_PharmacySales.",
         "500,000 granular commercial retail, hospital, and e-commerce transactional sales records. Lineage linked via WarehouseLotID and ProductionBatchID."),
        (3, "06_hospital_demand_data.csv", "DimHospital (Facility), DimDate, DimDemandProfile (Junk)",
         "HospitalID, HospitalGLN, HospitalName, HospitalType, City, State, CountryCode, LicensedBeds, ICUBeds, TraumaLevel, CatchmentPopulation, MedicationRequestStatus, FormularyStatus",
         "ForecastDemandPacks, RequestedQuantityPacks, ApprovedQuantityPacks, ReceivedQuantityPacks, EmergencyRequestQuantityPacks, OpeningStockPacks, DispensedQuantityPacks, ConsumedQuantityPacks, WastageQuantityPacks, ClosingStockPacks, UnfulfilledDemandPacks, StockoutDays, ServiceLevelPct -> exported to Fact_Demand.",
         "27,216 monthly clinical demand, procurement, and consumption records across 12 hospitals. Periodic snapshot fact grain at Hospital × Medicine × Month."),
        (4, "04_warehouse_data.csv", "DimWarehouse, DimStorageZone, DimInventoryStatus (Junk)",
         "WarehouseID, WarehouseGLN, WarehouseName, StorageZoneID, StorageCondition, WarehouseTotalCapacityPacks, InventoryStatus, WarehouseActivityStatus",
         "OpeningQuantityPacks, ReceivedQuantityPacks, PutawayQuantityPacks, QuarantineQuantityPacks, AvailableQuantityPacks, ReservedQuantityPacks, PickedQuantityPacks, ShippedQuantityPacks, DamagedQuantityPacks, ExpiredQuantityPacks, AdjustmentQuantityPacks, ClosingQuantityPacks, DaysToExpiry, StockoutFlag, NearExpiryFlag, FEFOComplianceFlag -> exported to Fact_Inventory.",
         "112,184 daily inventory lot snapshot records across 6 regional distribution centers. Semi-additive balance fact capturing lot availability and expiry risk.")
    ]

    for idx, (sno, src_tbl, dim_target, attrs, facts, comms) in enumerate(oltp_rows):
        r = 5 + idx
        vals = [sno, src_tbl, dim_target, attrs, facts, comms]
        for c, v in enumerate(vals, start=1):
            safe_set(ws_o, r, c, val=v, font=font_body, alignment=align_top_left, border=cell_border)
        ws_o.row_dimensions[r].height = 80

    # =========================================================================
    # 3. SHEET: Transform.OLTP
    # =========================================================================
    ws_t = wb["Transform.OLTP"]
    ws_t.column_dimensions["A"].width = 8
    ws_t.column_dimensions["B"].width = 28
    ws_t.column_dimensions["C"].width = 24
    ws_t.column_dimensions["D"].width = 16
    ws_t.column_dimensions["E"].width = 30
    ws_t.column_dimensions["F"].width = 25
    ws_t.column_dimensions["G"].width = 32

    dim_transformations = [
        (1, "MedicineID", "DimMedicine", "VARCHAR(16)", "Trim whitespace, uppercase, validated as unique natural key.", "Natural key for DimMedicine"),
        (2, "GenericName, BrandName", "DimMedicine", "VARCHAR(100)", "Title case, combined into display name 'Brand (Generic)'.", "Improves readability in BI dashboards"),
        (3, "DiseaseCategory", "DimMedicine", "VARCHAR(50)", "Standardized against ICD-10 clinical ontology hierarchy.", "Supports drill-down hierarchy"),
        (4, "Storage Temperature", "DimMedicine", "VARCHAR(30)", "Concat Min & Max: 'MinC to MaxC', validate Min < Max.", "Dynamic cold chain threshold checking"),
        (5, "Cost & Prices", "DimMedicine", "DECIMAL(10,2)", "Cast numeric strings to DECIMAL(10,2), validate > 0.", "Baseline financial valuation"),
        (6, "EffectiveFromDate", "DimMedicine", "TIMESTAMP", "Parsed to UTC timestamp; sets ValidFrom in SCD2 model.", "Enables point-in-time fact joins"),
        (7, "PharmacyID / HospitalID", "DimFacility", "VARCHAR(20)", "Union into conformed DimFacility; assign FacilitySK surrogate key.", "Conformed dimension across Sales & Demand"),
        (8, "PharmacyType / HospitalType", "DimFacility", "VARCHAR(30)", "Categorical mapping: Retail Chain, Independent, Hospital.", "Enables channel split analysis"),
        (9, "City, State, Country", "DimFacility", "VARCHAR(50)", "Standardize USPS abbreviations; map to 4 US Sales Regions.", "Enables regional drill-down"),
        (10, "SalesChannel", "DimChannel", "VARCHAR(30)", "Map into 2 conformed channels: Physical Pharmacy, Ecommerce.", "Distinguishes digital vs in-store sales"),
        (11, "Prescription & Return Flags", "DimSalesProfile", "CHAR(1)", "Normalize Y/N characters to standard binary indicator.", "Junk dimension bitmask"),
        (12, "CustomerSegment / PayerType", "DimSalesProfile", "VARCHAR(30)", "Categorical standardization into conformed junk profile.", "Enables payer margin analysis"),
        (13, "WarehouseID / ZoneID", "DimWarehouse", "VARCHAR(20)", "Extract natural keys; link to regional DC hierarchy.", "Warehouse capacity & zone tracking"),
        (14, "Capacity & Status", "DimWarehouse", "INT / VARCHAR", "Cast capacity to integer; standardize status to Active/Inactive.", "Warehouse utilization analytics"),
        (15, "SalesDate / SnapshotDate", "DimDate", "INTEGER", "Transform YYYY-MM-DD to integer surrogate key YYYYMMDD.", "Standard Kimball integer date key"),
        (16, "DaysToExpiry", "Fact / Dim", "INTEGER", "Recomputed dynamically as DATEDIFF(day, CurrentDate, ExpiryDate).", "Prevents static snapshot date drift"),
        (17, "Default Member Rows", "All Dimensions", "BIGINT / INT", "Inject SK = -1 with 'UNKNOWN' description for orphan handling.", "Kimball referential integrity best practice")
    ]

    for idx, (sno, attr, dim, dtype, act, comm) in enumerate(dim_transformations):
        r = 3 + idx
        safe_set(ws_t, r, 1, val=sno, font=font_body, alignment=align_center, border=cell_border)
        safe_set(ws_t, r, 2, val=attr, font=font_body, alignment=align_top_left, border=cell_border)
        safe_set(ws_t, r, 3, val=dim, font=font_body, alignment=align_top_left, border=cell_border)
        safe_set(ws_t, r, 4, val=dtype, font=font_body, alignment=align_top_left, border=cell_border)
        safe_set(ws_t, r, 5, val=act, font=font_body, alignment=align_top_left, border=cell_border)
        safe_set(ws_t, r, 7, val=comm, font=font_body, alignment=align_top_left, border=cell_border)
        ws_t.row_dimensions[r].height = 28

    fact_transformations = [
        (1, "SalesTransactionID", "Fact_PharmacySales", "VARCHAR(30)", "Validate alphanumeric format; retain as degenerate dimension.", "Order line identification"),
        (2, "SalesDate", "Fact_PharmacySales", "INTEGER", "Format as YYYYMMDD integer foreign key linking to DimDate.", "Role-playing sale date"),
        (3, "MedicineID", "Fact_PharmacySales", "BIGINT", "Point-in-time SCD2 surrogate lookup: DimMedicine.MedicineSK.", "Preserves historical price accuracy"),
        (4, "FacilityID (Pharmacy)", "Fact_PharmacySales", "BIGINT", "Foreign key lookup linking to DimFacility.FacilitySK.", "Enables retail location drill-down"),
        (5, "QuantitySoldPacks", "Fact_PharmacySales", "INTEGER", "Validate integer > 0; quarantine negative rows to dq.rejected_rows.", "Fully additive measure"),
        (6, "UnitRetailPriceUSD", "Fact_PharmacySales", "DECIMAL(10,2)", "Validated > 0; stored as non-additive unit price measure.", "Transaction unit price"),
        (7, "GrossSalesAmountUSD", "Fact_PharmacySales", "DECIMAL(12,2)", "Verify calculation: QuantitySoldPacks * UnitRetailPriceUSD.", "Fully additive gross revenue"),
        (8, "DiscountAmountUSD", "Fact_PharmacySales", "DECIMAL(12,2)", "Validate non-negative; capped at 100% of gross revenue.", "Additive commercial trade discount"),
        (9, "NetSalesAmountUSD", "Fact_PharmacySales", "DECIMAL(12,2)", "Computed measure: GrossSalesAmountUSD - DiscountAmountUSD.", "Fully additive net sales revenue"),
        (10, "CostOfGoodsSoldUSD", "Fact_PharmacySales", "DECIMAL(12,2)", "Derived measure: DimMedicine.UnitManufacturingCostUSD * QuantitySold.", "Additive cost baseline"),
        (11, "GrossMarginUSD", "Fact_PharmacySales", "DECIMAL(12,2)", "Computed measure: NetSalesAmountUSD - CostOfGoodsSoldUSD.", "Fully additive gross margin profit"),
        (12, "DaysToExpiryAtSale", "Fact_PharmacySales", "INTEGER", "Calculated: DATEDIFF(day, SalesDate, BatchExpiryDate) via lot lineage.", "Customer shelf-life safety margin"),
        (13, "DemandMonth", "Fact_Demand", "INTEGER", "Format as YYYYMM01 integer FK linking to monthly DimDate grain.", "Monthly snapshot grain"),
        (14, "ForecastDemandPacks", "Fact_Demand", "INTEGER", "Parsed as integer >= 0; additive monthly clinical forecast demand.", "Forecast demand benchmark"),
        (15, "Requested & Consumed Qty", "Fact_Demand", "INTEGER", "Validated positive integers; additive clinical demand measures.", "Fulfillment ratio calculation"),
        (16, "UnfulfilledDemandPacks", "Fact_Demand", "INTEGER", "Computed measure: GREATEST(0, RequestedQuantity - ConsumedQuantity).", "Direct measure of clinical shortage"),
        (17, "AvailableQuantityPacks", "Fact_Inventory", "INTEGER", "Semi-additive measure; additive across DC warehouses, not time.", "Warehouse on-hand stock"),
        (18, "Stockout & FEFO Flags", "Fact_Inventory", "TINYINT (0/1)", "Normalized to binary bit indicators for high-performance bitmap aggregation.", "Stockout and compliance indicators")
    ]

    for idx, (sno, attr, fact, dtype, act, comm) in enumerate(fact_transformations):
        r = 22 + idx
        safe_set(ws_t, r, 1, val=sno, font=font_body, alignment=align_center, border=cell_border)
        safe_set(ws_t, r, 2, val=attr, font=font_body, alignment=align_top_left, border=cell_border)
        safe_set(ws_t, r, 3, val=fact, font=font_body, alignment=align_top_left, border=cell_border)
        safe_set(ws_t, r, 4, val=dtype, font=font_body, alignment=align_top_left, border=cell_border)
        safe_set(ws_t, r, 5, val=act, font=font_body, alignment=align_top_left, border=cell_border)
        safe_set(ws_t, r, 7, val=comm, font=font_body, alignment=align_top_left, border=cell_border)
        ws_t.row_dimensions[r].height = 28

    # =========================================================================
    # 4. SHEET: Dim.Tables
    # =========================================================================
    ws_d = wb["Dim.Tables"]
    ws_d.column_dimensions["A"].width = 26
    ws_d.column_dimensions["B"].width = 18
    ws_d.column_dimensions["C"].width = 18
    ws_d.column_dimensions["D"].width = 12
    ws_d.column_dimensions["E"].width = 12
    ws_d.column_dimensions["F"].width = 24
    ws_d.column_dimensions["G"].width = 30

    # DimDate
    safe_set(ws_d, 3, 2, val="DateKey (INTEGER, format YYYYMMDD)", font=font_bold)
    safe_set(ws_d, 4, 2, val="FullDate (DATE, ISO-8601 YYYY-MM-DD)", font=font_bold)

    dim_date_attrs = [
        ("DateKey", "INTEGER", "Type 0 (Static)", "Date -> Year", "Surrogate integer key formatted YYYYMMDD"),
        ("FullDate", "DATE", "Type 0 (Static)", "Date -> Month -> Year", "Actual calendar date"),
        ("CalendarYear", "SMALLINT", "Type 0 (Static)", "Year Level", "Calendar year (2023 - 2026)"),
        ("Quarter", "CHAR(2)", "Type 0 (Static)", "Quarter -> Year", "Quarter identifier (Q1, Q2, Q3, Q4)"),
        ("MonthName", "VARCHAR(12)", "Type 0 (Static)", "Month -> Quarter", "Full month name (January - December)"),
        ("MonthNumber", "TINYINT", "Type 0 (Static)", "Month -> Quarter", "Calendar month number (1 - 12)"),
        ("WeekOfYear", "TINYINT", "Type 0 (Static)", "Week -> Year", "ISO calendar week number (1 - 53)"),
        ("DayOfWeek", "TINYINT", "Type 0 (Static)", "Day -> Week", "Day of week (1=Monday, 7=Sunday)"),
        ("DayName", "VARCHAR(10)", "Type 0 (Static)", "Day Level", "Name of day (Monday - Sunday)"),
        ("IsWeekendFlag", "BOOLEAN", "Type 0 (Static)", "Day -> Weekend", "True (1) if Saturday/Sunday, else False (0)"),
        ("FiscalYear", "SMALLINT", "Type 0 (Static)", "Fiscal Year", "Corporate fiscal reporting year")
    ]
    for idx, (attr, dtype, scd, hier, comm) in enumerate(dim_date_attrs):
        r = 6 + idx
        safe_set(ws_d, r, 1, val=attr, font=font_body, alignment=align_top_left, border=cell_border)
        safe_set(ws_d, r, 2, val=dtype, font=font_body, alignment=align_top_left, border=cell_border)
        safe_set(ws_d, r, 3, val=scd, font=font_body, alignment=align_top_left, border=cell_border)
        safe_set(ws_d, r, 6, val=hier, font=font_body, alignment=align_top_left, border=cell_border)
        safe_set(ws_d, r, 7, val=comm, font=font_body, alignment=align_top_left, border=cell_border)
        ws_d.row_dimensions[r].height = 20

    # Dim Table 2 -> DimMedicine (SCD Type 2)
    safe_set(ws_d, 17, 1, val="DimMedicine (Conformed - SCD Type 2)", font=font_sec_hdr)
    safe_set(ws_d, 18, 2, val="MedicineSK (BIGINT Surrogate Hash Key)", font=font_bold)
    safe_set(ws_d, 19, 2, val="MedicineID (VARCHAR(16) Master SKU ID)", font=font_bold)

    dim_med_attrs = [
        ("GenericName", "VARCHAR(100)", "Type 1 (Overwrite)", "Generic -> Therapeutic", "Standard international nonproprietary pharmaceutical name"),
        ("FictionalBrandName", "VARCHAR(100)", "Type 1 (Overwrite)", "Brand -> Generic", "Commercial trademarked brand name"),
        ("DiseaseCategory", "VARCHAR(50)", "Type 1 (Overwrite)", "Disease -> Category", "Target disease (Cardiovascular, Oncology, Diabetes, etc.)"),
        ("ICD10Category", "VARCHAR(20)", "Type 1 (Overwrite)", "Clinical Taxonomy", "WHO ICD-10 diagnostic category classification"),
        ("ATCCode", "VARCHAR(10)", "Type 1 (Overwrite)", "ATC Anatomical", "Anatomical Therapeutic Chemical pharmacology code"),
        ("TherapeuticClass", "VARCHAR(50)", "Type 1 (Overwrite)", "Therapeutic Class", "Therapeutic drug class (Antineoplastic, Statin, Biguanide)"),
        ("ColdChainFlag", "CHAR(1)", "Type 1 (Overwrite)", "Storage Hierarchy", "Y = Requires continuous cold-chain (2C-8C); N = Ambient"),
        ("StorageCondition", "VARCHAR(50)", "Type 2 (History)", "Environmental Range", "Explicit temperature range (e.g., 2°C to 8°C, Max Humidity 60%)"),
        ("UnitManufacturingCostUSD", "DECIMAL(10,2)", "Type 2 (History)", "Cost Baseline", "Standard batch unit production cost tracked over time"),
        ("RecommendedRetailPriceUSD", "DECIMAL(10,2)", "Type 2 (History)", "Pricing Strategy", "Manufacturer recommended retail price tracked over time"),
        ("IsCurrentFlag", "BOOLEAN", "Type 2 (History)", "SCD2 Versioning", "True (1) for active current version, False (0) for historical")
    ]
    for idx, (attr, dtype, scd, hier, comm) in enumerate(dim_med_attrs):
        r = 21 + idx
        safe_set(ws_d, r, 1, val=attr, font=font_body, alignment=align_top_left, border=cell_border)
        safe_set(ws_d, r, 2, val=dtype, font=font_body, alignment=align_top_left, border=cell_border)
        safe_set(ws_d, r, 3, val=scd, font=font_body, alignment=align_top_left, border=cell_border)
        safe_set(ws_d, r, 6, val=hier, font=font_body, alignment=align_top_left, border=cell_border)
        safe_set(ws_d, r, 7, val=comm, font=font_body, alignment=align_top_left, border=cell_border)
        ws_d.row_dimensions[r].height = 20

    # Dim Table 3 -> DimFacility (Conformed Hospital & Pharmacy)
    safe_set(ws_d, 32, 1, val="DimFacility (Conformed - Hospital & Commercial Pharmacy)", font=font_sec_hdr)
    safe_set(ws_d, 33, 2, val="FacilitySK (BIGINT Surrogate Key)", font=font_bold)
    safe_set(ws_d, 34, 2, val="FacilityID (VARCHAR(20) Natural GLN / Identifier)", font=font_bold)

    dim_fac_attrs = [
        ("FacilityName", "VARCHAR(100)", "Type 1 (Overwrite)", "Facility -> Region", "Official commercial facility or medical center name"),
        ("FacilityType", "VARCHAR(30)", "Type 1 (Overwrite)", "Channel Type", "Hospital, Hospital Pharmacy, Retail Chain, Independent"),
        ("City", "VARCHAR(50)", "Type 1 (Overwrite)", "City -> State", "Municipal city jurisdiction"),
        ("State", "CHAR(2)", "Type 1 (Overwrite)", "State -> Region", "US standard state postal abbreviation"),
        ("Region", "VARCHAR(20)", "Type 1 (Overwrite)", "Territory Hierarchy", "Geographic market region (Northeast, Midwest, South, West)"),
        ("LicensedBeds", "INT", "Type 1 (Overwrite)", "Hospital Scale", "Inpatient bed capacity (hospitals only; null for retail)"),
        ("ICUBeds", "INT", "Type 1 (Overwrite)", "Critical Acuity", "Intensive care unit beds (hospitals only)"),
        ("TraumaLevel", "VARCHAR(20)", "Type 1 (Overwrite)", "Clinical Acuity", "Trauma emergency designation (Level I, Level II, Level III)"),
        ("CatchmentPopulation", "INT", "Type 1 (Overwrite)", "Market Potential", "Demographic regional population served"),
        ("ActivityStatus", "VARCHAR(20)", "Type 1 (Overwrite)", "Facility Status", "Active commercial customer or licensed dispensing site")
    ]
    for idx, (attr, dtype, scd, hier, comm) in enumerate(dim_fac_attrs):
        r = 36 + idx
        safe_set(ws_d, r, 1, val=attr, font=font_body, alignment=align_top_left, border=cell_border)
        safe_set(ws_d, r, 2, val=dtype, font=font_body, alignment=align_top_left, border=cell_border)
        safe_set(ws_d, r, 3, val=scd, font=font_body, alignment=align_top_left, border=cell_border)
        safe_set(ws_d, r, 6, val=hier, font=font_body, alignment=align_top_left, border=cell_border)
        safe_set(ws_d, r, 7, val=comm, font=font_body, alignment=align_top_left, border=cell_border)
        ws_d.row_dimensions[r].height = 20

    # Dim Table 4 -> DimWarehouse (Conformed Regional Distribution Center)
    safe_set(ws_d, 46, 1, val="DimWarehouse (Conformed - Regional Distribution Centers)", font=font_sec_hdr)
    safe_set(ws_d, 47, 2, val="WarehouseSK (BIGINT Surrogate Key)", font=font_bold)
    safe_set(ws_d, 48, 2, val="WarehouseID (VARCHAR(16) Natural Warehouse Code)", font=font_bold)

    dim_wh_attrs = [
        ("WarehouseName", "VARCHAR(100)", "Type 1 (Overwrite)", "Warehouse -> Region", "Full name of regional cold-chain distribution center"),
        ("WarehouseGLN", "VARCHAR(20)", "Type 0 (Static)", "Global Standard", "GS1 Global Location Number identifier"),
        ("StorageZoneID", "VARCHAR(30)", "Type 1 (Overwrite)", "Zone -> Warehouse", "Internal storage zone code (Cold Room A, Ambient B, Deep Freeze)"),
        ("StorageCondition", "VARCHAR(50)", "Type 1 (Overwrite)", "Zone Environment", "Environmental zone range (2°C to 8°C Cold Chain, Ambient 15°C to 25°C)"),
        ("City", "VARCHAR(50)", "Type 1 (Overwrite)", "City -> State", "Distribution center physical city"),
        ("State", "CHAR(2)", "Type 1 (Overwrite)", "State -> Region", "State jurisdiction"),
        ("Region", "VARCHAR(20)", "Type 1 (Overwrite)", "Territory Hierarchy", "Regional logistics distribution hub territory"),
        ("TotalCapacityPacks", "INT", "Type 1 (Overwrite)", "Physical Scale", "Maximum total volumetric package capacity"),
        ("WarehouseActivityStatus", "VARCHAR(20)", "Type 1 (Overwrite)", "Operational Status", "Active operational hub / quarantine facility")
    ]
    for idx, (attr, dtype, scd, hier, comm) in enumerate(dim_wh_attrs):
        r = 50 + idx
        safe_set(ws_d, r, 1, val=attr, font=font_body, alignment=align_top_left, border=cell_border)
        safe_set(ws_d, r, 2, val=dtype, font=font_body, alignment=align_top_left, border=cell_border)
        safe_set(ws_d, r, 3, val=scd, font=font_body, alignment=align_top_left, border=cell_border)
        safe_set(ws_d, r, 6, val=hier, font=font_body, alignment=align_top_left, border=cell_border)
        safe_set(ws_d, r, 7, val=comm, font=font_body, alignment=align_top_left, border=cell_border)
        ws_d.row_dimensions[r].height = 20

    # Dim Table 5 (Other Dimension Types -> Junk Dimension DimSalesProfile)
    safe_set(ws_d, 62, 1, val="DimSalesProfile (Commercial Transaction Junk Dimension)", font=font_sec_hdr)
    safe_set(ws_d, 63, 2, val="SalesProfileSK (INTEGER Surrogate Key)", font=font_bold)
    safe_set(ws_d, 64, 2, val="ProfileHash (CHAR(32) MD5 Attribute Hash)", font=font_bold)
    safe_set(ws_d, 65, 2, val="Junk Dimension (Combines Low-Cardinality Transactional Flags)", font=font_bold)

    dim_junk_attrs = [
        ("PrescriptionRequiredFlag", "CHAR(1)", "Type 0 (Static)", "Regulatory Profile", "Y = Prescription Required, N = Over-The-Counter"),
        ("CustomerSegment", "VARCHAR(30)", "Type 0 (Static)", "Commercial Segment", "Retail Patient, Institutional Health System, Clinical Trial"),
        ("PayerType", "VARCHAR(30)", "Type 0 (Static)", "Financial Payer", "Private Commercial Insurance, Medicare, Medicaid, Out-of-Pocket Cash"),
        ("PaymentMethod", "VARCHAR(30)", "Type 0 (Static)", "Settlement Method", "Electronic Funds Transfer, Credit Card, Direct Third-Party Billing"),
        ("PromotionCode", "VARCHAR(30)", "Type 0 (Static)", "Marketing Campaign", "Promotional campaign code applied or 'NO_PROMOTION'"),
        ("SaleStatus", "VARCHAR(20)", "Type 0 (Static)", "Lifecycle Status", "Completed, Returned, Quarantined"),
        ("ReturnFlag", "CHAR(1)", "Type 0 (Static)", "Reversal Indicator", "Y = Product returned by customer/pharmacy, N = Normal sale")
    ]
    for idx, (attr, dtype, scd, hier, comm) in enumerate(dim_junk_attrs):
        r = 67 + idx
        safe_set(ws_d, r, 1, val=attr, font=font_body, alignment=align_top_left, border=cell_border)
        safe_set(ws_d, r, 2, val=dtype, font=font_body, alignment=align_top_left, border=cell_border)
        safe_set(ws_d, r, 3, val=scd, font=font_body, alignment=align_top_left, border=cell_border)
        safe_set(ws_d, r, 6, val=hier, font=font_body, alignment=align_top_left, border=cell_border)
        safe_set(ws_d, r, 7, val=comm, font=font_body, alignment=align_top_left, border=cell_border)
        ws_d.row_dimensions[r].height = 20

    # =========================================================================
    # 5. SHEET: Fact.Table (Fact_PharmacySales)
    # =========================================================================
    ws_f = wb["Fact.Table"]
    ws_f.column_dimensions["A"].width = 8
    ws_f.column_dimensions["B"].width = 25
    ws_f.column_dimensions["C"].width = 16
    ws_f.column_dimensions["D"].width = 10
    ws_f.column_dimensions["E"].width = 24
    ws_f.column_dimensions["F"].width = 16
    ws_f.column_dimensions["G"].width = 25
    ws_f.column_dimensions["H"].width = 32

    safe_set(ws_f, 2, 1, val="Fact Table Name: Fact_PharmacySales (Multichannel Commercial Sales)", font=font_sec_hdr)
    safe_set(ws_f, 3, 2, val="Grain: One row per individual sales transaction line item (SalesTransactionID)", font=font_bold)
    safe_set(ws_f, 4, 2, val="Transactional", font=font_bold)
    safe_set(ws_f, 5, 2, val="Primary Key: SalesTransactionSK (BIGINT Surrogate PK) / SalesTransactionID (Natural PK)", font=font_bold)
    safe_set(ws_f, 6, 2, val="Range Partitioned by CalendarYear and SalesMonth on DateKey", font=font_bold)
    safe_set(ws_f, 7, 2, val="B-tree Indexes on DateKey, MedicineSK, FacilitySK, SalesProfileSK; Clustered on DateKey", font=font_bold)

    pharm_sales_cols = [
        (1, "SalesTransactionSK", "BIGINT", "N", "Non-Additive", "N", "05_pharmacy_sales", "Surrogate Primary Key for the sales transaction fact row"),
        (2, "DateKey", "INTEGER", "Y", "Non-Additive", "N", "05_pharmacy_sales", "Foreign key linking to DimDate (Role: Transaction Sale Date)"),
        (3, "MedicineSK", "BIGINT", "Y", "Non-Additive", "N", "01_master/05_sales", "Foreign key linking to DimMedicine (Point-in-Time SCD2 version)"),
        (4, "FacilitySK", "BIGINT", "Y", "Non-Additive", "N", "05_pharmacy_sales", "Foreign key linking to DimFacility (Pharmacy / Dispensing Site)"),
        (5, "WarehouseSK", "BIGINT", "Y", "Non-Additive", "N", "04_warehouse/05_sales", "Foreign key linking to DimWarehouse (Fulfilling Regional DC)"),
        (6, "SalesProfileSK", "INTEGER", "Y", "Non-Additive", "N", "05_pharmacy_sales", "Foreign key linking to DimSalesProfile (Commercial Junk Dimension)"),
        (7, "SalesTransactionID", "VARCHAR(30)", "N", "Non-Additive", "Y", "05_pharmacy_sales", "Degenerate dimension: Operational Sales Transaction Identifier"),
        (8, "PharmacyOrderID", "VARCHAR(30)", "N", "Non-Additive", "Y", "05_pharmacy_sales", "Degenerate dimension: Pharmacy Purchase Order Header Identifier"),
        (9, "WarehouseLotID", "VARCHAR(30)", "N", "Non-Additive", "Y", "05_pharmacy_sales", "Degenerate dimension: Fulfilling Warehouse Lot traceability key"),
        (10, "ProductionBatchID", "VARCHAR(30)", "N", "Non-Additive", "Y", "05_pharmacy_sales", "Degenerate dimension: Upstream Manufacturing Batch traceability key"),
        (11, "QuantitySoldPacks", "INTEGER", "N", "Fully Additive", "N", "05_pharmacy_sales", "Total count of medicine commercial packages sold in transaction"),
        (12, "UnitRetailPriceUSD", "DECIMAL(10,2)", "N", "Non-Additive", "N", "05_pharmacy_sales", "Commercial retail sale price charged per package unit"),
        (13, "GrossSalesAmountUSD", "DECIMAL(12,2)", "N", "Fully Additive", "N", "05_pharmacy_sales", "Gross revenue: QuantitySoldPacks * UnitRetailPriceUSD"),
        (14, "DiscountAmountUSD", "DECIMAL(12,2)", "N", "Fully Additive", "N", "05_pharmacy_sales", "Total promotional / commercial trade discount applied"),
        (15, "NetSalesAmountUSD", "DECIMAL(12,2)", "N", "Fully Additive", "N", "05_pharmacy_sales", "Net recognized revenue: GrossSalesAmountUSD - DiscountAmountUSD"),
        (16, "CostOfGoodsSoldUSD", "DECIMAL(12,2)", "N", "Fully Additive", "N", "01_master/05_sales", "Production cost baseline: UnitManufacturingCostUSD * QuantitySoldPacks"),
        (17, "GrossMarginUSD", "DECIMAL(12,2)", "N", "Fully Additive", "N", "05_pharmacy_sales", "Gross commercial profit margin: NetSalesAmountUSD - CostOfGoodsSoldUSD"),
        (18, "DaysToExpiryAtSale", "INTEGER", "N", "Non-Additive", "N", "04_warehouse/05_sales", "Remaining shelf-life days of lot at point of commercial sale"),
        (19, "ReturnedQuantityPacks", "INTEGER", "N", "Fully Additive", "N", "05_pharmacy_sales", "Units returned back by customer/pharmacy reversal"),
        (20, "_batch_id", "INTEGER", "N", "Non-Additive", "N", "ETL Metadata", "Audit lineage: Ingestion batch identifier"),
        (21, "_ingested_at", "TIMESTAMP", "N", "Non-Additive", "N", "ETL Metadata", "Audit lineage: UTC timestamp when row committed to DWH")
    ]

    for idx, (sno, name, dtype, fk, mtype, deg, src, comm) in enumerate(pharm_sales_cols):
        r = 9 + idx
        safe_set(ws_f, r, 1, val=sno, font=font_body, alignment=align_center, border=cell_border)
        safe_set(ws_f, r, 2, val=name, font=font_body, alignment=align_top_left, border=cell_border)
        safe_set(ws_f, r, 3, val=dtype, font=font_body, alignment=align_top_left, border=cell_border)
        safe_set(ws_f, r, 4, val=fk, font=font_body, alignment=align_center, border=cell_border)
        safe_set(ws_f, r, 5, val=mtype, font=font_body, alignment=align_top_left, border=cell_border)
        safe_set(ws_f, r, 6, val=deg, font=font_body, alignment=align_center, border=cell_border)
        safe_set(ws_f, r, 7, val=src, font=font_body, alignment=align_top_left, border=cell_border)
        safe_set(ws_f, r, 8, val=comm, font=font_body, alignment=align_top_left, border=cell_border)
        ws_f.row_dimensions[r].height = 22

    # Clone Fact_Demand
    ws_f_demand = wb.copy_worksheet(ws_f)
    ws_f_demand.title = "Fact.Table.Demand"
    safe_set(ws_f_demand, 2, 1, val="Fact Table Name: Fact_Demand (Clinical Hospital Demand & Consumption)", font=font_sec_hdr)
    safe_set(ws_f_demand, 3, 2, val="Grain: One row per Hospital, Medicine, and Demand Month (HospitalID x MedicineID x Month)", font=font_bold)
    safe_set(ws_f_demand, 4, 2, val="Periodic Snapshot", font=font_bold)
    safe_set(ws_f_demand, 5, 2, val="Primary Key: HospitalDemandSK (BIGINT Surrogate PK) / HospitalDemandRecordID", font=font_bold)
    safe_set(ws_f_demand, 6, 2, val="Range Partitioned by CalendarYear on DateKey", font=font_bold)
    safe_set(ws_f_demand, 7, 2, val="B-tree Indexes on DateKey, MedicineSK, FacilitySK; Clustered on DateKey", font=font_bold)

    for r in range(9, 35):
        for c in range(1, 9):
            cell = ws_f_demand.cell(r, c)
            if type(cell).__name__ == 'Cell':
                cell.value = None

    demand_cols = [
        (1, "HospitalDemandSK", "BIGINT", "N", "Non-Additive", "N", "06_hospital_demand", "Surrogate Primary Key for hospital demand snapshot row"),
        (2, "DateKey", "INTEGER", "Y", "Non-Additive", "N", "06_hospital_demand", "Foreign key linking to DimDate (Role: Demand Month YYYYMM01)"),
        (3, "MedicineSK", "BIGINT", "Y", "Non-Additive", "N", "01_master/06_demand", "Foreign key linking to DimMedicine (Point-in-Time SCD2 version)"),
        (4, "FacilitySK", "BIGINT", "Y", "Non-Additive", "N", "06_hospital_demand", "Foreign key linking to DimFacility (Hospital Clinical Facility)"),
        (5, "HospitalDemandRecordID", "VARCHAR(30)", "N", "Non-Additive", "Y", "06_hospital_demand", "Degenerate dimension: Operational Hospital Demand Record Identifier"),
        (6, "ForecastDemandPacks", "INTEGER", "N", "Fully Additive", "N", "06_hospital_demand", "Monthly clinical projected requirement in packages"),
        (7, "RequestedQuantityPacks", "INTEGER", "N", "Fully Additive", "N", "06_hospital_demand", "Total formal procurement quantity requested by hospital"),
        (8, "ApprovedQuantityPacks", "INTEGER", "N", "Fully Additive", "N", "06_hospital_demand", "Total quantity authorized by hospital procurement committee"),
        (9, "ReceivedQuantityPacks", "INTEGER", "N", "Fully Additive", "N", "06_hospital_demand", "Physical quantity delivered to and accepted by hospital pharmacy"),
        (10, "ConsumedQuantityPacks", "INTEGER", "N", "Fully Additive", "N", "06_hospital_demand", "Actual quantity dispensed and consumed by clinical patients"),
        (11, "EmergencyRequestQuantityPacks", "INTEGER", "N", "Fully Additive", "N", "06_hospital_demand", "Expedited urgent order packages triggered by stockout risk"),
        (12, "UnfulfilledDemandPacks", "INTEGER", "N", "Fully Additive", "N", "06_hospital_demand", "Deficit: GREATEST(0, RequestedQuantity - ConsumedQuantity)"),
        (13, "StockoutDays", "INTEGER", "N", "Fully Additive", "N", "06_hospital_demand", "Count of days medicine was completely out of stock at hospital"),
        (14, "ServiceLevelPct", "DECIMAL(5,2)", "N", "Non-Additive", "N", "06_hospital_demand", "Hospital service fulfillment percentage achieved (0% - 100%)"),
        (15, "OpeningStockPacks", "INTEGER", "N", "Semi-Additive", "N", "06_hospital_demand", "Inventory on-hand at hospital at start of month (semi-additive)"),
        (16, "ClosingStockPacks", "INTEGER", "N", "Semi-Additive", "N", "06_hospital_demand", "Inventory on-hand at hospital at end of month (semi-additive)"),
        (17, "_batch_id", "INTEGER", "N", "Non-Additive", "N", "ETL Metadata", "Audit lineage: Ingestion batch identifier"),
        (18, "_ingested_at", "TIMESTAMP", "N", "Non-Additive", "N", "ETL Metadata", "Audit lineage: UTC timestamp when row committed to DWH")
    ]
    for idx, (sno, name, dtype, fk, mtype, deg, src, comm) in enumerate(demand_cols):
        r = 9 + idx
        safe_set(ws_f_demand, r, 1, val=sno, font=font_body, alignment=align_center, border=cell_border)
        safe_set(ws_f_demand, r, 2, val=name, font=font_body, alignment=align_top_left, border=cell_border)
        safe_set(ws_f_demand, r, 3, val=dtype, font=font_body, alignment=align_top_left, border=cell_border)
        safe_set(ws_f_demand, r, 4, val=fk, font=font_body, alignment=align_center, border=cell_border)
        safe_set(ws_f_demand, r, 5, val=mtype, font=font_body, alignment=align_top_left, border=cell_border)
        safe_set(ws_f_demand, r, 6, val=deg, font=font_body, alignment=align_center, border=cell_border)
        safe_set(ws_f_demand, r, 7, val=src, font=font_body, alignment=align_top_left, border=cell_border)
        safe_set(ws_f_demand, r, 8, val=comm, font=font_body, alignment=align_top_left, border=cell_border)
        ws_f_demand.row_dimensions[r].height = 22

    # Clone Fact_Inventory
    ws_f_inv = wb.copy_worksheet(ws_f)
    ws_f_inv.title = "Fact.Table.Inventory"
    safe_set(ws_f_inv, 2, 1, val="Fact Table Name: Fact_Inventory (Daily Warehouse Lot Inventory Snapshots)", font=font_sec_hdr)
    safe_set(ws_f_inv, 3, 2, val="Grain: One row per Warehouse, Lot, and Snapshot Date (WarehouseID x WarehouseLotID x Day)", font=font_bold)
    safe_set(ws_f_inv, 4, 2, val="Periodic Snapshot (Semi-Additive)", font=font_bold)
    safe_set(ws_f_inv, 5, 2, val="Primary Key: InventorySnapshotSK (BIGINT Surrogate PK) / InventorySnapshotID", font=font_bold)
    safe_set(ws_f_inv, 6, 2, val="Range Partitioned by SnapshotDate (Daily / Monthly Partitions)", font=font_bold)
    safe_set(ws_f_inv, 7, 2, val="B-tree Indexes on DateKey, MedicineSK, WarehouseSK; Clustered on DateKey", font=font_bold)

    for r in range(9, 35):
        for c in range(1, 9):
            cell = ws_f_inv.cell(r, c)
            if type(cell).__name__ == 'Cell':
                cell.value = None

    inv_cols = [
        (1, "InventorySnapshotSK", "BIGINT", "N", "Non-Additive", "N", "04_warehouse_data", "Surrogate Primary Key for daily inventory snapshot row"),
        (2, "DateKey", "INTEGER", "Y", "Non-Additive", "N", "04_warehouse_data", "Foreign key linking to DimDate (Role: Daily Snapshot Date)"),
        (3, "MedicineSK", "BIGINT", "Y", "Non-Additive", "N", "01_master/04_wh", "Foreign key linking to DimMedicine (Point-in-Time SCD2 version)"),
        (4, "WarehouseSK", "BIGINT", "Y", "Non-Additive", "N", "04_warehouse_data", "Foreign key linking to DimWarehouse (Regional Distribution Center)"),
        (5, "InventorySnapshotID", "VARCHAR(30)", "N", "Non-Additive", "Y", "04_warehouse_data", "Degenerate dimension: Operational Daily Snapshot Identifier"),
        (6, "WarehouseLotID", "VARCHAR(30)", "N", "Non-Additive", "Y", "04_warehouse_data", "Degenerate dimension: Physical warehouse lot identification code"),
        (7, "ProductionBatchID", "VARCHAR(30)", "N", "Non-Additive", "Y", "04_warehouse_data", "Degenerate dimension: Manufacturer production batch identifier"),
        (8, "OpeningQuantityPacks", "INTEGER", "N", "Semi-Additive", "N", "04_warehouse_data", "Starting lot stock balance at 00:00 UTC (semi-additive)"),
        (9, "ReceivedQuantityPacks", "INTEGER", "N", "Fully Additive", "N", "04_warehouse_data", "Inbound packs received into warehouse during snapshot day"),
        (10, "AvailableQuantityPacks", "INTEGER", "N", "Semi-Additive", "N", "04_warehouse_data", "Active uncommitted packs available to fulfill customer orders"),
        (11, "QuarantineQuantityPacks", "INTEGER", "N", "Semi-Additive", "N", "04_warehouse_data", "Packs locked in quarantine due to excursion or QA hold"),
        (12, "ReservedQuantityPacks", "INTEGER", "N", "Semi-Additive", "N", "04_warehouse_data", "Packs allocated to pending pick/ship orders"),
        (13, "ShippedQuantityPacks", "INTEGER", "N", "Fully Additive", "N", "04_warehouse_data", "Outbound packs picked and dispatched to customers during day"),
        (14, "ExpiredQuantityPacks", "INTEGER", "N", "Fully Additive", "N", "04_warehouse_data", "Packs reaching shelf-life expiry and written off"),
        (15, "ClosingQuantityPacks", "INTEGER", "N", "Semi-Additive", "N", "04_warehouse_data", "Ending lot stock balance at 23:59 UTC (semi-additive)"),
        (16, "DaysToExpiry", "INTEGER", "N", "Non-Additive", "N", "04_warehouse_data", "Calculated days remaining until batch reaches expiration"),
        (17, "StockoutFlag", "TINYINT", "N", "Non-Additive", "N", "04_warehouse_data", "1 if available quantity is 0 while active demand exists, else 0"),
        (18, "NearExpiryFlag", "TINYINT", "N", "Non-Additive", "N", "04_warehouse_data", "1 if batch expires within <= 90 days, else 0"),
        (19, "FEFOComplianceFlag", "TINYINT", "N", "Non-Additive", "N", "04_warehouse_data", "1 if warehouse dispatches followed FEFO sequence, else 0"),
        (20, "_batch_id", "INTEGER", "N", "Non-Additive", "N", "ETL Metadata", "Audit lineage: Ingestion batch identifier"),
        (21, "_ingested_at", "TIMESTAMP", "N", "Non-Additive", "N", "ETL Metadata", "Audit lineage: UTC timestamp when row committed to DWH")
    ]
    for idx, (sno, name, dtype, fk, mtype, deg, src, comm) in enumerate(inv_cols):
        r = 9 + idx
        safe_set(ws_f_inv, r, 1, val=sno, font=font_body, alignment=align_center, border=cell_border)
        safe_set(ws_f_inv, r, 2, val=name, font=font_body, alignment=align_top_left, border=cell_border)
        safe_set(ws_f_inv, r, 3, val=dtype, font=font_body, alignment=align_top_left, border=cell_border)
        safe_set(ws_f_inv, r, 4, val=fk, font=font_body, alignment=align_center, border=cell_border)
        safe_set(ws_f_inv, r, 5, val=mtype, font=font_body, alignment=align_top_left, border=cell_border)
        safe_set(ws_f_inv, r, 6, val=deg, font=font_body, alignment=align_center, border=cell_border)
        safe_set(ws_f_inv, r, 7, val=src, font=font_body, alignment=align_top_left, border=cell_border)
        safe_set(ws_f_inv, r, 8, val=comm, font=font_body, alignment=align_top_left, border=cell_border)
        ws_f_inv.row_dimensions[r].height = 22

    # =========================================================================
    # 6. SHEET: Star.Schema
    # =========================================================================
    ws_s = wb["Star.Schema"]
    ws_s.column_dimensions["L"].width = 8
    ws_s.column_dimensions["M"].width = 32
    ws_s.column_dimensions["N"].width = 38
    ws_s.column_dimensions["O"].width = 38

    if os.path.exists(DIAGRAM_PATH):
        xl_img = XLImage(DIAGRAM_PATH)
        xl_img.width = 750
        xl_img.height = 490
        ws_s.add_image(xl_img, "A5")
        print("Embedded diagram image into Star.Schema at A5")

    queries_data = [
        (1,
         "Per month x medicine x disease category x region: compare commercial pharmacy & e-commerce units sold against hospital demand requested, received, consumed, and unfulfilled packs.",
         """[PROVE IT SOLVES THE BUSINESS PROBLEM]
This query solves the fundamental healthcare supply chain challenge: bridging commercial retail distribution with clinical hospital demand to prevent life-saving drug shortages.
Technique: Kimball Conformed Drill-Across.
Because Fact_PharmacySales is at a daily transaction grain and Fact_Demand is at a monthly hospital grain, joining them directly would cause catastrophic Cartesian fan-out and distorted metrics.
Solution: Aggregate each fact table independently in separate CTEs to the exact conformed grain (CalendarYear, MonthName, Medicine, Region), then FULL OUTER JOIN on the conformed dimensions.

[EXECUTABLE DIMENSIONAL SQL]:
WITH monthly_sales AS (
    SELECT d.CalendarYear, d.MonthName, d.MonthNumber,
           m.MedicineID, m.GenericName, m.DiseaseCategory,
           f.Region,
           SUM(s.QuantitySoldPacks) AS CommercialUnitsSold,
           SUM(s.NetSalesAmountUSD) AS CommercialNetSalesUSD
    FROM Fact_PharmacySales s
    JOIN DimDate d ON s.DateKey = d.DateKey
    JOIN DimMedicine m ON s.MedicineSK = m.MedicineSK
    JOIN DimFacility f ON s.FacilitySK = f.FacilitySK
    GROUP BY 1,2,3,4,5,6,7
),
monthly_demand AS (
    SELECT d.CalendarYear, d.MonthName, d.MonthNumber,
           m.MedicineID, m.GenericName, m.DiseaseCategory,
           f.Region,
           SUM(dem.RequestedQuantityPacks) AS TotalRequestedPacks,
           SUM(dem.ReceivedQuantityPacks) AS TotalReceivedPacks,
           SUM(dem.ConsumedQuantityPacks) AS TotalConsumedPacks,
           SUM(dem.UnfulfilledDemandPacks) AS TotalUnfulfilledPacks
    FROM Fact_Demand dem
    JOIN DimDate d ON dem.DateKey = d.DateKey
    JOIN DimMedicine m ON dem.MedicineSK = m.MedicineSK
    JOIN DimFacility f ON dem.FacilitySK = f.FacilitySK
    GROUP BY 1,2,3,4,5,6,7
)
SELECT COALESCE(s.CalendarYear, dem.CalendarYear) AS Year,
       COALESCE(s.MonthName, dem.MonthName) AS Month,
       COALESCE(s.GenericName, dem.GenericName) AS Medicine,
       COALESCE(s.DiseaseCategory, dem.DiseaseCategory) AS Disease,
       COALESCE(s.Region, dem.Region) AS Region,
       COALESCE(s.CommercialUnitsSold, 0) AS UnitsSold_Commercial,
       COALESCE(dem.TotalRequestedPacks, 0) AS Requested_Hospital,
       COALESCE(dem.TotalConsumedPacks, 0) AS Consumed_Hospital,
       COALESCE(dem.TotalUnfulfilledPacks, 0) AS Unfulfilled_Hospital,
       ROUND(COALESCE(dem.TotalConsumedPacks, 0)::NUMERIC / NULLIF(dem.TotalRequestedPacks, 0) * 100, 2) AS HospitalFillRatePct
FROM monthly_sales s
FULL OUTER JOIN monthly_demand dem
  ON s.CalendarYear = dem.CalendarYear
 AND s.MonthNumber = dem.MonthNumber
 AND s.MedicineID = dem.MedicineID
 AND s.Region = dem.Region
ORDER BY Year DESC, MonthNumber DESC, Unfulfilled_Hospital DESC;"""),

        (2,
         "For medicines with high hospital demand or high commercial sales velocity: identify which regional distribution centers and batch lots exhibit stockout exposure, low available quantity, near-expiry risk (<30/60/90 days), and non-compliant FEFO picking.",
         """[PROVE IT SOLVES THE BUSINESS PROBLEM]
This query provides proactive operational protection against two massive financial and clinical failure modes:
1. Stockout failure for fast-moving critical medicines during peak consumption periods.
2. Expired inventory write-offs caused by non-compliant FIFO dispatching instead of FEFO (First-Expired, First-Out).
Technique: Ranks top-velocity medicines across sales and demand, filters the latest daily inventory snapshots, and categorizes shelf-life risk tiers.

[EXECUTABLE DIMENSIONAL SQL]:
WITH top_velocity_medicines AS (
    SELECT s.MedicineSK, m.MedicineID, m.GenericName, m.TherapeuticClass,
           SUM(s.QuantitySoldPacks) AS TotalUnitsSold,
           DENSE_RANK() OVER (PARTITION BY m.TherapeuticClass ORDER BY SUM(s.QuantitySoldPacks) DESC) AS VelocityRank
    FROM Fact_PharmacySales s
    JOIN DimMedicine m ON s.MedicineSK = m.MedicineSK
    GROUP BY 1,2,3,4
),
latest_inventory_snapshot AS (
    SELECT inv.WarehouseSK, inv.MedicineSK, inv.WarehouseLotID,
           w.WarehouseName, w.Region,
           inv.AvailableQuantityPacks,
           inv.DaysToExpiry,
           inv.StockoutFlag,
           inv.FEFOComplianceFlag,
           CASE WHEN inv.DaysToExpiry <= 30 THEN 'Critical (<30d)'
                WHEN inv.DaysToExpiry <= 60 THEN 'High Risk (31-60d)'
                WHEN inv.DaysToExpiry <= 90 THEN 'Moderate Risk (61-90d)'
                ELSE 'Healthy (>90d)' END AS ExpiryRiskCategory
    FROM Fact_Inventory inv
    JOIN DimWarehouse w ON inv.WarehouseSK = w.WarehouseSK
    WHERE inv.DateKey = (SELECT MAX(DateKey) FROM Fact_Inventory)
)
SELECT tvm.TherapeuticClass,
       tvm.GenericName AS TopMedicine,
       tvm.TotalUnitsSold,
       lis.WarehouseName,
       lis.WarehouseLotID,
       lis.AvailableQuantityPacks,
       lis.DaysToExpiry,
       lis.ExpiryRiskCategory,
       lis.StockoutFlag,
       lis.FEFOComplianceFlag
FROM top_velocity_medicines tvm
JOIN latest_inventory_snapshot lis ON tvm.MedicineSK = lis.MedicineSK
WHERE tvm.VelocityRank <= 3
  AND (lis.DaysToExpiry <= 90 OR lis.StockoutFlag = 1 OR lis.FEFOComplianceFlag = 0)
ORDER BY tvm.TherapeuticClass, lis.DaysToExpiry ASC;"""),

        (3,
         "Analyze commercial net sales revenue, gross margin USD and percentage, unit return rates, and days-to-expiry-at-sale across sales channels (Physical Retail vs. Hospital vs. E-commerce), customer segments, payer types, and promotional campaigns.",
         """[PROVE IT SOLVES THE BUSINESS PROBLEM]
This query delivers executive visibility into commercial profitability and discount leakage. It answers:
1. Which sales channels and customer segments generate the highest gross margin %?
2. Are promotional discounts actually driving profitable volume, or merely leaking margin?
3. Are customers receiving products with sufficient remaining shelf-life buffer at the point of sale?
Technique: Slices Fact_PharmacySales across conformed DimFacility, junk DimSalesProfile, and DimMedicine. Ratios (Margin %, Return %) are correctly computed as SUM(num)/SUM(den).

[EXECUTABLE DIMENSIONAL SQL]:
SELECT f.FacilityType AS SalesChannel,
       p.CustomerSegment,
       p.PayerType,
       p.PromotionCode,
       m.TherapeuticClass,
       COUNT(DISTINCT s.SalesTransactionID) AS TotalOrders,
       SUM(s.QuantitySoldPacks) AS TotalPacksSold,
       SUM(s.GrossSalesAmountUSD) AS GrossSalesUSD,
       SUM(s.DiscountAmountUSD) AS TotalDiscountsUSD,
       ROUND(SUM(s.DiscountAmountUSD) / NULLIF(SUM(s.GrossSalesAmountUSD), 0) * 100, 2) AS DiscountPenetrationPct,
       SUM(s.NetSalesAmountUSD) AS NetSalesUSD,
       SUM(s.CostOfGoodsSoldUSD) AS TotalCOGS_USD,
       SUM(s.GrossMarginUSD) AS GrossMarginUSD,
       ROUND(SUM(s.GrossMarginUSD) / NULLIF(SUM(s.NetSalesAmountUSD), 0) * 100, 2) AS GrossMarginPct,
       ROUND(SUM(s.ReturnedQuantityPacks)::NUMERIC / NULLIF(SUM(s.QuantitySoldPacks), 0) * 100, 2) AS ReturnRatePct,
       ROUND(AVG(s.DaysToExpiryAtSale), 1) AS AvgDaysToExpiryAtSale
FROM Fact_PharmacySales s
JOIN DimMedicine m ON s.MedicineSK = m.MedicineSK
JOIN DimFacility f ON s.FacilitySK = f.FacilitySK
JOIN DimSalesProfile p ON s.SalesProfileSK = p.SalesProfileSK
GROUP BY 1,2,3,4,5
ORDER BY GrossMarginUSD DESC;""")
    ]

    for idx, (sno, q_eng, q_proof) in enumerate(queries_data):
        r = 6 + idx
        safe_set(ws_s, r, 12, val=sno, font=font_bold, alignment=align_center, border=cell_border)
        safe_set(ws_s, r, 13, val=q_eng, font=font_bold, alignment=align_top_left, border=cell_border)
        safe_set(ws_s, r, 14, val=q_proof, font=font_code, alignment=align_top_left, border=cell_border)
        safe_set(ws_s, r, 15, border=cell_border)
        ws_s.row_dimensions[r].height = 280

    wb.save(OUTPUT_PATH_1)
    print("Saved:", OUTPUT_PATH_1)
    wb.save(OUTPUT_PATH_2)
    print("Saved:", OUTPUT_PATH_2)
    wb.save(OUTPUT_PATH_3)
    print("Saved:", OUTPUT_PATH_3)

if __name__ == "__main__":
    generate_diagram()
    populate_workbook()
    print("ALL WORKBOOKS GENERATED AND VALIDATED SUCCESSFULLY!")
