from sqlalchemy import select
from app.db.database import SessionLocal
from app.db.models.project import Project

db = SessionLocal()

try:
    projects = db.execute(
        select(Project)
    ).scalars().all()

    print("\nProjects:\n")

    for project in projects:
        print(f"Project: {project.name}")

        for test_case in project.test_case:
            print(f"    - {test_case.name}")
finally:
    db.close()

