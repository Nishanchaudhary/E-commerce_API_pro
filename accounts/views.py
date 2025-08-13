from rest_framework import generics, status, permissions
from rest_framework.response import Response
from .serializers import RegisterSerializer, UserSerializer
from .models import User, DeviceSession, OTP
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
import random
from django.utils import timezone
from datetime import timedelta
from .tasks import send_otp_task

class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]

class MeView(generics.RetrieveAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    def get_object(self):
        return self.request.user

# custom token obtain to capture device info
class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['role'] = user.role
        return token

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        resp = super().post(request, *args, **kwargs)
        # create DeviceSession if client sent device_id
        device_id = request.data.get('device_id')
        if device_id and resp.status_code == 200:
            user = User.objects.filter(username=request.data.get('username')).first()
            if user:
                DeviceSession.objects.create(user=user, device_id=device_id,
                                             user_agent=request.META.get('HTTP_USER_AGENT',''))
        return resp

# OTP endpoints
from rest_framework.views import APIView

class SendOTPView(APIView):
    permission_classes = [permissions.AllowAny]
    def post(self, request):
        username = request.data.get('username')
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return Response({'detail':'user not found'}, status=404)
        code = f"{random.randint(100000,999999)}"
        OTP.objects.create(user=user, code=code, purpose='login')
        # send via celery task (email/sms)
        send_otp_task.delay(user.id, code)
        return Response({'detail':'OTP sent'})

class VerifyOTPView(APIView):
    permission_classes = [permissions.AllowAny]
    def post(self, request):
        username = request.data.get('username'); code = request.data.get('code')
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return Response({'detail':'user not found'}, status=404)
        otp = OTP.objects.filter(user=user, code=code, is_used=False).order_by('-created_at').first()
        if not otp:
            return Response({'detail':'invalid otp'}, status=400)
        # expiry 10 min
        if timezone.now() - otp.created_at > timedelta(minutes=10):
            return Response({'detail':'otp expired'}, status=400)
        otp.is_used = True; otp.save()
        return Response({'detail':'verified'})
