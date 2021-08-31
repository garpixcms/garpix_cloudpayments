from garpixcms.urls import *  # noqa
from .views import example_view

urlpatterns = [
    path('', example_view),
    path('cloudpayments/', include('garpix_cloudpayments.urls')),
] + urlpatterns  # noqa
