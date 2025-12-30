#Redis is used for caching - for ex when we run for the first time get list of items
#programm will grab info from database, but when we will run it for the second time
#thanls to the Redis it will grab directly from cache without calling database again

import redis
import json

#Connect to local Redis
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
