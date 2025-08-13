from django.contrib import admin
from .models import Cart, CartItem
# Register your models here.

class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 1

class CartAdmin(admin.ModelAdmin):
    list_display = ['user', 'session_key', 'created_at']
    inlines = [CartItemInline]

admin.site.register(Cart, CartAdmin)
