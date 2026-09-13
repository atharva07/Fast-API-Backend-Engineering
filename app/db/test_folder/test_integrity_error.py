from sqlalchemy.exc import IntegrityError
from app.db.database import SessionLocal
from app.db.models.project import Project

db = SessionLocal()

try:
    project1 = Project(
        name="QAForge",
        description="First Project"
    )

    project2 = Project(
        name="QAForge",
        description="Second Project"
    )

    db.add(project1)
    db.add(project2)

    db.commit()

except IntegrityError as exc:
    print("IntegrityError occured!")
    print("Exception:")
    print(exc)

    db.rollback()

finally:
    db.close()