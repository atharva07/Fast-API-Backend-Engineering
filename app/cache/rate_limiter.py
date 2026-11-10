from app.cache.redis_client import redis_client
from app.cache.rate_limiter_interface import RateLimitResult

RATE_LIMIT_SCRIPT = """
local current = redis.call("INCR", KEYS[1])

if current == 1 then
    redis.call("EXPIRE", KEYS[1], ARGV[1])
end

local ttl = redis.call("TTL", KEYS[1])

return {current, ttl}
"""

"""
    In our example we will have limit = 3 and window_seconds = 60. 
    This means we will have maximum 3 requests with 60-seconds window
    After the window expires, a new counter starts
"""

class RateLimiter:
    def __init__(self, limit: int, window_seconds: int, namespace: str = "default"):
        if limit <= 0:
            raise ValueError("Limit must be greater that zero")

        if window_seconds <= 0:
            raise ValueError("Window must be greater than zero")

        if not namespace.strip():
            raise ValueError("Namespace cannot be empty")

        self.limit = limit
        self.window_seconds = window_seconds
        self.namespace = namespace

        self.script = redis_client.register_script(
            RATE_LIMIT_SCRIPT
        )

    def is_allowed(self, identifier: str) -> RateLimitResult:
        key = f"rate_limit:{self.namespace}:{identifier}"

        count, ttl = self.script(
            keys=[key],
            args=[self.window_seconds]
        )

        allowed = count <= self.limit

        return {
            "allowed": allowed,
            "count": count,
            "remaining": max(0, self.limit - count),
            "retry_after": max(0, ttl) if not allowed else None,
            "metadata": {}
        }