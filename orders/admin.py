from django.contrib import admin
from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ['get_total']
    fields = ['variant', 'quantity', 'price', 'get_total']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'full_name', 'email', 'status', 'total_amount', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['full_name', 'email', 'razorpay_order_id']
    readonly_fields = ['razorpay_order_id', 'razorpay_payment_id', 'created_at']
    inlines = [OrderItemInline]
    fieldsets = (
        ('Customer Information', {
            'fields': ('full_name', 'email', 'phone', 'address', 'city', 'state', 'pincode')
        }),
        ('Order Details', {
            'fields': ('status', 'total_amount', 'created_at')
        }),
        ('Payment Information', {
            'fields': ('razorpay_order_id', 'razorpay_payment_id')
        }),
    )


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['order', 'variant', 'quantity', 'price']
    list_filter = ['order__created_at']
    search_fields = ['order__id', 'variant__product__name']
    readonly_fields = ['get_total']
