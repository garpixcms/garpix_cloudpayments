from garpixcms.settings import *  # noqa

INSTALLED_APPS += [
    'garpix_cloudpayments',
]

MIGRATION_MODULES['garpix_cloudpayments'] = 'app.migrations.garpix_cloudpayments'

GARPIX_PAYMENT_STATUS_CHANGED_CALLBACK = 'garpix_payment.callbacks.empty_callback'
