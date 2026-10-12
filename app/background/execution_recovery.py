import time
from app.db.database import SessionLocal
from app.repositories.test_result import TestResultRepository
from app.background.rabbitmq_producer import send_test_execution

def recover_stuck_executions() -> None:
    db = SessionLocal()

    try:
        repository = TestResultRepository(db)

        results = repository.reset_stuck_execution()

        for result in results:
            send_test_execution(
                test_case_id=result.test_case_id,
                execution_id=result.id
            )

            print(f"Requeued execution {result.id}")

    finally:
        db.close()

def start_execution_recovery() -> None:
    print("Execution recovery started")

    while True:
        try:
            recover_stuck_executions()

        except Exception as exc:
            print(
                f"Execution recovery failed: {exc}"
            )

        time.sleep(30)