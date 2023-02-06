from django.urls import path
from .views import CloudpaymentView
# from .views.pay import pay_view
# from .views.fail import fail_view
# from .views.payment_data import payment_data_view

urlpatterns = [
    path('pay/', CloudpaymentView.pay_view),
    path('fail/', CloudpaymentView.fail_view),
    path('payment_data/', CloudpaymentView.payment_data_view),
]
