from django.contrib import admin
from ..models.payment import Payment


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    date_hierarchy = 'created_at'
    list_display = ('order_number', 'created_at', 'price', 'status', 'payment_uuid', 'is_test')
    list_filter = ('is_test', 'status', 'created_at')
    search_fields = ('order_number', )
