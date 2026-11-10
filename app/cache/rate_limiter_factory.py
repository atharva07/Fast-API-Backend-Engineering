from app.cache.rate_limiter_interface import RateLimiterProtocol
from app.cache.rate_limiter_registry import RATE_LIMITER_REGISTRY

def create_rate_limiter(
    algorithm: str,
    limit: int,
    window_seconds: int,
    namespace: str = "default"
) -> RateLimiterProtocol:
    limiter_class = RATE_LIMITER_REGISTRY.get(algorithm)

    if limiter_class is None:
        raise ValueError(
            f"Unsupported rate limiting algorithm: {algorithm}"
        )

    return limiter_class(
        limit=limit,
        window_seconds=window_seconds,
        namespace=namespace
    )