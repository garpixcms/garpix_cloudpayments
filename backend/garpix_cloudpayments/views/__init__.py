import json
import importlib
import importlib.util
import logging
from decimal import Decimal
from typing import Optional

from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView
from ..utils import hmac_sha256
from garpix_cloudpayments.models import Config
from garpix_cloudpayments.models.choices import PAYMENT_STATUS_COMPLETED
from garpix_cloudpayments.models.payment import Payment

SUCCESS_CODE = 0
ERROR_CODE = 13


class CloudpaymentView(TemplateView):
    template_name = 'garpix_cloudpayments/cloudpayment_form.html'

    @staticmethod
    def init_callback():
        try:
            callback = importlib.import_module(settings.GARPIX_PAYMENT_STATUS_CHANGED_CALLBACK)
        except Exception as e:
            logging.error(f'При импорте произошла ошибка: GARPIX_PAYMENT_STATUS_CHANGED_CALLBACK. {e}')
            logging.warning('GARPIX_PAYMENT_STATUS_CHANGED_CALLBACK импортирован вручную.')
        return callback

    @staticmethod
    @csrf_exempt
    def payment_data_view(request):
        config = Config.get_solo()
        payment_uuid = request.GET.get('payment_uuid')
        try:
            payment = Payment.objects.get(payment_uuid=payment_uuid)
            return JsonResponse({
                'publicId': config.public_id,
                'description': 'Оплата товара',
                'amount': payment.price,
                'currency': 'RUB',
                'invoiceId': payment.order_number,
                'skin': "mini",
            })
        except Payment.DoesNotExist:
            return JsonResponse({
                'error': 'Does not exist',
            })

    @staticmethod
    @csrf_exempt
    def confirm_view(request) -> Optional[JsonResponse]:
        response_data = CloudpaymentView._get_response_data(request)
        if response_data['code'] == SUCCESS_CODE:
            payment = Payment.objects.get(order_number=response_data['order_number'])
            payment.status = PAYMENT_STATUS_COMPLETED
            payment.save(update_fields=['status'])
            return CloudpaymentView.response_success_0(payment.order_number, "Платеж подтвержден.")

        return CloudpaymentView.response_error_13()

    @staticmethod
    @csrf_exempt
    def pay_view(request) -> Optional[JsonResponse]:
        response_data = CloudpaymentView._get_response_data(request)
        if response_data['code'] == SUCCESS_CODE:
            payment = Payment.objects.get(order_number=response_data['order_number'])

            callback = CloudpaymentView.init_callback()
            callback.callback(payment)

            return CloudpaymentView.response_success_0(payment.order_number, "Платеж проведен.")

        return CloudpaymentView.response_error_13()

    @staticmethod
    @csrf_exempt
    def _default_view(request) -> Optional[JsonResponse]:
        config = Config.get_solo()
        headers = request.headers
        cloud_hmac = headers.get('x-content-hmac')
        post_to_arr = []
        for item in request.POST:
            value = request.POST[item]
            post_to_arr.append(f'{item}={value}')
        hmac_data = '&'.join(post_to_arr)
        local_hmac = hmac_sha256(hmac_data, config.password_api).decode('utf-8')
        request_data = None
        if len(request.POST) > 1:
            request_data = request.POST
        if request_data and len(request_data) > 0 and local_hmac == cloud_hmac:
            try:
                payment = Payment.objects.get(payment_uuid=request_data.get('InvoiceId'))
                payment_price = payment.price
                request_price = Decimal(request_data.get('Amount'))
                if payment_price != request_price:
                    return JsonResponse({
                        "code": 12,
                        "detail": "Неверная сумма. Платеж будет отклонен.",
                        "order_number": payment.order_number
                    })

                payment.status = request_data.get('Status')
                payment.is_test = request_data.get('TestMode') == '1'
                payment.transaction_id = request_data.get('TransactionId', '')
                payment.save()
                return CloudpaymentView.response_success_0(
                    payment.order_number,
                    "Платеж может быть проведен. Система выполнит авторизацию платежа"
                )

            except Payment.DoesNotExist:
                pass

        return CloudpaymentView.response_error_13()

    @classmethod
    @csrf_exempt
    def fail_view(cls, request) -> Optional[JsonResponse]:
        cls._default_view(request)

    @staticmethod
    def _get_response_data(request) -> dict:
        response = CloudpaymentView._default_view(request)
        response_content = json.loads(response.content.decode('utf8'))
        code = response_content.get('code')
        order_number = response_content.get('order_number')

        return {'code': code, 'order_number': order_number}

    @staticmethod
    def response_success_0(order_number: int, detail: str = 'success') -> JsonResponse:
        return JsonResponse({
            "code": SUCCESS_CODE,
            "detail": detail,
            "order_number": order_number
        })

    @staticmethod
    def response_error_13() -> JsonResponse:
        return JsonResponse({
            "code": ERROR_CODE,
            "detail": "Платеж не может быть принят. Платеж будет отклонен.",
            "order_number": None
        })
