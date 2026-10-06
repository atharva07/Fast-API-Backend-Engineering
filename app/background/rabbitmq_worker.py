import json
import time
from app.background.rabbitmq import create_connection, declare_queue
from app.core.rabbitmq import RABBITMQ_QUEUE

def process_test_execution(test_case_id: int, result_id: int) -> None:
    print(
        f"Executing test case = {test_case_id}, "
        f"result_id={result_id}"  
    )

    time.sleep(10)

    print(
        f"Test Execution completed: "
        f"test_case={test_case_id}, "
        f"result_id={result_id}"
    )

def start_worker() -> None:
    connection = create_connection()

    channel = connection.channel()

    declare_queue(channel)

    print("RabbitMQ worker started")

    def callback(
        ch,
        method,
        properties,
        body
    ):  
        try:
            message = json.loads(body)

            test_case_id = message["test_case_id"]

            result_id = message["result_id"]

            process_test_execution(test_case_id=test_case_id, result_id=result_id)

            ch.basic_ack(delivery_tag=method.delivery_tag)

            print("Job Acknowledged")

        except Exception as exc:
            print(f"Job Failed: {exc}")

            ch.basic_nack(delivery_tag=method.delivery_tag, requeue=True)

    channel.basic_consume(
        queue=RABBITMQ_QUEUE,
        on_message_callback=callback,
        # This is RaabbitMQ considers the message to processed succssfully as soon as it delivers in to the worker.
        # auto_ack=True
        # Using below technique, RabbitMQ will wait for the worker to acknowledge the message
        auto_ack=False
    )

    channel.start_consuming()