import time
import secrets
from app.cache.redis_client import redis_client
from app.cache.rate_limiter_interface import RateLimitResult

SLIDING_WINDOW_SCRIPT = """
local key = KEYS[1]

local now = tonumber(ARGV[1])
local window_ms = tonumber(ARGV[2])
local limit = tonumber(ARGV[3])
local request_id = ARGV[4]

-- 1. Calculate the cutoff timestamp
local cutoff = now - window_ms

-- 2. Remove requests outside sliding window
redis.call(
    "ZREMRANGEBYSCORE",
    key,
    "-inf",
    cutoff
)

-- 3. Count requests inside the window
local count = redis.call("ZCARD", key)

-- 4. Check whether the limit has been reached
if count >= limit then
    local oldest = redis.call(
        "ZRANGE",
        key,
        0,
        0,
        "WITHSCORES"
    )

    local retry_after = 0

    if #oldest > 0 then
        retry_after = math.ceil(
            (tonumber(oldest[2]) + window_ms - now) / 1000
        )
    end

    return {
        0,
        count, 
        0,
        retry_after
    }
end

-- 5. Add the current request
redis.call(
    "ZADD",
    key,
    now,
    request_id
)

-- 6. Set key expiration
redis.call("PEXPIRE", key, window_ms)

-- 7. Return the result
return {
    1,
    count + 1,
    limit - count - 1,
    0
}
"""

class SlidingWindowRateLimiter:
    def __init__(self, limit: int, window_seconds: int):
        if limit <= 0:
            raise ValueError("Limit must be greater than zero")

        if window_seconds <= 0:
            raise ValueError("Window must be greater than zero")

        self.limit = limit
        self.window_seconds = window_seconds
        self.window_ms = window_seconds * 1000

        self.script = redis_client.register_script(
            SLIDING_WINDOW_SCRIPT
        )

    def is_allowed(self, identifier: str) -> RateLimitResult:
        key = f"sliding_rate_limit:{identifier}"

        now_ms = time.time_ns() // 1_000_000
        request_id = secrets.token_urlsafe(16)

        allowed, count, remaining, retry_after = self.script(
            keys=[key],
            args=[
                now_ms,
                self.window_ms,
                self.limit,
                request_id
            ]
        )

        return {
            "allowed": bool(allowed),
            "count": int(count),
            "remaining": int(remaining), 
            "retry_after": int(retry_after) if not allowed else None,   
            "metadata": {}
        }
        