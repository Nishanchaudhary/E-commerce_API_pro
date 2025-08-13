from rest_framework import generics, permissions, status
from rest_framework.response import Response
from .models import Cart,CartItem
from .serializers import CartSerializer,CartItemSerializer
from django.shortcuts import get_object_or_404

class CartDetailView(generics.RetrieveAPIView):
    serializer_class = CartSerializer
    permission_classes = [permissions.AllowAny]
    def get_object(self):
        user = self.request.user if self.request.user.is_authenticated else None
        session_key = self.request.COOKIES.get('cart_session')
        if user:
            cart, _ = Cart.objects.get_or_create(user=user)
            return cart
        cart, _ = Cart.objects.get_or_create(session_key=session_key or 'guest')
        return cart

from rest_framework.views import APIView

class AddToCartView(APIView):
    permission_classes = [permissions.AllowAny]
    def post(self, request):
        variant_id = request.data.get('variant_id')
        qty = int(request.data.get('qty',1))
        user = request.user if request.user.is_authenticated else None
        session_key = request.COOKIES.get('cart_session', 'guest')
        if user:
            cart, _ = Cart.objects.get_or_create(user=user)
        else:
            cart, _ = Cart.objects.get_or_create(session_key=session_key)
        variant = get_object_or_404(__import__('apps.products.models', fromlist=['ProductVariant']).ProductVariant, pk=variant_id)
        item, created = CartItem.objects.get_or_create(cart=cart, variant=variant)
        if not created:
            item.qty += qty
        else:
            item.qty = qty
        item.save()
        return Response({'detail':'added'}, status=status.HTTP_200_OK)

