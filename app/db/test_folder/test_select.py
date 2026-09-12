from sqlalchemy import select
from app.db.database import SessionLocal
from app.db.models.test_case import TestCase

db = SessionLocal()

try:
    statement = select(TestCase).where(
        TestCase.id == 4
    )

    result = db.execute(statement)

    test_case = result.scalar_one_or_none()

    # Test Update
    if test_case is None:
        print("Test case not found")
    else:
        print("Before: ", test_case.status)

        test_case.status = "COMPLETED"

        print("Dirty Object: ", db.dirty)

        db.rollback()

        print("After: ", test_case.status)

    # Test Retrieve
    # for test_case in test_cases:
    #     print(
    #         test_case.id,
    #         test_case.name,
    #         test_case.description,
    #         test_case.priority,
    #         test_case.status
    #     )

    # Test Delete
    # if test_case is None:
    #     print("Test Case not found")
    # else:
    #     print("Deleting: ", test_case.name)
    #     db.delete(test_case)
    #     db.commit()
    #     print("Deleted Successfully")
finally:
    db.close()