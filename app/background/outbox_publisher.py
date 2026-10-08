import json
import time
from app.background.rabbitmq import create_connection
from app.core.rabbitmq import RABBITMQ_QUEUE
from app.db.database import SessionLocal
from app.repositories.outbox_event import OutboxEventRepository

def publish_pending_events() -> None:
    connection = create_connection()
    channel = connection.channel()

    db = SessionLocal()

    try:
        repository = OutboxEventRepository(db)

        events = repository.get_pending_events()

        for event in events:
            try:
                message = json.loads(event.payload)

                channel.basic_publish(
                    exchange="",
                    routing_key=RABBITMQ_QUEUE,
                    body=json.dumps(message),
                    properties=__import__("pika").BasicProperties(
                        delivery_mode=2,
                    ),
                )

                event.status = "PUBLISHED"

                db.commit()

                print(
                    f"Published outbox event "
                    f"{event.id} to RabbitMQ"
                )

            except Exception as exc:
                db.rollback()

                print(
                    f"Failed to publish outbox event "
                    f"{event.id}: {exc}"
                )
    finally:
        db.close()
        connection.close()

def start_outbox_publisher() -> None:
    print("Outbox publisher started")

    while True:
        try:
            publish_pending_events()

        except Exception as exc:
            print(
                f"Outbox Publishing Failed: {exc}"
            )

        time.sleep(5)
