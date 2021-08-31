from django.http import JsonResponse
from ..models.payment import Payment
from decimal import Decimal
from django.conf import settings


def default_view(request):
    if request.method == 'post':
        # print(request.POST)
        try:
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
