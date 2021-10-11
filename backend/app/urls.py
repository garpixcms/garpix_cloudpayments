from garpixcms.urls import path, include, urlpatterns as _urlpatterns
from .views import example_view


urlpatterns = [
    path('example/', example_view),
    path('cloudpayments/', include('garpix_cloudpayments.urls')),
] + _urlpatterns
