# SDI Mart: Agent Prompts (Verify → Build)

Use **Prompt A first, in its own session**. Review its evidence. Then run **Prompt B in a new session**. Both assume `AGENTS.md` and `PROGRESS.md` from the main instruction set are in the repo. If they are not, the agent should create `PROGRESS.md` and continue.

Replace the `<…>` placeholders before pasting.

---

# PROMPT A: SDI Design Verification Against the Real Data

```
ROLE
You are a senior data engineer and Kimball-trained dimensional modeler. Your job in this
session is to VERIFY a dimensional design against the real source data and make evidence-based
decisions. You are not here to build the pipeline yet.

CONTEXT
Course project: Pharma Cold-Chain DWH + BI. Phase 1 is the "Sales & Demand Intelligence (SDI)"
mart: a fact constellation of three facts (Fact_PharmacySales, Fact_Demand, Fact_Inventory)
with conformed dimensions (DimDate, DimMedicine SCD2, DimFacility, DimWarehouse, DimSalesProfile).
The design is documented in the workbook <path/to/SDI_Excel.xlsx> (sheets: Business.Req.XRay,
OLTP.XRay, Transform.OLTP, Dim.Tables, Fact.Table, Fact.Table.Demand, Fact.Table.Inventory,
Star.Schema with an embedded diagram and 3 dimensional queries Q1-Q3).
Source files (read-only): <path>/01_master_data.csv, 04_warehouse_data.csv,
05_pharmacy_sales_data.csv, 06_hospital_demand_data.csv. Also profile 02_manufacturing_data.csv
and 03_manufacturer_delivery_data.csv, but ONLY for lineage and expiry lookups.
Deadline pressure: Phase 1 Milestone 2 is 25 Nov 2026. Time-box this session to ~3 hours of work.
Be efficient: DuckDB over CSV directly (read_csv_auto) is the preferred tool. No Docker needed.

GROUND RULES
1. The DATA is the source of truth. The workbook is a set of HYPOTHESES to test. If they disagree,
   the data wins and you record a decision.
2. Source files are READ-ONLY. Never modify, move or delete them. Do not edit the workbook in this
   session (Prompt B does that). Write only under docs/sdi_verification/ and sql/verification/ and
   scripts/.
3. Every claim in your report must be backed by a query you ran, with its result saved. No claim
   without evidence. If you could not test something, say "NOT TESTED" and why.
4. Do not invent columns, values, or business rules. If a column the workbook assumes does not
   exist, report it, list the closest real column(s), and propose options.
5. Make decisions yourself when they are reversible; log each as an ADR. Ask the human only for
   (a) missing files, (b) choices that are instructor-defined, (c) irreversible actions.
6. Be reproducible: all checks run from one script (scripts/verify_sdi.py) that regenerates every
   result file. Seed any sampling.

STEP 0: Locate and inventory
- Find the 4 (+2) source files and the workbook. If any is missing, STOP and ask.
- For each CSV: row count, column list with inferred types, null % per column, distinct count per
  column, min/max for numeric/date columns, duplicate-PK check on the documented PK, encoding and
  delimiter issues, whitespace/case anomalies in key and categorical columns.
- Compare row counts to the spec: 63 / 561 / 999 / 112,184 / 500,000 / 27,216 (01..06). Report any difference.
- Extract the workbook: for every dimension and fact column it lists, mark whether the named
  source column exists (EXISTS / MISSING / RENAMED:<real name>). Save as
  docs/sdi_verification/00_column_traceability.csv. This is the master traceability matrix.

STEP 1: Test each hypothesis (H1-H18). For each one: write the SQL, run it, save the result, then
state PASS / FAIL / PARTIAL / NOT TESTED, the evidence in one or two lines, and the decision.

Dimension and lineage hypotheses
H1  SCD2 history exists. Does 01_master_data have more than one row per MedicineID, or varying
    EffectiveFromDate? If there is only one version per SKU, SCD2 cannot be demonstrated from base
    data. Decision: the generator must inject attribute changes in refresh R2 (note this).
H2  Region derivation. The workbook assumes "4 US regions" mapped from State. Check the distinct
    values of CountryCode / State / City across pharmacies, hospitals and warehouses. Are all US?
    Is a region column already present? Decide how Region is derived and test that 100% of
    facilities and warehouses map to a region (no unknowns).
H3  Channel semantics. List distinct SalesChannel and PharmacyType values with counts, and a
    cross-tab SalesChannel x PharmacyType. Decide: how many channels exist (2 or 3), which rows
    represent the "Hospital" channel, and which identifier (PharmacyID vs HospitalID) is populated
    for them. This decides the DimChannel design and whether Q1 must exclude hospital-channel sales.
H4  Conformed DimFacility feasibility. Do PharmacyID and HospitalID share a format? Any ID overlap
    that would collide in a union? Are hospital IDs in 05 the same IDs as in 06? Decide: union into
    DimFacility with a type attribute, or keep DimHospital and DimPharmacy separate.
H5  Junk dimension size. Count distinct combinations of (PrescriptionRequiredFlag, CustomerSegment,
    PayerType, PaymentMethod, PromotionCode, SaleStatus, ReturnFlag). Report the PromotionCode
    cardinality alone. Rule: if combinations > ~500 or PromotionCode is high-cardinality or
    time-varying, split PromotionCode into its own DimPromotion; else keep one junk dimension.
H6  Return representation. Compare ReturnFlag, SaleStatus and ReturnedQuantityPacks: are they
    mutually consistent? Is ReturnedQuantityPacks <= QuantitySoldPacks everywhere? Decide
    which field is authoritative and whether ReturnFlag/SaleStatus are redundant in the junk dim.
H7  Warehouse dimension grain. Test functional dependencies: within WarehouseID, do
    WarehouseName, GLN, capacity and status stay constant over time? Do StorageZoneID and
    StorageCondition vary within a warehouse? Rule: if zone varies, add DimStorageZone (or make the
    warehouse dimension zone-grain); if capacity or status vary over time, SCD2 on those attributes.
H8  Hospital attributes. Per HospitalID, are LicensedBeds, ICUBeds, TraumaLevel,
    CatchmentPopulation constant over time? Where are MedicationRequestStatus and FormularyStatus
    used (per row or per hospital)? Rule: row-varying low-cardinality status -> DimDemandProfile
    (junk); per-hospital constant -> DimFacility. The same test for InventoryStatus and
    WarehouseActivityStatus -> DimInventoryStatus (junk) or DimWarehouse.
H9  DimMedicine columns. Confirm every column in OLTP.XRay for 01 exists, and that
    WholesalePriceUSD, StorageMinTempC, StorageMaxTempC and ShelfLifeMonths are carried into the
    dimension (workbook Dim.Tables currently omits them and EffectiveFrom/To). Check
    StorageMin < StorageMax, costs and prices > 0, and ColdChainFlag consistent with temperature range.

Fact-level hypotheses
H10 Sales arithmetic. Test Gross = Qty x UnitPrice, Net = Gross - Discount, Margin = Net - COGS.
    Report the % of rows that violate each (with tolerance 0.01). Test COGS vs
    Qty x UnitManufacturingCostUSD from the master (point-in-time if history exists). Decision: for
    each measure, load the source value, or recompute and log the delta in DQ.
H11 Sales grain and lineage. SalesTransactionID unique? % of sales whose WarehouseLotID resolves
    to 04_warehouse, and whose ProductionBatchID resolves to 02. Does one WarehouseLotID map to
    exactly one WarehouseID? Does the sale's medicine equal the lot's medicine? Report orphan counts.
H12 DaysToExpiryAtSale. Compare the source value to (lot expiry date - SaleDate), where lot
    expiry = snapshot date + DaysToExpiry from 04, or the batch expiry from 02. Decide which
    source of expiry is authoritative; report the % match and the typical error.
H13 Demand grain and measures. HospitalDemandRecordID unique, and (HospitalID, MedicineID, Month)
    unique? What is the month key format? Test whether UnfulfilledDemandPacks equals
    GREATEST(0, Requested - Received), GREATEST(0, Requested - Consumed) or neither (% match
    each). Test ServiceLevelPct against Received/Requested and Consumed/Requested. Test the stock
    identity Opening + Received - Consumed - Wastage = Closing (and a variant with Dispensed).
    Decision rules: if the source Unfulfilled column matches Requested-Received in >= 99% of
    rows, define fulfilment as Received/Requested and use the source column; if it matches
    Requested-Consumed, document that definition; else keep the source column as-is and record
    the definition as "source-defined, unreconciled".
H14 Inventory grain and density. (WarehouseLotID, WarehouseID, SnapshotDate) unique? Are
    snapshots dense (every lot daily) or sparse? Per warehouse: first/last snapshot date and the
    number of missing days. This decides whether "latest snapshot" must be defined per lot and
    warehouse rather than a global MAX(date).
H15 DaysToExpiry semantics. Within a lot, how does DaysToExpiry change across snapshot dates?
    Does it decrease by exactly the date difference (as-of-snapshot, which is good) or stay
    static? Verify the derived ExpiryDate (= SnapshotDate + DaysToExpiry) is constant per lot.
    Conclusion needed: DaysToExpiry must be stored as-of SnapshotDate and never recomputed vs
    the current date; confirm or refute with data.
H16 Inventory flags and identity. Compare StockoutFlag to (AvailableQuantity = 0),
    NearExpiryFlag to (DaysToExpiry <= 90), and describe FEFOComplianceFlag (grain? per lot-day or
    per dispatch? distribution by warehouse). Test the movement identity: Closing = Opening +
    Received - Shipped - Expired - Damaged +/- Adjustment (find the version that holds, and
    report the % that fail). Decide which extra quantity columns must be added to Fact_Inventory
    so the identity is testable (Picked, Damaged, Adjustment, Putaway, etc.).
H17 Cross-file regional consistency. For sales: does the region of the pharmacy equal the region
    of the lot's warehouse? Hospital region vs warehouse region? This affects Q1's "region" and
    whether the commercial-vs-hospital comparison is meaningful at region grain.
H18 Date coverage. Min/max date per file and months present vs expected. Note that 2023-2025
    must be fully covered, and list gaps.

STEP 2: Test the workbook's three queries against a throwaway prototype
- Build a quick prototype star in a scratch DuckDB file (scratch/sdi_proto.duckdb) from the CSVs
  using the workbook's logic (surrogate keys can be simple). This is a TEST HARNESS only, not the
  production model.
- Run Q1, Q2, Q3 EXACTLY as written in the workbook. Record: runs / errors (copy the exact
  error text), row counts, and any silent logic problems.
- Known suspicions to confirm or refute by experiment, not by assertion:
  a) Q1: ORDER BY MonthNumber is ambiguous (both CTEs expose it) -> expect a Binder error.
  b) Q1: includes hospital-channel sales although the query text says pharmacy and e-commerce
     only -> quantify the overlap by units.
  c) Q2: joins sales velocity and inventory on MedicineSK; with SCD2 versions this splits
     velocity and drops inventory rows -> demonstrate with a medicine that has 2 versions (create
     a synthetic version row in the prototype if the base data has none, and say that you did).
  d) Q2: ranks on sales only although the text says "high hospital demand OR high sales";
     it also uses a global MAX(DateKey) snapshot -> check how many warehouses lack that date.
  e) Q3: "channel" is taken from FacilityType; compare with SalesChannel; AVG(DaysToExpiryAtSale)
     is a per-transaction average -> compare with the pack-weighted average and report the gap.
- Write corrected versions Q1', Q2', Q3' (sql/verification/q1_fixed.sql etc.) that fix every
  confirmed issue. Reconcile each to raw data:
  Q1' total units sold (pharmacy + e-commerce only) = SUM over raw 05 with the same filter;
      hospital quantities = SUM over raw 06. No fan-out.
  Q3' totals (sales, margin, units) = raw 05 totals.
  Q2' returns a non-empty, explainable result; show 5 sample rows hand-verified against raw data.

STEP 3: Documentation-risk review of the workbook (no data needed)
- Business.Req.XRay: list every statistic, dollar figure, percentage and named "case study" or
  reference. For each, mark SOURCED (URL you actually opened and read), UNSOURCED, or
  UNVERIFIABLE. Do not "confirm" anything from memory. If you have web access, search and cite;
  if not, mark UNVERIFIED. Propose to remove or reword every unsourced figure.
- Flag unprofessional or off-scope text (for example, the OLTP.XRay "reason" line, and KPIs
  that need files outside this mart such as OTIF, which needs 03).
- Check the diagram: is it clipped, does it show role-playing dates, does it match the columns in
  Dim.Tables / Fact.Table sheets? List every mismatch between diagram and sheets.

DECISION FORMAT (one ADR per decision, in docs/decisions/, numbered from the next free number)
  Title / Context / Hypothesis tested / Evidence (SQL file + result file + key numbers) /
  Options considered / DECISION / Consequences for the model, DQ rules and the generator /
  Confidence (HIGH, MEDIUM, LOW) and what would change your mind.
Group related findings into one ADR; there should be roughly 8-15 ADRs, not 40.

OUTPUTS (all under the repo)
  docs/sdi_verification/00_column_traceability.csv
  docs/sdi_verification/01_profile.md              (per-file profile tables)
  docs/sdi_verification/02_findings.md             (H1-H18 table: result, evidence, decision, ADR link)
  docs/sdi_verification/03_query_test_report.md    (Q1-Q3 as-written vs fixed, with errors and reconciliations)
  docs/sdi_verification/04_workbook_change_list.md (a precise, cell-level/sheet-level list of edits for
        the workbook v01: what to add, change or remove, each tied to a finding)
  docs/sdi_verification/05_doc_risk_review.md
  docs/sdi_verification/06_generator_requirements.md (what the data generator must produce because
        of the findings: SCD2 changes, defect injection, lineage rules, volumes)
  docs/decisions/NNN-*.md
  sql/verification/*.sql  +  sql/verification/results/*.csv  +  scripts/verify_sdi.py
  PROGRESS.md updated

DEFINITION OF DONE
- `python scripts/verify_sdi.py` regenerates every result file with no manual step.
- Every H1-H18 has a status with evidence, or "NOT TESTED" with a reason.
- Q1', Q2', Q3' run without error and reconcile to raw totals (numbers shown).
- The change list is specific enough that another engineer could edit the workbook from it alone.
- No source file or the original workbook was modified (show checksums before and after).

FINISH WITH
  Done / Evidence (key numbers) / Decisions made (list ADR titles) / Needs human decision
  (only true blockers, each with your recommendation) / Risks to the 25 Nov milestone / Next.
Then STOP. Do not start building.
```

