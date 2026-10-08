import time
from app.db.database import SessionLocal
from app.db.models.test_result import TestResult

def run_test_case(
    test_case_id: int,
    result_id: int,
) -> None:

    print(
        f"Starting test execution: "
        f"test_case={test_case_id}, result={result_id}")

    time.sleep(10)

    db = SessionLocal()

    try:
        result = db.get(TestResult, result_id)

        if result is None:
            return

        result.status = "PASSED"

        db.commit()

        print(
            f"Test execution completed: "
            f"test_case={test_case_id}, result={result_id}")

    except Exception:
        db.rollback()

        result = db.get(TestResult, result_id)

        if result is not None:
            result.status = "FAILED"
            db.commit()

    finally:
        db.close()