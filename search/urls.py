
from django.urls import path
from .views import ProductSearchView

urlpatterns = [
    path('search/products/', ProductSearchView.as_view(), name='product-search'),
]
