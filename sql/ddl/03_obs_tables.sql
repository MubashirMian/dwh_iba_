-- 03_obs_tables.sql

-- DQ Rejection Quarantine Table
CREATE TABLE IF NOT EXISTS dq.rejected_rows (
    rejection_id BIGSERIAL PRIMARY KEY,
    source_table TEXT NOT NULL,
    source_row_id TEXT,
    rejection_reason TEXT NOT NULL,
    rule_id TEXT NOT NULL,
    rejected_payload JSONB,
    rejected_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_rejected_rule ON dq.rejected_rows (rule_id);
CREATE INDEX IF NOT EXISTS idx_rejected_source ON dq.rejected_rows (source_table);

-- Observability Query Performance Log Table
CREATE TABLE IF NOT EXISTS obs.query_log (
    log_id BIGSERIAL PRIMARY KEY,
    query_tag TEXT NOT NULL,
    dashboard_name TEXT,
    widget_name TEXT,
    execution_timestamp TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    duration_ms NUMERIC(10, 2) NOT NULL,
    rows_returned BIGINT NOT NULL,
    user_or_role TEXT DEFAULT CURRENT_USER,
    is_cold_run BOOLEAN DEFAULT FALSE,
    query_text TEXT
);

CREATE INDEX IF NOT EXISTS idx_query_log_tag ON obs.query_log (query_tag);
CREATE INDEX IF NOT EXISTS idx_query_log_timestamp ON obs.query_log (execution_timestamp);
