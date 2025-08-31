# alx_backend_caching_property_listings

A Django project demonstrating **caching with Redis** for property
listings.\
It showcases how to optimize database queries, invalidate caches using
signals, and monitor cache efficiency via Redis metrics.

------------------------------------------------------------------------

## ✨ Features

-   **Property Listings API**: List properties via `/properties/`
    endpoint.
-   **Optimized Querying**: Caches the queryset of properties in Redis
    for 1 hour.
-   **Cache Invalidation**: Automatically clears the Redis cache on
    property create/update/delete using Django signals.
-   **Redis Metrics**: Tracks `keyspace_hits`, `keyspace_misses`, and
    computes cache hit ratio.
-   **Safe API Access**: Uses Django's `@require_GET` decorator for
    GET-only access.
-   **Modular Utilities**: Encapsulated caching and metrics logic in
    `properties/utils.py`.

------------------------------------------------------------------------

## 🛠️ Tech Stack

-   **Backend**: Django (Python)
-   **Database**: SQLite (default for dev; replaceable with
    Postgres/MySQL)
-   **Caching**: Redis via `django-redis`
-   **API**: Django REST Framework (optional for expansion)
-   **Logging**: Python's standard logging for cache metrics

------------------------------------------------------------------------

## 📂 Project Structure

    manage.py
    alx_backend_caching_property_listings/
        ├── settings.py
        ├── urls.py
        ├── wsgi.py
        └── asgi.py
    
    properties/                    # Main app for property listings
        ├── models.py              # Property model
        ├── views.py               # property_list view with caching
        ├── utils.py               # get_all_properties & get_redis_cache_metrics
        ├── signals.py             # Cache invalidation signals
        ├── apps.py                # Loads signals at startup
        └── __init__.py            # Default app config

------------------------------------------------------------------------

## 🚀 API Endpoints

### Get all properties

**Endpoint:** `GET /properties/`\
**View:** `property_list` in `properties/views.py`\
**Caching:** Uses `get_all_properties()` → Redis (`all_properties` key,
expires in 1 hour).

Example response:

``` json
{
  "data": [
    {
      "id": 1,
      "title": "2-Bedroom Apartment",
      "price": 100000,
      "location": "Lagos"
    },
    ...
  ]
}
```

------------------------------------------------------------------------

## 🔄 Caching Workflow

1.  **Query Check**: `get_all_properties()` checks Redis
    (`cache.get('all_properties')`).\
2.  **Miss Handling**: If not found, fetches `Property.objects.all()`.\
3.  **Store**: Saves queryset in Redis with a 1-hour TTL
    (`cache.set(..., 3600)`).\
4.  **Invalidate**: On `post_save` or `post_delete`, signals clear the
    Redis cache.

------------------------------------------------------------------------

## 📊 Redis Cache Metrics

`properties/utils.py` contains:

``` python
def get_redis_cache_metrics():
    client = get_redis_connection("default")
    info = client.info("stats")
    hits = info.get("keyspace_hits", 0)
    misses = info.get("keyspace_misses", 0)
    total_requests = hits + misses
    hit_ratio = hits / total_requests if total_requests > 0 else 0

    logger.info("Redis cache metrics: hits=%d, misses=%d, ratio=%.2f",
                hits, misses, hit_ratio)
    return {
        "hits": hits,
        "misses": misses,
        "hit_ratio": hit_ratio,
    }
```

-   ✅ Logs metrics with `logger.info`\
-   ✅ Gracefully handles zero requests
    (`if total_requests > 0 else 0`)\
-   ✅ Returns structured dictionary of metrics

------------------------------------------------------------------------

## ⚡ Setup Instructions

### 1. Clone Repo

``` bash
git clone https://github.com/loutimi/alx_backend_caching_property_listings.git
cd alx_backend_caching_property_listings
```

### 2. Install Dependencies

``` bash
pip install -r requirements.txt
```

### 3. Setup Redis

Ensure Redis is running locally:

``` bash
redis-server
```

### 4. Run Migrations

``` bash
python manage.py migrate
```

### 5. Start Server

``` bash
python manage.py runserver
```

Visit <http://localhost:8000/properties/>.

------------------------------------------------------------------------

## ✅ Validation Notes

-   `property_list` returns JSON with a `data` key →
    `JsonResponse({"data": ...})`.\
-   Metrics function uses:
    -   `if total_requests > 0 else 0` for hit ratio.\
    -   `logger.info(...)` for logging cache stats.\
-   Signals correctly delete Redis key `all_properties` on changes.

------------------------------------------------------------------------

## 📌 Author

**Rotimi Musa**\
ALX Backend Specialization -- Caching Property Listings
