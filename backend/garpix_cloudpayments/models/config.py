from django.db import models
from solo.models import SingletonModel


class Config(SingletonModel):
    public_id = models.CharField(max_length=200, verbose_name='publicId из личного кабинета CP')
    password_api = models.CharField(max_length=200, default='', verbose_name='Пароль для API из личного кабинета CP')

    def __str__(self):
        return 'Настройки CloudPayments'
