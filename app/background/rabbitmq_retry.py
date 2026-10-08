import json
from app.background.rabbitmq import create_connection, declare_queue
from app.core.rabbitmq import RABBITMQ_RETRY_QUEUE

def publish_retry(test_case_id: int, result_id: int, attempts: int) -> None:
    connection = create_connection()

    try:
        channel = connection.channel()
        declare_queue(channel)

        delay_seconds = 5 * (
            2 ** (attempts - 1)
        )

        message = {
            "test_case_id": test_case_id,
            "result_id": result_id,
            "attempts": attempts
        }

        channel.basic_publish(
            exchange="",
            routing_key=RABBITMQ_RETRY_QUEUE,
            body=json.dumps(message),
            properties=__import__(
                "pika"
            ).BasicProperties(
                delivery_mode=2,
                expiration=str(
                    delay_seconds * 1000
                ),
            ),
        )

        print(
            f"Retry schedule in "
            f"{delay_seconds} seconds"
        )
    finally:
        connection.close()