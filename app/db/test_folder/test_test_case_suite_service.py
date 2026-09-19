from sqlalchemy import select

from app.db.database import SessionLocal
from app.db.models.test_suite import TestSuite
from app.db.unit_of_work import UnitOfWork
from app.services.test_case import TestCaseService


db = SessionLocal()

try:

    uow = UnitOfWork(db)
    service = TestCaseService(uow)

    suite = db.execute(
        select(TestSuite)
    ).scalars().first()

    if suite is None:
        raise RuntimeError(
            "No test suite exists"
        )

    print("Using suite:")
    print(suite.id, suite.name)

    # -----------------------------
    # Create
    # -----------------------------

    test_case = service.create_test_case(
        suite_id=suite.id,
        name="Repository Architecture Test",
        description="Testing suite-based test case",
        priority="HIGH",
    )

    print("\nCreated test case:")
    print(
        test_case.id,
        test_case.name,
        test_case.suite_id,
    )

    # -----------------------------
    # Get by suite
    # -----------------------------

    test_cases = service.get_test_cases_by_suite(
        suite.id
    )

    print("\nTest cases in suite:")

    for item in test_cases:
        print(
            item.id,
            item.name,
            item.suite_id,
        )

finally:
    db.close()