from django.urls import path
from .views import KhaltiVerifyView

urlpatterns = [
    path('khalti/verify/', KhaltiVerifyView.as_view(), name='khalti_verify'),
]
