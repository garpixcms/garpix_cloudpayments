from garpixcms.settings import *  # noqa

INSTALLED_APPS += [ # noqa F405
    'garpix_cloudpayments',
]

# noqa F405
MIGRATION_MODULES['garpix_cloudpayments'] = 'app.migrations.garpix_cloudpayments'  # noqa F405

GARPIX_PAYMENT_STATUS_CHANGED_CALLBACK = 'garpix_payment.callbacks.empty_callback'
