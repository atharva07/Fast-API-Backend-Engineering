import json
from app.background.rabbitmq import create_connection, declare_queue
from app.core.rabbitmq import RABBITMQ_QUEUE

def send_test_execution(test_case_id: int, result_id: int) -> None:
    connection = create_connection()
    try:
        channel = connection.channel()
        declare_queue(channel)

        message = {
            "test_case_id": test_case_id,
            "result_id": result_id,
            "attempts": 0,
        }

        channel.basic_publish(exchange="", routing_key=RABBITMQ_QUEUE, body=json.dumps(message))
        print(f"Job published: {message}")
    finally:
        connection.close()