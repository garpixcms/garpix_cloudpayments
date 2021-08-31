from django.http import JsonResponse
from ..models.config import Config
from ..models.payment import Payment


def payment_data_view(request):
    config = Config.get_solo()
    order_number = request.GET.get('order_number')
    try:
        payment = Payment.objects.get(order_number=order_number)
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
