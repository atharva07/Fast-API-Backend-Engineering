from fastapi import Request, HTTPException, status
from app.cache.rate_limiter import RateLimiter

rate_limiter = RateLimiter(
    limit=3,
    window_seconds=60
)

def rate_limit(request: Request):
    client_ip = request.client.host

    result = rate_limiter.is_allowed(client_ip)

    if not result["allowed"]:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Rate Limit exceeded. Try again later",
            headers={
                "Retry-After": str(result["retry_after"])
            }
        )

    return result