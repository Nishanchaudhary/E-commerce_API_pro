from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from django.conf import settings
import requests
from payments.models import Payment
from orders.models import Order

class KhaltiVerifyView(APIView):
    permission_classes = [permissions.AllowAny]  # client verifies after Khalti checkout
    def post(self, request):
        token = request.data.get('token')
        amount = request.data.get('amount')  # in paisa (integer)
        order_id = request.data.get('order_id')
        if not token or not amount or not order_id:
            return Response({'detail':'token, amount and order_id required'}, status=400)
        url = 'https://khalti.com/api/v2/payment/verify/'
        headers = {'Authorization': f'Key {settings.KHALTI_SECRET_KEY}'}
        resp = requests.post(url, data={'token': token, 'amount': amount}, headers=headers)
        data = resp.json()
        if resp.status_code == 200 and data.get('idx'):
            # mark payment and order
            try:
                order = Order.objects.get(pk=order_id)
            except Order.DoesNotExist:
                return Response({'detail':'order not found'}, status=404)
            Payment.objects.create(order=order, amount=order.total_amount, provider='khalti', provider_id=data.get('idx'), success=True, raw_response=data)
            order.status = 'paid'
            order.save()
            return Response({'success': True, 'data': data})
        else:
            return Response({'success': False, 'detail': data}, status=400)
