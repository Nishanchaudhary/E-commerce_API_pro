from rest_framework import serializers

from products.models import ProductVariant
from .models import Cart,CartItem
from products.serializers import ProductVariantSerializer

class CartItemSerializer(serializers.ModelSerializer):
    variant = ProductVariantSerializer(read_only=True)
    variant_id = serializers.PrimaryKeyRelatedField(
        queryset=ProductVariant.objects.all(),
        write_only=True,
        source='variant'
    )
    class Meta:
        model = CartItem
        fields = ['id','variant','variant_id','qty','added_at']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['variant_id'].queryset = __import__('products.models', fromlist=['ProductVariant']).ProductVariant.objects.all()

class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)
    class Meta:
        model = Cart
        fields = ['id','user','session_key','items','created_at']
