from sqlalchemy import select

from app.db.database import SessionLocal
from app.db.models.test_suite import TestSuite


db = SessionLocal()

try:
    suite = db.execute(
        select(TestSuite)
        .limit(1)
    ).scalar_one()

    print("Suite:")
    print(suite.id, suite.name)

    print("\nProject:")
    print(suite.project.id, suite.project.name)

    print("\nTest Cases:")

    for test_case in suite.test_cases:
        print(
            test_case.id,
            test_case.name,
            "suite_id:",
            test_case.suite_id,
        )

finally:
    db.close()