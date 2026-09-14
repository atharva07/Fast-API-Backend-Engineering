from sqlalchemy.exc import IntegrityError

from app.db.database import SessionLocal
from app.db.models.test_case import TestCase

db = SessionLocal()

try:
    test_case = TestCase(
        name="Invalid Project Test",
        description="Testing foreign key violation",
        priority="MEDIUM",
        status="DRAFT",
        project_id=999999,
    )

    db.add(test_case)

    db.commit()

except IntegrityError as exc:
    print("IntegrityError occurred!")

    print("Original error:")
    print(exc.orig)

    print("SQLSTATE:")
    print(exc.orig.sqlstate)

    db.rollback()

finally:
    db.close()