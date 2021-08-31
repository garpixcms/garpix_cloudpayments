from django.urls import path
from .views.pay import pay_view
from .views.fail import fail_view
from .views.payment_data import payment_data_view

urlpatterns = [
    path('pay/', pay_view),
    path('fail/', fail_view),
    path('payment_data/', payment_data_view),
]
