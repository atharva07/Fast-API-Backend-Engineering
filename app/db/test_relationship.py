from sqlalchemy import select

from app.db.database import SessionLocal
from app.db.models.project import Project
from app.db.models.test_case import TestCase
from app.db.models.test_result import TestResult

db = SessionLocal()

try:
    # test_case.project.name
    # statement = select(TestCase).where(
    #     TestCase.project_id == 2
    # )

    # result = db.execute(statement)

    # test_cases = result.scalars().all()

    # for test_case in test_cases:
    #     print(
    #         "Test Case:",
    #         test_case.name
    #     )

    #     if test_case.project:
    #         print(
    #             "Project:",
    #             test_case.project.name
    #         )

    # project.test_case
    # statement = select(Project).where(
    #     Project.id == 1
    # )

    # result = db.execute(statement)

    # project = result.scalar_one_or_none()

    # if project:
    #     print("Project:", project.name)

    #     for test_case in project.test_case:
    #         print("Test Case:", test_case.name)

    # Getting test results for a specific test case
    test_case = db.execute(
        select(TestCase)
        .where(TestCase.id == 4)
    ).scalar_one()

    result1 = TestResult(
        test_case = test_case,
        status = "PASSED"
    )

    result2 = TestResult(
        test_case = test_case,
        status = "FAILED"
    )

    db.add_all([result1, result2])
    db.commit()

    print("Created results: ")
    print(result1.id, result1.status)
    print(result2.id, result2.status)

finally:
    db.close()