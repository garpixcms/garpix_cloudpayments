from django.http import JsonResponse
from ..models.payment import Payment
from decimal import Decimal
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from ..utils import hmac_sha256
from garpix_cloudpayments.models import Config


@csrf_exempt
def default_view(request):
    if request.method == 'POST':
        headers = request.headers
        try:
            config = Config.get_solo()
            cloud_hmac = headers.get('X-Content-Hmac')
            hmac_data = request.body.decode('utf-8')
            local_hmac = hmac_sha256(hmac_data, config.password_api).decode('utf-8')
            if local_hmac != cloud_hmac:
                return JsonResponse({"code": 13})
            payment = Payment.objects.get(order_number=request.POST.get('InvoiceId'))
            payment.status = request.POST.get('Status')
            payment.is_test = request.POST.get('TestMode') == '1'
            payment.transaction_id = request.POST.get('TransactionId')
            if payment.price != Decimal(request.POST.get('Amount')):
                raise Exception('Wrong price')
            payment.save()
            callback = __import__(settings.GARPIX_PAYMENT_STATUS_CHANGED_CALLBACK)
            callback(payment)
        except Payment.DoesNotExist:
            return JsonResponse({"code": 1})
        except Exception:
            return JsonResponse({"code": 2})
    return JsonResponse({"code": 0})
