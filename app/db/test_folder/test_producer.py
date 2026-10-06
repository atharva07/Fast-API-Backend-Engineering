from app.background.rabbitmq_producer import send_test_execution

if __name__ == "__main__":
    send_test_execution(
        test_case_id=32,
        result_id=52
    )   