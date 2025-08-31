from django.core.cache import cache
from .models import Property
import logging
from django_redis import get_redis_connection


logger = logging.getLogger(__name__)


def get_all_properties():
    # Try to get cached queryset
    properties = cache.get('all_properties')
    
    if not properties:
        # Cache miss → fetch from DB
        properties = list(Property.objects.all().values())
        
        # Store in Redis for 1 hour (3600 seconds)
        cache.set('all_properties', properties, 3600)
    
    return properties


def get_redis_cache_metrics():
    """
    Retrieve Redis cache metrics and calculate hit ratio.
    Returns:
        dict: {
            "hits": int,
            "misses": int,
            "hit_ratio": float
        }
    """
    conn = get_redis_connection("default")
    info = conn.info("stats")

    hits = info.get("keyspace_hits", 0)
    misses = info.get("keyspace_misses", 0)

    total = hits + misses
    hit_ratio = (hits / total) if total > 0 else 0.0

    metrics = {
        "hits": hits,
        "misses": misses,
        "hit_ratio": round(hit_ratio, 2),
    }

    logger.info(f"Redis Cache Metrics: {metrics}")

    return metrics
