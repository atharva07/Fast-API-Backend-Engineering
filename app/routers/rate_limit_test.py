from fastapi import APIRouter, Depends
from app.dependencies.rate_limit import create_rate_limit_dependency

router = APIRouter()

# IP based rate limiting - public endpoint
@router.get("/rate-limit-test")
def test_ip_rate_limit(
    result: dict = Depends(create_rate_limit_dependency(
        algorithm="fixed_window",
        limit=3,
        window_seconds=60,
        namespace="rate_limit_test_ip",
        identifier_type="ip"
    ))
):
    return {
        "messsage": "IP rate limit test successful",
        "rate_limit": result
    }

# User-based rate limiting (authenticated endpoint)
@router.get("/rate-limit-test/user")
def test_user_rate_limit(
    result: dict = Depends(create_rate_limit_dependency(
        algorithm="sliding_log",
        limit=3,
        window_seconds=60,
        namespace="rate_limit_test_user",
        identifier_type="user"
    ))
):
    return {
        "message": "User rate limit test successful",
        "rate_limit": result
    }

# User-based rate limiting (Sliding Counter)
@router.get("/rate-limit-test/user-counter")
def test_user_counter_rate_limit(
    result: dict = Depends(create_rate_limit_dependency(
        algorithm="sliding_counter",
        limit=3,
        window_seconds=60,
        namespace="rate_limit_test_user",
        identifier_type="user"
    ))
):
    return {
        "message": "User Sliding Window Counter test successful",
        "rate_limit": result
    }