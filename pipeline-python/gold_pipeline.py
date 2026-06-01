from sqlalchemy import create_engine, text

engine = create_engine(
    "postgresql+psycopg2://trade_user:trade_password@localhost:5432/trade_db"
)

def main():
    with engine.begin() as conn:

        conn.execute(text("""
            DELETE FROM gold_trades
        """))

        conn.execute(text("""
            INSERT INTO gold_trades (
                trade_id,
                latest_event_id,
                trade_status,
                quantity,
                price,
                counterparty,
                instrument,
                currency,
                last_updated_at
            )
            SELECT DISTINCT ON (trade_id)
                trade_id,
                event_id,
                event_type,
                quantity,
                price,
                counterparty,
                instrument,
                currency,
                event_timestamp
            FROM silver_trade_events
            WHERE is_valid = true
            ORDER BY trade_id, event_timestamp DESC
        """))

        print("Silver → Gold completed")

if __name__ == "__main__":
    main()