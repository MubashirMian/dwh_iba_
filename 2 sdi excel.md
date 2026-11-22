\# 02 — SDI EXCEL (design-first; carries the most marks)

\*\*Goal:\*\* (a) a machine-readable model spec \`docs/model\_spec.json\`, (b) \`excel/SDI.Excel.xlsx\` built \*\*from the spec\*\* on top of the instructor's template \`excel/template/DAWH.DWH.Template\_1.xlsx\` (human places it there; the template must be kept intact in look/structure).  
\*\*Prereq:\*\* Stage 1 outputs (\`data\_profile.md\`, \`data\_dictionary.md\`). \*\*Next:\*\* \`03\_...\`.  
Final numbers/proofs are added in Stage 9 after the DWH exists (the build script is re-runnable).

\#\# Why spec-first  
\`model\_spec.json\` is the single source of truth for: Excel sheets, DDL/dbt models (Stage 5), BI views (Stage 8), BI Excel and later phases. Any later change \= edit spec → re-run \`python excel/build\_sdi\_excel.py\`.

\#\# 🛑 ASK HUMAN (short)  
1\. Place the template at \`excel/template/DAWH.DWH.Template\_1.xlsx\`.  
2\. Team role-play: who plays the stakeholders (Head of Sales, Demand Planner, Hospital Supply Manager, Finance/Pricing, C-suite)? Default: agent invents roles; human may give 3–5 real analytical questions they want. Proceed with defaults if no answer.

\#\# Template structure (verified — do not break)  
Sheets: \`ReadMe\`, \`Business.Req.XRay\`, \`OLTP.XRay\`, \`Transform.OLTP\`, \`Dim.Tables\`, \`Fact.Table\`, \`Star.Schema\`. Titles use green fill \`92D050\`. ReadMe is informational — leave as is.  
\| Sheet \| Layout facts \|  
\|---\|---\|  
\| Business.Req.XRay \| Questions in A2:A11 (merged A:B); answers go in \*\*C2:F11 (merged C:F per row)\*\*. 10 prompts: domain, process, how the process runs, stakeholders, competitors, case studies, stakeholder analytical requirements, AI-found standard requirements, KPIs (standard/global names), reason for building. \|  
\| OLTP.XRay \| C2 (reason) and C3 (tables list) are \*\*pre-filled\*\* — keep. Excel Table \`Table223\` A4:F51 with columns: Sno · Your selected OLTP Table · DimTable fed · Attributes exported · Facts/KPIs exported · Comments. Sno 1–3 pre-numbered. \|  
\| Transform.OLTP \| Dimension-attribute section from row 2 (headers: Sno, Attrb.Name, DimTable Name, Data.Type, Transformation Action \[merged E:F\], Comments in G); fact-attribute section starts at row 20/21 with the same headers (FactTable name). \|  
\| Dim.Tables \| Blocks: DimDate (row 2), Dim Table 2 (17), 3 (32), 4 (46); each \= name row, "Primary/Surrogate Key:", "Natural Key:", header row (Attribute, Data.Type, SCD Strategy \[merged C:E\], Hierarchy, Comments) \+ \~11 attribute rows. Row 61+: "Other Dimension Types: Role-Playing, Outrigger, Junk, Bridge, Snowflaked" block (Dim Table / keys / \*\*Dim Table Type\*\* row / header / rows). \|  
\| Fact.Table \| Name, Grain, Type (\`\<Transactional/Periodic/Accumulating/Factless\>\` placeholder → replace), PK, Partitioning, Indexing, then header row 8: S.No, Name, Data.Type, FK (Y/N), Measure Type (Fully/Semi/Non), Degenerate (Y/N), OLTP Source Table, Comments. \|  
\| Star.Schema \| Image area merged \*\*A5:H40\*\*; right side L4 "3 Solvable Dimensional Queries": columns L Sno · M Query (English) · N:O "Prove it solves the business problem". \|

\#\# Tasks  
\#\#\# 2.1 Design the SDI model → \`docs/model\_spec.json\`  
Derive from the real columns (Stage 1). Start from this \*\*default design\*\*, then adapt names/attributes to what exists (drop what the data cannot support; never invent columns that don't exist in sources — derived attributes are OK if the transformation is stated):

\*\*Business questions (the mart must answer):\*\* hospital forecast vs actual consumption ratio; unfulfilled demand; channel revenue split and gross margin (Retail vs Hospital vs E-commerce); top-10 fast vs slow-moving medicines per therapeutic class; trend over time; region/hospital drill-down.

\*\*Dimensions (conformed ones marked ★ for future marts):\*\*  
