from fastapi import Depends, APIRouter, Response, status, BackgroundTasks
from app.background.job import TestExecutionJob
from app.background.queue import job_queue
from app.db.dependencies import get_unit_of_work
from app.db.unit_of_work import UnitOfWork
from app.models.test_case import TestCaseCreate, TestCaseResponse, TestCaseUpdate
from app.models.test_result import TestResultResponse
from app.services.test_case import TestCaseService
from app.security.authorization import require_suite_permission, require_test_case_permission
from app.models.permission import Permission
from app.db.models.user import User
from app.background.rabbitmq_producer import send_test_execution


router = APIRouter(
    prefix="/api", 
    tags=["Test Cases"]
)

"""
    GET all Test Cases Request
"""
@router.get("/suites/{suite_id}/test_cases", response_model=list[TestCaseResponse])
def get_test_cases(suite_id: int,
                    current_user: User = Depends(require_suite_permission(Permission.TEST_CASE_VIEW)),
                    uow: UnitOfWork = Depends(get_unit_of_work)):
    service = TestCaseService(uow)

    return service.get_test_cases_by_suite(suite_id)

"""
    POST Request
"""
@router.post("/suites/{suite_id}/test_cases", response_model=TestCaseResponse, status_code=status.HTTP_201_CREATED)
def create_test_case(suite_id: int, test_case: TestCaseCreate,
                    current_user = Depends(require_suite_permission(Permission.TEST_CASE_CREATE)), 
                    uow: UnitOfWork = Depends(get_unit_of_work)):
    service = TestCaseService(uow)

    return service.create_test_case(
        suite_id=suite_id,
        name=test_case.name,
        description=test_case.description,
        priority=test_case.priority.value
    )

"""
    Individual Test Case GET Request
"""
@router.get("/test_cases/{test_case_id}", response_model=TestCaseResponse)
def get_test_case(test_case_id: int, 
                  current_user: User = Depends(require_test_case_permission(Permission.TEST_CASE_VIEW)),
                  uow: UnitOfWork = Depends(get_unit_of_work)):
    service = TestCaseService(uow)

    return service.get_test_case(test_case_id)

"""
    PUT Request
"""
@router.put("/test_cases/{test_case_id}", response_model=TestCaseResponse)
def replace_test_case(test_case_id: int, test_case: TestCaseCreate,
                    current_user: User = Depends(require_test_case_permission(Permission.TEST_CASE_UPDATE)),
                    uow: UnitOfWork = Depends(get_unit_of_work)):
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
def update_test_case(test_case_id: int, test_case: TestCaseUpdate,
                    current_user: User = Depends(require_test_case_permission(Permission.TEST_CASE_UPDATE)), 
                    uow: UnitOfWork = Depends(get_unit_of_work)):
    service = TestCaseService(uow)

    return service.update_test_case(
        test_case_id=test_case_id,
        name=test_case.name,
        description=test_case.description,
        priority=test_case.priority,
        status=test_case.status
    )

"""
    DELETE Request
"""
@router.delete("/test_cases/{test_case_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_test_case(test_case_id: int, 
                    current_user: User = Depends(require_test_case_permission(Permission.TEST_CASE_DELETE)),
                    uow: UnitOfWork = Depends(get_unit_of_work)):
    service = TestCaseService(uow)

    service.delete_test_case(test_case_id)

    return Response(status_code=204)

"""
    POST Execute Request
"""
@router.post("/test_cases/{test_case_id}/execute", response_model=TestResultResponse, status_code=status.HTTP_202_ACCEPTED)
def execute_test_case(test_case_id: int, uow: UnitOfWork = Depends(get_unit_of_work)):
    service = TestCaseService(uow)

    result = service.execute_test_case(test_case_id)

    print(
        f"Publishing execution {result.id} "
        f"to RabbitMQ"
    )

    # send_test_execution(
    #     test_case_id=test_case_id,
    #     execution_id=result.id
    # )

    return result