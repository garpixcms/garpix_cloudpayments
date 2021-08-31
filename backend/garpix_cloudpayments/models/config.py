from django.db import models
from .choices import PAYMENT_STATUS_CHOICES, PAYMENT_STATUS_AWAITING_AUTHENTICATION
from solo.models import SingletonModel


class Config(SingletonModel):
    public_id = models.CharField(max_length=200, verbose_name='publicId из личного кабинета CP')

    def __str__(self):
        return 'Настройки CloudPayments'
