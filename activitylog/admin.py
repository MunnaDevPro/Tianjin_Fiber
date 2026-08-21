from django.contrib import admin
from django.utils.html import format_html
from .models import UserSession

@admin.register(UserSession)
class UserSessionAdmin(admin.ModelAdmin):
    list_display = ('user', 'status_badge', 'ip_address', 'location', 'device_info', 'browser_info', 'login_time', 'last_activity', 'logout_time')
    list_filter = ('is_active', 'login_time')
    search_fields = ('user__username', 'ip_address', 'location', 'device_info')
    
    # Read-only configuration
    readonly_fields = ('user', 'session_key', 'ip_address', 'user_agent', 'device_info', 'browser_info', 'location', 'login_time', 'last_activity', 'logout_time', 'is_active')
    
    def status_badge(self, obj):
        if obj.is_active:
            return format_html('<span class="badge badge-success px-2.5 py-1" style="border-radius: 4px; font-weight: 600; font-size: 0.75rem; background-color: #10b981; color: white;">Active</span>')
        if obj.logout_time:
            return format_html('<span class="badge badge-secondary px-2.5 py-1" style="border-radius: 4px; font-weight: 600; font-size: 0.75rem; background-color: #64748b; color: white;">Logged Out</span>')
        return format_html('<span class="badge badge-warning px-2.5 py-1" style="border-radius: 4px; font-weight: 600; font-size: 0.75rem; background-color: #f59e0b; color: white;">Timed Out</span>')
    status_badge.short_description = 'Status'

    def changelist_view(self, request, extra_context=None):
        # Dynamically deactivate sessions that are no longer valid
        from django.contrib.sessions.models import Session
        from django.utils import timezone
        from django.conf import settings

        # 1. Fetch active Django session keys from DB
        active_django_sessions = set(
            Session.objects.filter(expire_date__gt=timezone.now()).values_list('session_key', flat=True)
        )

        # 2. Deactivate sessions not in active Django sessions
        UserSession.objects.filter(is_active=True).exclude(session_key__in=active_django_sessions).update(is_active=False)

        # 3. Deactivate sessions that have exceeded the inactivity timeout (default 30 mins)
        inactivity_timeout = getattr(settings, 'USER_SESSION_TIMEOUT', 1800)
        cutoff_time = timezone.now() - timezone.timedelta(seconds=inactivity_timeout)
        UserSession.objects.filter(is_active=True, last_activity__lt=cutoff_time).update(is_active=False)

        return super().changelist_view(request, extra_context=extra_context)

    # Disable add permission
    def has_add_permission(self, request):
        return False

    # Disable change permission
    def has_change_permission(self, request, obj=None):
        return False

    # Allow log deletion if superuser needs to prune, but disable by default for safety
    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser

