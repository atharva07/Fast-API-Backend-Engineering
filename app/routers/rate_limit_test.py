from fastapi import APIRouter, Depends
from app.dependencies.rate_limit import rate_limit

router = APIRouter()

@router.get("/rate-limit-test")
def test_rate_limit(
    result: dict = Depends(rate_limit)
):
    return {
        "messsage": "Request successful",
        "rate_limit": result
    }