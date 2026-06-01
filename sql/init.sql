CREATE TABLE IF NOT EXISTS bronze_trade_events (
    id SERIAL PRIMARY KEY,
    kafka_partition INTEGER,
    kafka_offset BIGINT,
    received_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    raw_event JSONB
);

CREATE TABLE IF NOT EXISTS silver_trade_events (
    event_id VARCHAR(100) PRIMARY KEY,
    trade_id VARCHAR(100),
    event_type VARCHAR(50),
    event_timestamp TIMESTAMP,
    quantity NUMERIC,
    price NUMERIC,
    counterparty VARCHAR(100),
    instrument VARCHAR(100),
    currency VARCHAR(10),
    is_valid BOOLEAN,
    validation_error TEXT,
    processed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS gold_trades (
    trade_id VARCHAR(100) PRIMARY KEY,
    latest_event_id VARCHAR(100),
    trade_status VARCHAR(50),
    quantity NUMERIC,
    price NUMERIC,
    counterparty VARCHAR(100),
    instrument VARCHAR(100),
    currency VARCHAR(10),
    last_updated_at TIMESTAMP
);