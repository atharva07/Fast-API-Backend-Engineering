from sqlalchemy import select
from app.db.database import SessionLocal
from app.db.models.project import Project
from app.db.models.user import User

db = SessionLocal()

try:
    user = db.execute(
        select(User)
        .where(User.id == 1)
    ).scalar_one()

    project = db.execute(
        select(Project)
        .where(Project.id == 1)
    ).scalar_one()

    print("user: ", user.name)
    print("Projects: ")

    for project in user.projects:
        print("-", project.name)

    print()
    print("Project: ", project.name)
    print("Users: ")

    for user in project.users:
        print("-", user.name)

finally:
    db.close()