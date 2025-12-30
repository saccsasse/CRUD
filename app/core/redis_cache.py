import redis
import json


redis_client = redis.Redis(host="localhost", port=6379, db=0, decode_responses=True)

def get_cache(key : str):
    """Retrieve a cached value by key"""
    data = redis_client.get(key)
    if data:
        return json.loads(data)
    return None

def set_cache(key: str, value, ttl: int = 60):
    """Cache a value with a time-to-live (TTL) in seconds"""
    redis_client.setex(key, ttl, json.dumps(value))

def delete_cache(key: str):
    """Invalidate cache manually"""
    redis_client.delete(key)
