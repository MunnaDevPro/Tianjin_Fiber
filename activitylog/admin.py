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
        return format_html('<span class="badge badge-secondary px-2.5 py-1" style="border-radius: 4px; font-weight: 600; font-size: 0.75rem; background-color: #94a3b8; color: white;">Logged Out</span>')
    status_badge.short_description = 'Status'

    # Disable add permission
    def has_add_permission(self, request):
        return False

    # Disable change permission
    def has_change_permission(self, request, obj=None):
        return False

    # Allow log deletion if superuser needs to prune, but disable by default for safety
    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser
