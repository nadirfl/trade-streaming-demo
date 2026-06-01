import json
from datetime import datetime
from decimal import Decimal

from sqlalchemy import create_engine, text

engine = create_engine(
    "postgresql+psycopg2://trade_user:trade_password@localhost:5432/trade_db"
)

def validate_event(event: dict) -> tuple[bool, str | None]:
    required_fields = [
        "eventId",
        "tradeId",
        "eventType",
        "eventTimestamp",
        "quantity",
        "price",
        "counterparty",
        "instrument",
        "currency",
    ]

    for field in required_fields:
        if field not in event or event[field] is None:
            return False, f"Missing required field: {field}"
    
    if event["eventType"] not in ["NEW", "AMEND", "CANCEL"]:
        return False, f"Missing required field: {field}"
    
    return True, None

def parse_timestamp(value):
    if isinstance(value, (int, float)):
        return datetime.fromtimestamp(value)

    if isinstance(value, str):
        return datetime.fromisoformat(value.replace("Z", "+00:00"))

    raise ValueError(f"Unsupported timestamp format: {value}")

def main():
    with engine.begin() as conn:
        bronze_rows = conn.execute(
            text("""
                SELECT id, raw_event
                FROM bronze_trade_events
                ORDER BY id
            """)
        ).fetchall()

        print(f"Found {len(bronze_rows)} bronze events")

        for row in bronze_rows:
            raw_event = row.raw_event

            if isinstance(raw_event, str):
                event = json.loads(raw_event)
            else:
                event = raw_event

            is_valid, validation_error = validate_event(event)

            conn.execute(
                text("""
                    INSERT INTO silver_trade_events (
                        event_id,
                        trade_id,
                        event_type,
                        event_timestamp,
                        quantity,
                        price,
                        counterparty,
                        instrument,
                        currency,
                        is_valid,
                        validation_error
                    )
                    VALUES (
                        :event_id,
                        :trade_id,
                        :event_type,
                        :event_timestamp,
                        :quantity,
                        :price,
                        :counterparty,
                        :instrument,
                        :currency,
                        :is_valid,
                        :validation_error
                    )
                    ON CONFLICT (event_id) DO NOTHING
                """),
                {
                    "event_id": event.get("eventId"),
                    "trade_id": event.get("tradeId"),
                    "event_type": event.get("eventType"),
                    "event_timestamp": parse_timestamp(event["eventTimestamp"]) if event.get("eventTimestamp") else None,
                    "quantity": Decimal(str(event["quantity"])) if event.get("quantity") is not None else None,
                    "price": Decimal(str(event["price"])) if event.get("price") is not None else None,
                    "counterparty": event.get("counterparty"),
                    "instrument": event.get("instrument"),
                    "currency": event.get("currency"),
                    "is_valid": is_valid,
                    "validation_error": validation_error,
                }
            )

        print("Bronze to Silver completed")

if __name__ == "__main__":
    main()