from fastapi import APIRouter, Depends
from app.db.dependencies import get_unit_of_work
from app.db.unit_of_work import UnitOfWork
from app.models.test_result import TestResultResponse
from app.services.test_result import TestResultService

router = APIRouter(prefix="/api", tags=["Test Results"])

"""
    GET all Test Results Request
"""
@router.get("/test_cases/{test_case_id}/results")
def get_results(test_case_id: int, uow: UnitOfWork = Depends(get_unit_of_work)):
    service = TestResultService(uow)

    return service.get_results_by_test_case(test_case_id)

@router.get("/results/{result_id}")
def get_result(result_id: int, uow: UnitOfWork = Depends(get_unit_of_work)):
    service = TestResultService(uow)

    return service.get_results(result_id)