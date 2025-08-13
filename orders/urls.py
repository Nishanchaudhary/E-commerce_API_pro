from django.urls import path
from .views import CreateOrderFromCart

urlpatterns = [
    path('create/', CreateOrderFromCart.as_view(), name='create_order'),
]
