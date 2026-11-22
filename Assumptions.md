# **ASSUMPTIONS.md — every assumption/default decision (feeds the report's mandatory "Assumptions" section)**

Format: `A-<nn> | Stage | Assumption | Why | Impact`

A-01 \| 1 \| CSV files are ingested directly (the project text says "Excel files" but sources are .csv). \| Sources listed as .csv in the spec. \| None. A-02 \| 1 \| Power BI Desktop (Windows) connects to Postgres `bi` schema in DirectQuery/Import; DuckDB is not queried by Power BI directly. \| Power BI has no native DuckDB connector. \| Mart is mirrored to Postgres after each refresh.

