from django.urls import path
from .views import confirm_view, pay_view, fail_view, payment_data_view


urlpatterns = [
    path('confirm/', confirm_view),
    path('pay/', pay_view),
    path('fail/', fail_view),
    path('payment_data/', payment_data_view),
]
