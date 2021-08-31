PAYMENT_STATUS_AWAITING_AUTHENTICATION = 'AwaitingAuthentication'
PAYMENT_STATUS_AUTHORIZED = 'Authorized'
PAYMENT_STATUS_COMPLETED = 'Completed'
PAYMENT_STATUS_CANCELLED = 'Cancelled'
PAYMENT_STATUS_DECLINED = 'Declined'

PAYMENT_STATUS_CHOICES = (
    (PAYMENT_STATUS_AWAITING_AUTHENTICATION, 'Ожидает аутентификации'),
    (PAYMENT_STATUS_AUTHORIZED, 'Авторизована'),
    (PAYMENT_STATUS_COMPLETED, 'Завершена'),
    (PAYMENT_STATUS_CANCELLED, 'Отменена'),
    (PAYMENT_STATUS_DECLINED, 'Отклонена'),
)
