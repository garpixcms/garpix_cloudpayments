from garpixcms.urls import path, include, urlpatterns
from .views import example_view


urlpatterns += [
    path('', example_view),
    path('example', example_view),
    path('cloudpayments/', include('garpix_cloudpayments.urls')),
]
