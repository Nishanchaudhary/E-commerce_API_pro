from rest_framework.views import APIView
from rest_framework import permissions,status
from rest_framework.response import Response
from cart.models import Cart,CartItem
from .models import Order,OrderItem
from decimal import Decimal

class CreateOrderFromCart(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def post(self, request):
        user = request.user
        cart = Cart.objects.filter(user=user).first()
        if not cart or not cart.items.exists():
            return Response({'detail':'cart is empty'}, status=status.HTTP_400_BAD_REQUEST)
        order = Order.objects.create(user=user, status='pending')
        total = Decimal('0.00')
        for item in cart.items.all():
            OrderItem.objects.create(order=order, variant=item.variant, qty=item.qty, price=item.variant.price, vendor=item.variant.product.vendor)
            total += item.variant.price * item.qty
        order.total_amount = total
        order.save()
        # clear cart
        cart.items.all().delete()
        return Response({'order_id': order.id, 'total': str(order.total_amount)}, status=status.HTTP_201_CREATED)
