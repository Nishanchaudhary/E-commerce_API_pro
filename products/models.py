from django.db import models
from django.utils.text import slugify
from django.utils.crypto import get_random_string

def gen_sku():
    return get_random_string(10).upper()

class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(blank=True, unique=True)
    def save(self,*args,**kwargs):
        if not self.slug: self.slug = slugify(self.name)
        super().save(*args,**kwargs)

class Product(models.Model):
    title = models.CharField(max_length=255)
    image = models.ImageField(upload_to='products/images/', blank=True, null=True)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField(blank=True)
    brand = models.CharField(max_length=100, blank=True)
    category = models.ForeignKey(Category, null=True, blank=True, on_delete=models.SET_NULL)
    vendor = models.ForeignKey('accounts.User', null=True, blank=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)
    def save(self,*args,**kwargs):
        if not self.slug:
            base = slugify(self.title)[:50]
            self.slug = f"{base}-{get_random_string(6)}"
        super().save(*args,**kwargs)

class ProductVariant(models.Model):
    product = models.ForeignKey(Product, related_name='variants', on_delete=models.CASCADE)
    sku = models.CharField(max_length=64, default=gen_sku, unique=True)
    barcode = models.CharField(max_length=128, blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    inventory = models.IntegerField(default=0)
    # attributes = models.JSONField(default=dict)  # e.g. {'size':'M','color':'red'}
    is_active = models.BooleanField(default=True)
    low_stock_threshold = models.IntegerField(default=5)

    def __str__(self):
        return f"{self.product.title} ({self.sku})"
