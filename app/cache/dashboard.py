from app.cache.memory import delete
from app.cache.memory import delete_by_prefix

def invalidate_dashboard(user_id: int):
    cache_key = f"dashboard:{user_id}"
    delete(cache_key)
    print(f"Dashboard cache invalidated: {cache_key}")

def invalidate_all_dashboards():
    delete_by_prefix("dashboard:")
    print("All dashboard caches invalidated")