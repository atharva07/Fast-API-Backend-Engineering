from sqlalchemy import select

from app.db.database import SessionLocal
from app.db.models.test_suite import TestSuite


db = SessionLocal()

try:
    suites = db.execute(
        select(TestSuite)
    ).scalars().all()

    print("Test suites:", suites)

finally:
    db.close()