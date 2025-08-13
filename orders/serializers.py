from rest_framework import serializers
from .models import Order,OrderItem
from products.serializers import ProductVariantSerializer

class OrderItemSerializer(serializers.ModelSerializer):
    variant = ProductVariantSerializer(read_only=True)
    class Meta:
        model = OrderItem
        fields = ['id','variant','qty','price','vendor']

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    class Meta:
        model = Order
        fields = ['id','user','status','placed_at','scheduled_for','total_amount','tracking_number','items','delivery_otp']
