-- Create a table for monthly US-Iran geopolitical conflict indicators
CREATE TABLE IF NOT EXISTS gdelt_monthly (
    month DATE PRIMARY KEY,
    conflict_events INTEGER NOT NULL,
    avg_goldstein NUMERIC(6, 2),
    total_mentions BIGINT NOT NULL,

    CONSTRAINT chk_conflict_events
        CHECK (conflict_events >= 0),

    CONSTRAINT chk_total_mentions
        CHECK (total_mentions >= 0),

    CONSTRAINT chk_avg_goldstein
        CHECK (avg_goldstein BETWEEN -10 AND 10)
);