---

# PROMPT B: SDI v01 (Corrected Workbook → Silver/Gold Models → Query Tests)

Run only after Prompt A's outputs are reviewed. If Prompt A raised "Needs human decision" items, answer them in the placeholder below.

```
ROLE
Senior data engineer / BI engineer. Continue the Pharma Cold-Chain DWH project, Phase 1 (SDI mart).

INPUTS (read first)
  AGENTS.md, PROGRESS.md, docs/decisions/*, docs/sdi_verification/* (especially 04_workbook_change_list.md,
  03_query_test_report.md and 06_generator_requirements.md), sql/verification/q*_fixed.sql, and the
  original workbook <path/to/SDI_Excel.xlsx> (keep as -00, never overwrite).
Human decisions on open items: <paste answers, or "none; follow your recommendations">.
Deadline: Phase 1 Milestone 2 is 25 Nov 2026. Priorities are tagged MUST / SHOULD / COULD; drop
COULD first, then SHOULD. Never drop MUST.

TASK 1 [MUST]: Workbook v01
- Copy the workbook to excel/DAWH_DWH_Pharma_ColdChain_Sales_Demand-01.xlsx and apply EVERY item in
  04_workbook_change_list.md, using openpyxl (preserve formatting; do not rebuild sheets from scratch).
- Add a "Changelog" sheet: each change, the finding/ADR it came from, and before/after.
- Keep sheet names and the existing layout: Dim.Tables, Fact.Table.PharmSales (rename if needed
  and say so), Fact.Table.Demand, Fact.Table.Inventory, Star.Schema (with the 3 queries and
  "prove it" text). Add a "Role-Playing" section and mark junk dimensions, bridge tables if any.
- Replace the three SQL queries with the verified Q1', Q2', Q3' and, for each, add a "Result evidence" row:
  row count and 3-5 sample rows from the real data, plus the reconciliation numbers.
- Business.Req.XRay: remove or reword every statistic and case study marked UNSOURCED /
  UNVERIFIABLE in 05_doc_risk_review.md. Keep only claims with a source you actually opened, with the
  URL. Replace the unprofessional "reason" line. Move out-of-scope KPIs (e.g., OTIF) to a "Later phases" note.
- Regenerate the star-schema diagram (Python, e.g., matplotlib/graphviz/SVG to PNG) so that it
  matches the sheets exactly, is not clipped, shows role-playing dates (sale/snapshot/demand month/
  expiry), the junk dimensions, and every FK. Embed it in Star.Schema.
- Validate: the workbook opens without errors; every dimension/fact column traces to a real source
  column or a documented derivation (re-run the traceability check and attach the result).

TASK 2 [MUST]: Build the SDI model with dbt-duckdb (follow AGENTS.md rules)
- Source abstraction: a dbt var `source_mode` = `postgres` (Bronze tables via ATTACH, the real
  path) or `csv` (read_csv over data/source, the fallback if the platform/Bronze is not ready yet).
  Same models either way. State which mode you ran.
- Silver: typed/trimmed/deduped models for 01, 04, 05, 06 applying the DQ rules from the ADRs
  (price > 0, valid dates, expiry > manufacture, non-null keys, non-negative quantities, return <= sold,
  arithmetic identities within tolerance). Rejected rows -> dq.rejected_rows (or a rejects table in
  csv mode) with reason codes. Never drop silently.
- Gold, exactly as in workbook v01: dim_date (with YearMonth, MonthStartDateKey, role-playing views),
  dim_medicine (SCD2 via dbt snapshot; ValidFrom/ValidTo; point-in-time lookups), dim_facility (and
  dim_channel / dim_sales_profile / dim_promotion / dim_warehouse / junk dims as decided), an
  unknown member (-1) in every dimension, and the three facts: fact_pharm_sales (transaction),
  fact_demand (monthly periodic snapshot), fact_inventory (daily lot periodic snapshot, semi-additive).
  DaysToExpiry is stored AS OF SnapshotDate, with ExpiryDateKey; never recomputed against today.
- Incremental by `_batch_id`; the whole build must be idempotent (run twice -> no change).
- Tests: unique, not_null, relationships on every key; accepted_values on flags; custom tests for
  the arithmetic identities, SCD2 non-overlap (no gaps/overlaps in ValidFrom/ValidTo), and the
  inventory movement identity decided in Prompt A.
- Reconciliation tests (tests/reconciliation/): Bronze/source rows = Silver rows + rejects;
  Silver = Gold per fact; measures sums match raw.

TASK 3 [MUST]: Make Q1-Q3 the acceptance tests
- Put Q1', Q2', Q3' in sql/bench/ with the tag lines `-- dashboard: <page>; widget: <name>`.
- Run them on the Gold tables. Each returns a non-empty result and reconciles to raw (show numbers).
- Add a test that fails if any query uses MedicineSK in a cross-fact join (must use the natural key
  or the current-version rule), to prevent the SCD2 trap from returning.

TASK 4 [SHOULD]: Prepare for refreshes
- Apply 06_generator_requirements.md: write the generator spec stub for SDI (what to generate for
  R1/R2: volumes, SCD2 changes, defect rates, lineage rules). If the generator already exists,
  verify it satisfies these requirements and list gaps.
- Add `agg_*` summary tables for the three queries and a before/after timing of Q1'-Q3'.

TASK 5 [SHOULD]: Metric dictionary
- docs/metrics.md for the SDI metrics (net sales, gross margin %, return rate, discount penetration,
  hospital fulfilment, forecast-to-actual, WAPE, unfulfilled demand rate, DoIC, stockout rate,
  near-expiry value at risk, FEFO %, expiry waste %): definition, formula, grain, additivity, source.
  Ratios are always SUM(num)/SUM(den). Inventory balances are semi-additive.

DO NOT
- Do not modify source CSVs or workbook -00. Do not build BI dashboards or Airflow DAGs here, except
  a minimal `dag_mart_sdi` if the Airflow platform already exists (say so if you skip it).
- Do not trust the workbook where Prompt A's ADRs overrode it.

DEFINITION OF DONE
- `dbt build` green (show summary); reconciliation tests pass (show numbers).
- Workbook -01 and Gold match column-for-column (attach the check).
- Q1', Q2', Q3' pass and reconcile; the SCD2 point-in-time proof: pick one medicine with two versions
  and show sales rows pointing to the correct version by date.
- Second `dbt build` with no new data changes nothing (show row counts before/after).
- PROGRESS.md updated; tag `iter-sdi-v01`.

FINISH WITH
  Done / Evidence / Assumptions / Open questions / Risks to 25 Nov / Next.
Then STOP.
```

---

# What comes after Prompt B

| Next | Where it comes from |
|---|---|
| Query-layer optimization and the Grafana query-performance dashboard | Main instruction set, Iteration 5 |
| Superset dashboards for Q1, Q2, Q3 and two live refreshes | Iteration 6 (Milestone 2) |
| Platform, ingestion and observability, if not already done (run in a **separate parallel session**) | Iterations 1-3 |
| Phase 2: extend `fact_inventory` with manufacturing and shipment lineage | Iteration 7 |
