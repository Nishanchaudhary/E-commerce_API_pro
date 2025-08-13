from django.contrib import admin
from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1
    readonly_fields = ['price']
 
    fields = ['variant', 'qty', 'price', 'vendor']
    show_change_link = True


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = [
        'id', 'user', 'status', 'placed_at',
        'scheduled_for', 'total_amount', 'tracking_number'
    ]
    list_filter = ['status', 'placed_at', 'scheduled_for']
    search_fields = ['user__username', 'tracking_number']
    inlines = [OrderItemInline]
    ordering = ['-placed_at']
    readonly_fields = ['placed_at', 'total_amount']
    fieldsets = (
        ('Order Info', {
            'fields': ('user', 'status', 'placed_at', 'scheduled_for', 'total_amount')
        }),
        ('Delivery Details', {
            'fields': ('tracking_number', 'delivery_otp')
        }),
    )

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user')


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['id', 'order', 'variant', 'qty', 'price', 'vendor']
    search_fields = ['order__id', 'variant__sku', 'vendor__username']
    list_filter = ['vendor']

