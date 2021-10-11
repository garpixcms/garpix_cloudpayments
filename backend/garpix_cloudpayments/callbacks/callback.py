import logging
from garpix_cloudpayments.models.choices import (
    PAYMENT_STATUS_CANCELLED, PAYMENT_STATUS_DECLINED, PAYMENT_STATUS_AUTHORIZED, PAYMENT_STATUS_COMPLETED
)


def callback(payment) -> int:
    order = None
    # Order.objects.get(pk=payment.order_number)
    # if order is None: raise ValidationError('Заказ на найден. Невозможно оплатить.')

    if payment.status == PAYMENT_STATUS_AUTHORIZED:
        logging.info('Order paid success!')
        # Your a logic via order.paid()
        payment.status = PAYMENT_STATUS_COMPLETED

    elif payment.status in (PAYMENT_STATUS_CANCELLED, PAYMENT_STATUS_DECLINED):
        # Your a logic via  order.cancel()
        logging.warning(f'Заказ: {order} не оплачен: {payment}')

    else:
        logging.error('Произошла непредвиденная ошибка при оплате заказа. Деньги не списаны. Повторите оплату еще раз.')
        logging.warning('PaymentStatus', payment.status)

    payment.save()
    return payment.status
