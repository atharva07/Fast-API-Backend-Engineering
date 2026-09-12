from typing import Annotated
from fastapi import Depends, APIRouter, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.db.dependencies import get_db
from app.db.models.test_case import TestCase
from app.models.test_case import TestCaseCreate, TestCaseResponse, TestCaseUpdate

router = APIRouter()
DBSession = Annotated[Session, Depends(get_db)]

# Get Test Cases - GET
@router.get(
    "/",
    response_model=list[TestCaseResponse],
)
def get_test_cases(db: DBSession):
    test_cases = db.execute(
        select(TestCase)
    ).scalars().all()

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
    # Here we create Database object, This creates an SQLAlchemy Object
    db_test_case = TestCase(
        name = test_case.name, 
        description = test_case.description,
        priority = test_case.priority.value,
        status = "DRAFT",
    )

    # This starts tracking the object
    db.add(db_test_case)
    # This flushes the pending changes and commits the transaction
    db.commit()
    # Reloads the object from the database
    db.refresh(db_test_case)

    return db_test_case

# Get Test Case by ID - GET
@router.get(
    "/{test_case_id}",
    response_model=TestCaseResponse,
)
def get_test_case(
    test_case_id: int,
    db: DBSession
):
    test_case = db.execute(
        select(TestCase)
        .where(TestCase.id == test_case_id)
    ).scalar_one_or_none()

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
    db_test_case = db.execute(
        select(TestCase)
        .where(TestCase.id == test_case_id)
    ).scalar_one_or_none()

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
    db_test_case = db.execute(
        select(TestCase)
        .where(TestCase.id == test_case_id)
    ).scalar_one_or_none()

    if db_test_case is None: 
        raise HTTPException(
            status_code=404,
            detail="Test Case Not found",
        )

    db.delete(db_test_case)
    db.commit()
