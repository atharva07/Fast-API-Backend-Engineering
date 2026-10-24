cache = {}

def get(key: str):
    return cache.get(key)

def set(key: str, value):
    cache[key] = value

def delete(key: str):
    cache.pop(key, None)

def delete_by_prefix(prefix: str):
    keys = [
        key for key in cache
        if key.startswith(prefix)
    ]

    for key in keys:
        delete(key)