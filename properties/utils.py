from django.core.cache import cache
from .models import Property

def get_all_properties():
    # Try to get cached queryset
    properties = cache.get('all_properties')
    
    if not properties:
        # Cache miss → fetch from DB
        properties = list(Property.objects.all().values())
        
        # Store in Redis for 1 hour (3600 seconds)
        cache.set('all_properties', properties, 3600)
    
    return properties
