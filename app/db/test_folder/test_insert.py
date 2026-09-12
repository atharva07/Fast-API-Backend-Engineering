from app.db.database import SessionLocal
from app.db.models.test_case import TestCase

db = SessionLocal()

try:
    test_case = TestCase(
        name="SQLAlchemy Login Test",
        description="Created using SQLAlchemy",
        priority="HIGH",
        status="DRAFT",
        project_id=1
    )

    db.add(test_case)

    db.commit()

    print("Test case Created")

    print("ID:", test_case.id)

finally:
    db.close()