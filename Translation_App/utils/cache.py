from werkzeug  import SimpleCache
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

cache = SimpleCache()

def get_from_cache(key):
    value = cache.get(key)
    if value:
        logger.info(f"Cache hit for key: {key}")
    else:
        logger.info(f"Cache miss for key: {key}")
    return value

def set_to_cache(key, value, timeout=3600):
    try:
        cache.set(key, value, timeout)
        logger.info(f"Cached key: {key} with timeout: {timeout} seconds")
    except Exception as e:
        logger.error(f"Error caching key {key}: {e}")

def delete_from_cache(key):
    try:
        if cache.delete(key):
            logger.info(f"Deleted cache for key: {key}")
        else:
            logger.info(f"No cache found for key: {key} to delete")
    except Exception as e:
        logger.error(f"Error deleting cache key {key}: {e}")

def clear_all_cache():
    try:
        cache.clear()
        logger.info("Cleared all cache")
    except Exception as e:
        logger.error(f"Error clearing all cache: {e}")
