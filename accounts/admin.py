from django.contrib import admin
from .models import User, DeviceSession, OTP
# Register your models here.

class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'role', 'phone_number', 'email']
    search_fields = ['email','username','phone_number']

class DeviceSessionAdmin(admin.ModelAdmin):
    list_display = ['user', 'device_id', 'created_at', 'revoked']
    search_fields = ['user__email']

class OTPAdmin(admin.ModelAdmin):
    list_display = ['user', 'created_at']
    search_fields = ['user__email']

admin.site.register(User, UserAdmin)
admin.site.register(DeviceSession, DeviceSessionAdmin)
admin.site.register(OTP, OTPAdmin)
