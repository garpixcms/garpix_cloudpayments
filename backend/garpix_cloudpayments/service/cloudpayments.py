import importlib
import importlib.util
import json
import logging

from django.conf import settings
from django.http import JsonResponse


SUCCESS_CODE = 0
ERROR_CODE = 13


class ServiceCloudpayments:

    def __init__(self, request):
        self.request = request

    @staticmethod
    def init_callback():
        try:
            callback = importlib.import_module(settings.GARPIX_PAYMENT_STATUS_CHANGED_CALLBACK)
        except Exception as e:
            callback = 'undefined'
            logging.error(f'При импорте произошла ошибка: GARPIX_PAYMENT_STATUS_CHANGED_CALLBACK. {e}')
            logging.warning('GARPIX_PAYMENT_STATUS_CHANGED_CALLBACK импортирован вручную.')

        return callback

    def _get_response_data(self) -> dict:
        from garpix_cloudpayments.views.default_view import default_view  # troubles with import
        response = default_view(self.request)
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
