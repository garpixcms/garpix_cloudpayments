from .default_view import default_view
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def fail_view(request):
    return default_view(request)
