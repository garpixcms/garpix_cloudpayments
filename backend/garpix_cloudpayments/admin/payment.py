from django.contrib import admin
from ..models.payment import Payment


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('order_number', 'created_at', 'price', 'status', 'is_test')
    list_filter = ('is_test', 'status')
    search_fields = ('order_number',)
