from django.db import models
from .choices import PAYMENT_STATUS_CHOICES, PAYMENT_STATUS_AWAITING_AUTHENTICATION
import uuid


def generate_uuid():
    return uuid.uuid4().hex


class Payment(models.Model):
    payment_uuid = models.CharField(max_length=64, verbose_name='UUID', default=generate_uuid)
    order_number = models.CharField(max_length=200, verbose_name='Номер заказа')
    transaction_id = models.CharField(max_length=200, default='', blank=True, verbose_name='Номер транзакции')
    price = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='Сумма платежа')
    status = models.CharField(max_length=100, default=PAYMENT_STATUS_AWAITING_AUTHENTICATION, choices=PAYMENT_STATUS_CHOICES, verbose_name='Статус')
    is_test = models.BooleanField(default=False, verbose_name='Тестовый платеж')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    def __str__(self):
        return f'{self.order_number} ({self.price}) - {self.status}'
