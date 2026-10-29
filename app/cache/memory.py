"""
    This is python based cache
"""
# cache = {}

# def get(key: str):
#     return cache.get(key)

# def set(key: str, value):
#     cache[key] = value

# def delete(key: str):
#     cache.pop(key, None)

# def delete_by_prefix(prefix: str):
#     keys = [
#         key for key in cache
#         if key.startswith(prefix)
#     ]

#     for key in keys:
#         delete(key)

"""
    This is redis based cache handler
"""
import os
import json
import logging
from typing import Any
from redis.exceptions import RedisError

from app.cache.redis_client import redis_client

logger = logging.getLogger(__name__)

CACHE_TTL_SECONDS = int(os.getenv("CACHE_TTL_SECONDS", "60"))

def get(key: str) -> Any | None:
    try:
        value = redis_client.get(key)
        if value is None:
            return None

        return json.loads(value)
    except (RedisError, ValueError, TypeError):
        logger.exception("Failed to read cache key %s", key)
        return None

def set(key: str, value: Any) -> None:
    try:
        serialize_value = json.dumps(value)
        redis_client.set(key, serialize_value, ex=CACHE_TTL_SECONDS)
    except (RedisError, ValueError, TypeError):
        logger.exception("Failed to write cache key %s", key)

def delete(key: str) -> None:
    try:
        redis_client.delete(key)
    except RedisError:  
        logger.exception("Failed to delete cache key %s", key)

def delete_by_prefix(prefix: str) -> None:
    try:
        keys = redis_client.scan_iter(match=f"{prefix}", count=100)
        for key in keys:
            redis_client.delete(key)
    except:
        logger.exception("Failed to invalidate cache prefix %s", prefix)