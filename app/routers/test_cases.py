from typing import Annotated
from fastapi import Depends, APIRouter, Response, status
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.db.dependencies import (DBSession, get_test_case_service, get_unit_of_work,)
from app.db.models.test_case import TestCase
from app.db.unit_of_work import UnitOfWork
from app.models.test_case import TestCaseCreate, TestCaseResponse, TestCaseUpdate
from app.repositories.test_case import TestCaseRepository
from app.models.test_result import TestResultResponse
from app.services.test_case import TestCaseService

router = APIRouter(prefix="/api", tags=["Test Cases"])

"""
    GET all Test Cases Request
"""
@router.get("/suites/{suite_id}/test_cases", response_model=list[TestCaseResponse])
def get_test_cases(suite_id: int, uow: UnitOfWork = Depends(get_unit_of_work)):
    service = TestCaseService(uow)

    return service.get_test_cases_by_suite(suite_id)

"""
    POST Request
"""
@router.post("/suites/{suite_id}/test_cases", response_model=TestCaseResponse, status_code=status.HTTP_201_CREATED)
def create_test_case(suite_id: int, test_case: TestCaseCreate, uow: UnitOfWork = Depends(get_unit_of_work)):
    service = TestCaseService(uow)

    return service.create_test_case(
        suite_id=suite_id,
        name=test_case.name,
        description=test_case.description,
        priority=test_case.priority.value
    )

"""
    GET Request
"""
@router.get("/test_cases/{test_case_id}", response_model=TestCaseResponse)
def get_test_case(test_case_id: int, uow: UnitOfWork = Depends(get_unit_of_work)):
    service = TestCaseService(uow)

    return service.get_test_case(test_case_id)

"""
    PUT Request
"""
@router.put("/test_cases/{test_case_id}", response_model=TestCaseResponse)
def replace_test_case(test_case_id: int, test_case: TestCaseCreate, uow: UnitOfWork = Depends(get_unit_of_work)):
    service = TestCaseService(uow)

    return service.replace_test_case(
        test_case_id=test_case_id,
        name=test_case.name,
        description=test_case.description,
        priority=test_case.priority.value
    )

"""
    PATCH Request
"""
@router.patch("/test_cases/{test_case_id}", response_model=TestCaseResponse)
def update_test_case(test_case_id: int, test_case: TestCaseUpdate, uow: UnitOfWork = Depends(get_unit_of_work)):
    service = TestCaseService(uow)

    return service.update_test_case(
        test_case_id=test_case_id,
        name=test_case.name,
        description=test_case.description,
        priority=test_case.priority
    )

"""
    DELETE Request
"""
@router.delete("/test_cases/{test_case_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_test_case(test_case_id: int, uow: UnitOfWork = Depends(get_unit_of_work)):
    service = TestCaseService(uow)

    service.delete_test_case(test_case_id)

    return Response(status_code=204)

"""
    POST Execute Request
"""
@router.post("/test_cases/{test_case_id}/execute", response_model=TestCaseResponse)
def execute_test_case(test_case_id: int, uow: UnitOfWork = Depends(get_unit_of_work)):
    service = TestCaseService(uow)

    return service.execute_test_case(test_case_id)