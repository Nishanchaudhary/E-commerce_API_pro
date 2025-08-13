from django.contrib import admin
from .models import Payment
# Register your models here.

class PaymentAdmin(admin.ModelAdmin):
    list_display = ['order', 'amount', 'created_at', 'success']
    list_filter = ['order','provider','provider_id']
    search_fields = ['order','provider','provider_id']

admin.site.register(Payment, PaymentAdmin)
