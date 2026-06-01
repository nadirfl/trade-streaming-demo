import json
from confluent_kafka import Consumer
from sqlalchemy import create_engine, text

engine = create_engine(
    "postgresql+psycopg2://trade_user:trade_password@localhost:5432/trade_db"
)

consumer = Consumer({
    'bootstrap.servers':'localhost:9092',
    'group.id':'trade-consumer-group',
    'auto.offset.reset':'earliest'
})

consumer.subscribe(['trade-events'])

print("Waiting for trade events...")

try:
    while True:
        msg = consumer.poll(1.0)

        if msg is None:
            continue

        if msg.error():
            print(f"Consumer error: {msg.error()}")
            continue

        raw_json = msg.value().decode('utf-8')

        print(f"Received: {raw_json}")

        with engine.begin() as conn:
            conn.execute(
                text("""
                        INSERT INTO bronze_trade_events (
                        kafka_partition,
                        kafka_offset,
                        raw_event
                    )
                    VALUES (
                        :partition,
                        :offset,
                        CAST(:raw_event AS JSONB)
                    )
                """),
                {
                    "partition": msg.partition(),
                    "offset": msg.offset(),
                    "raw_event": raw_json
                }
            )
except KeyboardInterrupt:
    print("Stopping consumer...")

finally:
    consumer.close()