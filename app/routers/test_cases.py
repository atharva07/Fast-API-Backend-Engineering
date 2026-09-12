from typing import Annotated
from fastapi import Depends, APIRouter, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.db.dependencies import get_db
from app.db.models.test_case import TestCase
from app.models.test_case import TestCaseCreate, TestCaseResponse, TestCaseUpdate
from app.repositories.test_case import TestCaseRepository
from app.models.test_result import TestResultResponse
from app.services.test_case import TestCaseService

router = APIRouter()
DBSession = Annotated[Session, Depends(get_db)]

# Get Test Cases - GET
@router.get(
    "/",
    response_model=list[TestCaseResponse],
)
def get_test_cases(db: DBSession):
    repository = TestCaseRepository(db)

    test_cases = repository.get_all()

    return test_cases

# Create Test Cases - POST
@router.post(
    "/",
    response_model=TestCaseResponse,
    status_code=201
)
def create_test_case(
    test_case: TestCaseCreate,
    db: DBSession
):
    repository = TestCaseRepository(db)
    # Here we create Database object, This creates an SQLAlchemy Object
    test_case = TestCase(
        name = test_case.name, 
        description = test_case.description,
        priority = test_case.priority.value,
        status = "DRAFT",
    )

    # This starts tracking the object
    repository.add(test_case)
    # This flushes the pending changes and commits the transaction
    db.commit()
    # Reloads the object from the database
    db.refresh(test_case)

    return test_case

# Get Test Case by ID - GET
@router.get(
    "/{test_case_id}",
    response_model=TestCaseResponse,
)
def get_test_case(
    test_case_id: int,
    db: DBSession
):
    repository = TestCaseRepository(db)

    test_case = repository.get_by_id(test_case_id)

    if test_case is None:
        raise HTTPException(
            status_code=404,
            detail="Test Case Not Found",
        )
    
    return test_case

# Update Test Case - PATCH / PUT
@router.put(
    "/{test_case_id}",
    response_model=TestCaseResponse
)
def update_test_case(
    test_case_id: int,
    test_case: TestCaseUpdate,
    db: DBSession,
):
    repository = TestCaseRepository(db)

    db_test_case = repository.get_by_id(test_case_id)

    if test_case is None: 
        raise HTTPException(
            status_code=404,
            detail="Test Case not Found",
        )

    update_data = test_case.model_dump(
        exclude_unset=True
    )

    for field, value in update_data.items():
        if hasattr(value, "value"):
            value = value.value

        setattr(
            db_test_case,
            field,
            value,
        )

    db.commit()
    db.refresh(db_test_case)

    return db_test_case

# Delete Test Case - DELETE
@router.delete(
    "/{test_case_id}",
    status_code=204
)
def delete_test_case(
    test_case_id: int,
    db: DBSession
):
    repository = TestCaseRepository(db)
    
    test_case = repository.get_by_id(test_case_id)

    if test_case is None: 
        raise HTTPException(
            status_code=404,
            detail="Test Case Not found",
        )

    repository.delete(test_case)
    db.commit()

@router.post(
    "/{test_case_id}/execute",
    response_model=TestResultResponse,
    status_code=201
)
def execute_test_case(
    test_case_id: int,
    db: DBSession
):
    service = TestCaseService(db)

    return service.execute_test_case(test_case_id)