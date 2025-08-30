from django.http import JsonResponse
from django.views.decorators.cache import cache_page
from django.views.decorators.http import require_GET
from .models import Property

@require_GET
@cache_page(60 * 15)  # cache for 15 minutes
def property_list(request):
    properties = list(Property.objects.values())
    return JsonResponse({
        "data": properties
    })
