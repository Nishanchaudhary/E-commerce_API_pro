from django.contrib import admin
from .models import Category,Product,ProductVariant
# Register your models here.

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}

class ProductVariantInline(admin.TabularInline):
    model = ProductVariant
    extra = 1

class ProductAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'brand']
    inlines = [ProductVariantInline]

admin.site.register(Category,CategoryAdmin)
admin.site.register(Product, ProductAdmin)
