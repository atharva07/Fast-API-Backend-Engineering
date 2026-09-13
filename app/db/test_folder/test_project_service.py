from app.db.database import SessionLocal
from app.db.unit_of_work import UnitOfWork
from app.services.project import ProjectService
from app.exceptions.project import ProjectAlreadyExistsError

db = SessionLocal()

try:
    uow = UnitOfWork(db)

    service = ProjectService(uow)

    service.create_project(
        name="QAForge",
        description="Duplicate project",
    )

except ProjectAlreadyExistsError as exc:
    print("Application exception:")
    print(exc)

finally:
    db.close()