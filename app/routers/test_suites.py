from fastapi import APIRouter, Depends, Response, status
from app.db.dependencies import get_unit_of_work
from app.db.unit_of_work import UnitOfWork
from app.models.test_suite import (
    TestSuiteCreate,
    TestSuiteResponse,
    TestSuiteUpdate,
)
from app.services.test_suite import TestSuiteService

router = APIRouter(prefix="/api", tags=["Test Suites"])

@router.post("/projects/{project_id}/suites", response_model=TestSuiteResponse, status_code=status.HTTP_201_CREATED)
def create_suite(project_id: int, suite: TestSuiteCreate, uow: UnitOfWork = Depends(get_unit_of_work)):
    service = TestSuiteService(uow)

    return service.create_suite(
        project_id=project_id,
        name=suite.name,
        description=suite.description
    )

@router.get("/projects/{project_id}/suites", response_model=list[TestSuiteResponse])
def get_suites(project_id: int, uow: UnitOfWork = Depends(get_unit_of_work)):
    service = TestSuiteService(uow)

    return service.get_suites(project_id)

@router.get("/suites/{suite_id}", response_model=TestSuiteResponse)
def get_suite(suite_id: int, uow: UnitOfWork = Depends(get_unit_of_work)):
    service = TestSuiteService(uow)

    return service.get_suite(suite_id)

@router.put("/suites/{suite_id}", response_model=TestSuiteResponse)
def replace_suite(suite_id: int, suite: TestSuiteCreate, uow: UnitOfWork = Depends(get_unit_of_work)):
    service = TestSuiteService(uow)

    return service.replace_suite(
        suite_id=suite_id,
        name=suite.name,
        description=suite.description
    )

@router.patch("/suites/{suite_id}", response_model=TestSuiteResponse)
def update_suite(suite_id: int, suite: TestSuiteUpdate, uow: UnitOfWork = Depends(get_unit_of_work)):
    service = TestSuiteService(uow)

    return service.update_suite(
        suite_id=suite_id,
        name=suite.name,
        description=suite.description
    )

@router.delete("/suites/{suite_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_suite(suite_id: int, uow: UnitOfWork = Depends(get_unit_of_work)):
    service = TestSuiteService(uow)

    service.delete_suite(suite_id)

    return Response(status_code=204)