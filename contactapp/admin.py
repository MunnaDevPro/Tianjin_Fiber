from django.contrib import admin
from .models import ContactPageSettings, ContactMessage

@admin.register(ContactPageSettings)
class ContactPageSettingsAdmin(admin.ModelAdmin):
    pass

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'subject', 'created_at')
    readonly_fields = ('name', 'email', 'phone', 'subject', 'message', 'created_at')

    def has_add_permission(self, request):
        return False
