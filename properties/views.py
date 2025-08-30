from django.http import JsonResponse
from django.views.decorators.http import require_GET
from .utils import get_all_properties

@require_GET
def property_list(request):
    properties = get_all_properties()
    return JsonResponse({"data": properties})
