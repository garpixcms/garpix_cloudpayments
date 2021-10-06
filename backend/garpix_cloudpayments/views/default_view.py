import json
from decimal import Decimal
from typing import Optional

from django.core.exceptions import ValidationError
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from garpix_cloudpayments.models.payment import Payment
from garpix_cloudpayments.service import ServiceCloudpayments


@csrf_exempt
def default_view(request) -> Optional[JsonResponse]:
    if len(request.POST) > 1:
        request_data = request.POST
    elif request.body:
        request_data = json.loads(request.body.decode("utf-8"))
    else:
        raise ValidationError('Не полученны данные из запроса. (request.POST or request.body)')

    if request_data and len(request_data) > 0:
        payment = Payment.objects.get(order_number=request_data.get('InvoiceId'))
        payment.status = request_data.get('Status')
        payment.is_test = request_data.get('TestMode') == '1'
        payment.transaction_id = request_data.get('TransactionId', '')

        if payment.price != Decimal(request_data.get('Amount')):
            return JsonResponse({
                "code": 12,
                "detail": "Неверная сумма. Платеж будет отклонен.",
                "order_number": payment.order_number
            })

        payment.save()

        return ServiceCloudpayments.response_success_0(
            payment.order_number,
            "Платеж может быть проведен. Система выполнит авторизацию платежа"
        )

    return ServiceCloudpayments.response_error_13()
