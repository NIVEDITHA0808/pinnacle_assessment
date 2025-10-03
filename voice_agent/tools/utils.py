"""common utils file"""

from datetime import datetime, timezone, timedelta
 
CACHE = {}
CACHE_TTL = timedelta(minutes=20)

def get_from_cache(cache_key: str):
    """Retrieve from cache if it's not expired"""
    cache_data = CACHE.get(cache_key)
    if not cache_data:
        return None
    
    value, timestamp = cache_data
    
    if datetime.now(timezone.utc) - timestamp < CACHE_TTL:
        return value

    return None

def add_to_cache(key: str, value):
    """Store in cache with current timestamp"""
    CACHE[key] = (value, datetime.now(timezone.utc))
