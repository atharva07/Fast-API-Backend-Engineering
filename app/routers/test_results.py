from fastapi import APIRouter, Depends, Query
from app.db.dependencies import get_unit_of_work
from app.db.unit_of_work import UnitOfWork
from app.services.test_result import TestResultService
from app.models.test_result import PaginatedTestResultRespones

router = APIRouter(prefix="/api", tags=["Test Results"])

"""
    GET all Test Results Request
"""
@router.get("/test_cases/{test_case_id}/results")
def get_results(test_case_id: int, uow: UnitOfWork = Depends(get_unit_of_work)):
    service = TestResultService(uow)

    return service.get_results_by_test_case(test_case_id)

"""
    GET Request
"""
@router.get("/results/{result_id}")
def get_result(result_id: int, uow: UnitOfWork = Depends(get_unit_of_work)):
    service = TestResultService(uow)

    return service.get_results(result_id)

# """
#     GET Request - All Test Results across all test cases
# """
# @router.get("/results")
# def get_all_results(uow: UnitOfWork = Depends(get_unit_of_work)):
#     service = TestResultService(uow)

#     return service.get_all_results()

"""
    Implementing pagination
"""
@router.get("/results", response_model=PaginatedTestResultRespones)
def get_paginated_results(page: int = Query(default=1, ge=1), page_size: int = Query(default=10, ge=1,le=100), uow: UnitOfWork = Depends(get_unit_of_work)):
    service = TestResultService(uow)

    return service.get_results_page(
        page = page,
        page_size = page_size
    )