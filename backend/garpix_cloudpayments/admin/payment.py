from django.contrib import admin
from django.http import HttpResponse
from django.template import loader
from garpix_cloudpayments.models import Payment


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    actions = ('show_demo_form', )
    date_hierarchy = 'created_at'
    list_display = ('order_number', 'created_at', 'price', 'status', 'payment_uuid', 'is_test')
    list_filter = ('is_test', 'status', 'created_at')
    search_fields = ('order_number', )

    def pay_by_demo_form(self, request, queryset):
        payment = queryset.first()
        t = loader.get_template(Payment.template_name)
        c = {'payment_uuid': payment.payment_uuid}
        return HttpResponse(t.render(c, request))
    pay_by_demo_form.short_description = 'Оплатить с помощью формы (1 платежка)'
