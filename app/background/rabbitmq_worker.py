import json
import time
from app.background.rabbitmq import create_connection, declare_queue
from app.core.rabbitmq import RABBITMQ_QUEUE
from app.background.rabbitmq_retry import publish_retry
from app.db.database import SessionLocal
from app.repositories.test_result import TestResultRepository

def process_test_execution(test_case_id: int, result_id: int) -> None:
    print(
        f"Executing test case = {test_case_id}, "
        f"result_id={result_id}"  
    )

    if test_case_id == 33:
        raise RuntimeError(
            "Temporary Failure"
        )

    print(
        "Execution Successful"
    )

    time.sleep(10)

    print(
        f"Test Execution completed: "
        f"test_case={test_case_id}, "
        f"result_id={result_id}"
    )

def start_worker(worker_name: str) -> None:
    connection = create_connection()
    channel = connection.channel()
    declare_queue(channel)

    print(f"{worker_name} started")

    MAX_RETRIES = 3

    def callback(
        ch,
        method,
        properties,
        body
    ):  
        db = SessionLocal()

        try:
            message = json.loads(body)
            execution_id = message["execution_id"]
            test_case_id = message["test_case_id"]
            attempts = message.get("attempts",0,)

            repository = TestResultRepository(db)

            result = repository.get_by_id(execution_id)

            if result is None:
                print(
                    f"Execution {execution_id} "
                    f"does not exist"
                )

                ch.basic_ack(delivery_tag=method.delivery_tag)

                return

            if result.status in {
                "PASSED",
                "FAILED",
            }:
                print(
                    f"Execution {execution_id} "
                    f"already completed: "
                    f"{result.status}"
                )   
                ch.basic_ack(delivery_tag=method.delivery_tag)

                return
            
            print(
                f"{worker_name} executing "
                f"execution={execution_id} "
                f"test_case={test_case_id}"
            )

            process_test_execution(test_case_id=test_case_id, result_id=execution_id)

            result.status = "PASSED"

            db.commit()

            print(
                f"Execution {execution_id} "
                f"completed successfully"
            )

            ch.basic_ack(delivery_tag=method.delivery_tag)
            
        except Exception as exc:
            db.rollback()

            print(f"{worker_name} Failed Job: {exc}")

            attempts += 1

            if attempts <= MAX_RETRIES:
                publish_retry(test_case_id=test_case_id, result_id=execution_id, attempts=attempts)
                ch.basic_ack(delivery_tag=method.delivery_tag)
            else:
                print(
                    f"{worker_name}: "
                    f"maximum retries exceeded"
                )

                ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)

        finally:
            db.close()

    channel.basic_qos(
        prefetch_count=1
    )

    channel.basic_consume(
        queue=RABBITMQ_QUEUE,
        on_message_callback=callback,
        # This is RaabbitMQ considers the message to processed succssfully as soon as it delivers in to the worker.
        # auto_ack=True
        # Using below technique, RabbitMQ will wait for the worker to acknowledge the message
        auto_ack=False
    )

    channel.start_consuming()