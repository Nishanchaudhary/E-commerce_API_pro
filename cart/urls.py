from django.urls import path
from .views import CartDetailView, AddToCartView

urlpatterns = [
    path('', CartDetailView.as_view(), name='cart_detail'),
    path('add/', AddToCartView.as_view(), name='cart_add'),
]
