# Garpix CloudPayments

Прием платажей с CloudPayments.

## Быстрый старт

Установите через pipenv:

```bash
pipenv install garpix_cloudpayments
```

Добавьте `garpix_cloudpayments` в `INSTALLED_APPS` и укажите адрес для миграций:

```python
# settings.py

INSTALLED_APPS += [
    'garpix_cloudpayments',
]
MIGRATION_MODULES = {
    # ...
}
MIGRATION_MODULES['garpix_cloudpayments'] = 'app.migrations.garpix_cloudpayments'
```

Создайте директории и файлы:

```bash
backend/app/migrations/garpix_cloudpayments/
backend/app/migrations/garpix_cloudpayments/__init__.py
```

Сделайте миграции и мигрируйте:

```bash
python3 backend/manage.py makemigrations
python3 backend/manage.py migrate
```

Добавьте пути в `urls.py`:

```python
from django.urls import path, include

urlpatterns = [
    path('cloudpayments/', include('garpix_cloudpayments.urls')),
    # ...
]
```

Также, добавьте в личном кабинете CloudPayments ссылки на эти коллбеки:

* `Pay уведомление` => `https://example.com/cloudpayments/pay/`

* `Fail уведомление` => `https://example.com/cloudpayments/fail/`

После этого необходимо зайти в административную панель и добавить публичный ключ из личного кабинета CloudPayments.

При изменении статуса платежа, дергается функция, указанная в `app/settings.py` (вы можете поменять на свою функцию и указать путь до нее):

```
# app/settings.py

GARPIX_PAYMENT_STATUS_CHANGED_CALLBACK = 'garpix_payment.callbacks.empty_callback'
```

Пример функции:

```python
from garpix_cloudpayments.models.choices import PAYMENT_STATUS_COMPLETED, PAYMENT_STATUS_CANCELLED, PAYMENT_STATUS_DECLINED


def my_callback(payment):
    if payment.status == PAYMENT_STATUS_COMPLETED:
        print('Меняем статус заказа на успешный')
    elif payment.status in (PAYMENT_STATUS_CANCELLED, PAYMENT_STATUS_DECLINED):
        print('Заказ провален')
    else:
        print('Можем тоже использовать')
```

Ниже пример работы на фронтенде (до вызова точки `/cloudpayments/payment_data/` необходимо создать объект модели `Payment`):

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Garpix CloudPayments</title>
    <script src="https://widget.cloudpayments.ru/bundles/cloudpayments"></script>
    <script src="https://cdn.jsdelivr.net/npm/axios/dist/axios.min.js"></script>
</head>
<body>

<label>Номер заказа (payment_uuid):<input type="text" value="1" name="payment_uuid" class="jsPaymentUUID"></label>
<button onclick="getDataAndPay(); return false;">Оплатить</button>

<script>
    function getDataAndPay() {
        var paymentUUID = document.querySelector('.jsPaymentUUID').value;
        axios.get('/cloudpayments/payment_data/?payment_uuid=' + paymentUUID)
            .then(function (paymentData) {
                console.log(paymentData);
                pay(paymentData);
            })
    }


    function pay(paymentData) {
        var widget = new cp.CloudPayments();
        widget.pay('auth', // или 'charge'
            paymentData,
            {
                onSuccess: function (options) { // success
                    //действие при успешной оплате
                    alert('success');
                },
                onFail: function (reason, options) { // fail
                    //действие при неуспешной оплате
                    alert('fail');
                },
                onComplete: function (paymentResult, options) { //Вызывается как только виджет получает от api.cloudpayments ответ с результатом транзакции.
                    //например вызов вашей аналитики Facebook Pixel
                    alert('complete')
                }
            }
        )
    };
</script>
</body>
</html>
```

# Changelog

See [CHANGELOG.md](CHANGELOG.md).

# Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md).

# License

[MIT](LICENSE)

---

Developed by Garpix / [https://garpix.com](https://garpix.com)