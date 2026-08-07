from django.db import models
from django.contrib.auth.models import User

class UserSession(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sessions')
    session_key = models.CharField(max_length=40, unique=True, null=True, blank=True)
    ip_address = models.GenericIPAddressField()
    user_agent = models.TextField()
    device_info = models.CharField(max_length=255)
    browser_info = models.CharField(max_length=255)
    location = models.CharField(max_length=255, default="Unknown Location")
    login_time = models.DateTimeField(auto_now_add=True)
    last_activity = models.DateTimeField(auto_now=True)
    logout_time = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = "User Session Log"
        verbose_name_plural = "User Session Logs"
        ordering = ['-login_time']

    def __str__(self):
        return f"{self.user.username} - {self.device_info} ({self.ip_address})"
