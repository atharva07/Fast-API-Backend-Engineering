from app.background.rabbitmq_producer import (
    send_test_execution,
)

if __name__ == "__main__":

    # for i in range(1, 7):

    send_test_execution(
        test_case_id=32,
        execution_id=60
    )