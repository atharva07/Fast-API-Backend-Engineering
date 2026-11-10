from fastapi import Request, HTTPException, status, Depends
from app.cache.rate_limiter_factory import create_rate_limiter
from app.security.dependencies import get_current_user

def create_rate_limit_dependency(
    algorithm: str,
    limit: int,
    window_seconds: int,
    namespace: str,
    identifier_type: str = "ip"
):
    if identifier_type not in ("ip", "user"):
        raise ValueError(
            "identifier_type must be either 'ip' or 'user'"
        )

    limiter = create_rate_limiter(
        algorithm=algorithm,
        limit=limit,
        window_seconds=window_seconds,
        namespace=namespace
    )

    def rate_limit(
        request: Request,
        current_user=Depends(get_current_user)
        if identifier_type == "user"
        else None
    ):  
        # This is user based block
        if identifier_type == "user":
            identifier = f"user:{current_user.id}"
        else:
            # This is IP based block
            if request.client is None:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Unable to identify Client"
                )

            # This is will return the IP
            identifier = request.client.host

        result = limiter.is_allowed(identifier)

        if not result["allowed"]:
            headers = {}

            if result["retry_after"] is not None:
                headers["Retry-After"] = str(result["retry_after"])

            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail="Rate limit exceeded. Try again later",
                headers=headers
            )

        return result

    return rate_limit