from django.http import JsonResponse
from ..models.config import Config
from ..models.payment import Payment
from django.views.decorators.csrf import csrf_exempt


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
