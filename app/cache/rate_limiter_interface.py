from typing import Protocol, TypedDict

class RateLimitResult(TypedDict):
    allowed: bool
    count: int | float
    remaining: int
    retry_after: int | None
    metadata: dict

class RateLimiterProtocol(Protocol):
    def is_allowed(self, identifier: str) -> RateLimitResult:
        ...