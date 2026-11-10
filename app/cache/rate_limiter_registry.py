from app.cache.rate_limiter import RateLimiter
from app.cache.rate_limiter_sliding_window import SlidingWindowRateLimiter
from app.cache.rate_limiter_sliding_counter import SlidingWindowCounterRateLimiter

RATE_LIMITER_REGISTRY = {
    "fixed_window": RateLimiter,
    "sliding_log": SlidingWindowRateLimiter,
    "sliding_counter": SlidingWindowCounterRateLimiter
}