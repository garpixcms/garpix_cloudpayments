from typing import Optional

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from garpix_cloudpayments.models.choices import PAYMENT_STATUS_COMPLETED
from garpix_cloudpayments.models.payment import Payment
from garpix_cloudpayments.service import ServiceCloudpayments


SUCCESS_CODE = 0
ERROR_CODE = 13


@csrf_exempt
def confirm_view(request) -> Optional[JsonResponse]:
    response_data = ServiceCloudpayments(request)._get_response_data()

    if response_data['code'] == SUCCESS_CODE:
        payment = Payment.objects.get(order_number=response_data['order_number'])
        payment.status = PAYMENT_STATUS_COMPLETED
        payment.save(update_fields=['status'])
        return ServiceCloudpayments.response_success_0(payment.order_number, "Платеж подтвержден.")

    return ServiceCloudpayments.response_error_13()
