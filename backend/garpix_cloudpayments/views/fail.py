from django.views.decorators.csrf import csrf_exempt
from .default_view import default_view


@csrf_exempt
def fail_view(request):
    return default_view(request)
