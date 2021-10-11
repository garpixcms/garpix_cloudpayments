from typing import Optional

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from ..models import Payment
from ..service.cloudpayments import SUCCESS_CODE, ServiceCloudpayments


@csrf_exempt
def pay_view(request) -> Optional[JsonResponse]:
    response_data = ServiceCloudpayments(request)._get_response_data()

    if response_data['code'] == SUCCESS_CODE:
        payment = Payment.objects.get(order_number=response_data['order_number'])

        callback = ServiceCloudpayments.init_callback()
        callback.callback(payment)

        return ServiceCloudpayments.response_success_0(payment.order_number, "Платеж проведен.")

    return ServiceCloudpayments.response_error_13()
