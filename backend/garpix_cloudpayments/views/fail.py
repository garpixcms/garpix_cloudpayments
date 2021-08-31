from .default_view import default_view


def fail_view(request):
    return default_view(request)
