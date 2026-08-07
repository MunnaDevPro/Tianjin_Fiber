from django.contrib.auth.signals import user_logged_out, user_logged_in
from django.dispatch import receiver
from django.utils import timezone
from .models import UserSession

@receiver(user_logged_in)
def handle_user_login(sender, request, user, **kwargs):
    # Middleware will handle creating/updating the UserSession object
    pass

@receiver(user_logged_out)
def handle_user_logout(sender, request, user, **kwargs):
    if request and hasattr(request, 'session'):
        session_key = request.session.session_key
        if session_key:
            UserSession.objects.filter(session_key=session_key).update(
                is_active=False,
                logout_time=timezone.now()
            )
