from django.urls import path
from .views import confirm_view, pay_view, fail_view, payment_data_view


urlpatterns = [
    path('confirm/', confirm_view, name='cloudpayments_confirm'),
    path('pay/', pay_view, name='cloudpayments_pay'),
    path('fail/', fail_view, name='cloudpayments_fail'),
    path('payment_data/', payment_data_view, name='cloudpayments_payment_data'),
]
