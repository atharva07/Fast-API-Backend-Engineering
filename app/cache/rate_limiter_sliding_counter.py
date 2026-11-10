import time
import math
from app.cache.redis_client import redis_client
from app.cache.rate_limiter_interface import RateLimitResult    

SLIDING_COUNTER_SCRIPT = """
local key = KEYS[1]

local now_ms = tonumber(ARGV[1])
local window_ms = tonumber(ARGV[2])
local limit = tonumber(ARGV[3])

-- 1. Identify the current time window
local current_window_id = math.floor(now_ms / window_ms)
local elapsed_ms = now_ms % window_ms

-- 2. Read Existing counters
local data = redis.call("HMGET", key,
    "previous_count",
    "current_count",
    "window_id"
)

local previous_count = tonumber(data[1]) or 0
local current_count = tonumber(data[2]) or 0
local stored_window_id = tonumber(data[3])

-- 3. Initialize or update the window counters
if not stored_window_id then
    previous_count = 0
    current_count = 0

elseif current_window_id == stored_window_id + 1 then

    -- We moved forward by exactly one window
    previous_count = current_count
    current_count = 0

elseif current_window_id > stored_window_id + 1 then
    -- We skip one or more windows
    previous_count = 0
    current_count = 0

end

-- 4. Calculate the previous window's contribution
local weight = (window_ms - elapsed_ms) / window_ms

local estimated_count = current_count + (previous_count * weight)

-- 5. Check whether accepting this request exceeds the limit
local projected_count = estimated_count + 1
local allowed = 0

if projected_count <= limit then
    allowed = 1
    current_count = current_count + 1
end

-- 6. Persist the updated counters and window ID
redis.call("HSET", key, 
    "previous_count", previous_count,
    "current_count", current_count,
    "window_id", current_window_id
)

-- 7. Expire inactive rate-limit data
redis.call("PEXPIRE", key, window_ms * 2)

-- 8. Return the result
return {
    allowed,
    tostring(estimated_count), 
    current_count,
    previous_count, 
    tostring(weight)
}
"""

class SlidingWindowCounterRateLimiter:
    def __init__(self, limit: int, window_seconds: int, namespace: str = "default"):
        if limit <= 0:
            raise ValueError("Limit must be greater than zero")

        if window_seconds <= 0:
            raise ValueError("Window must be greater than zero")

        if not namespace.strip():
            raise ValueError("Namespace cannot be empty")

        self.limit = limit
        self.window_seconds = window_seconds
        self.window_ms = window_seconds * 1000
        self.namespace = namespace

        self.script = redis_client.register_script(
            SLIDING_COUNTER_SCRIPT
        )

    def is_allowed(self, identifier: str) -> RateLimitResult:
        key = f"sliding_counter:{self.namespace}:{identifier}"

        now_ms = time.time_ns() // 1_000_000

        (
            allowed,
            estimated_count,
            current_count,
            previous_count,
            weight
        ) = self.script(
            keys=[key],
            args=[
                now_ms,
                self.window_ms,
                self.limit
            ]
        )

        estimated_count = float(estimated_count)
        final_count = estimated_count + 1 if allowed else estimated_count

        return {
            "allowed": bool(allowed),
            "count": final_count,
            "remaining": max(0, math.floor(self.limit - final_count)),
            "retry_after": None,
            "metadata": {
                "current_count": int(current_count),
                "previous_count": int(previous_count),
                "weight": float(weight)
            }
        }