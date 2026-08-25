from django.contrib import admin
from django.utils.html import format_html
from django.utils.text import Truncator
from import_export.admin import ImportExportModelAdmin
from import_export import resources
from .models import ContactPageSettings, ContactMessage

class ContactMessageResource(resources.ModelResource):
    class Meta:
        model = ContactMessage
        import_id_fields = ('id',)
        skip_unchanged = True
        report_skipped = True

@admin.register(ContactPageSettings)
class ContactPageSettingsAdmin(admin.ModelAdmin):
    pass

@admin.register(ContactMessage)
class ContactMessageAdmin(ImportExportModelAdmin):
    resource_classes = [ContactMessageResource]

    class Media:
        css = {
            'all': ('css/import_export.css',)
        }

    list_display = ('sender_info', 'contact_details', 'message_preview', 'received_date')
    list_display_links = ('sender_info', 'message_preview')
    search_fields = ('name', 'email', 'phone', 'subject', 'message')
    list_filter = ('created_at',)
    readonly_fields = ('name', 'email', 'phone', 'subject', 'message', 'created_at')

    def sender_info(self, obj):
        return format_html(
            '<div style="line-height: 1.1; display: flex; flex-direction: column; min-width: 120px;">'
            '<strong style="font-size: 13px; color: #1e293b; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; max-width: 180px;" title="{}">{}</strong>'
            '<span style="font-size: 11px; color: #64748b; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; max-width: 180px;" title="{}">{}</span>'
            '</div>',
            obj.name, obj.name, obj.email.lower(), obj.email.lower()
        )
    sender_info.short_description = "Sender"

    def contact_details(self, obj):
        if obj.phone:
            phone_html = f'''<div style="display: flex; align-items: center; white-space: nowrap;">
                <span style="background-color: #dcfce7; color: #16a34a; width: 22px; height: 22px; border-radius: 50%; display: inline-flex; align-items: center; justify-content: center; margin-right: 6px; box-shadow: 0 1px 2px rgba(0,0,0,0.05);">
                    <i class="fas fa-phone-alt" style="font-size: 10px;"></i>
                </span>
                <span style="font-size: 12.5px; color: #334155; font-weight: 500;">{obj.phone}</span>
            </div>'''
        else:
            phone_html = '<div style="font-size: 12px; color: #cbd5e1; white-space: nowrap; display: flex; align-items: center; height: 22px;"><i>No phone</i></div>'
        return format_html(phone_html)
    contact_details.short_description = "Contact"

    def message_preview(self, obj):
        subject = Truncator(obj.subject).chars(40)
        message = Truncator(obj.message).chars(60)
        return format_html(
            '<div style="max-width: 250px; line-height: 1.2;">'
            '<strong style="font-size: 12px; color: #334155; display: block; margin-bottom: 2px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;" title="{}">{}</strong>'
            '<span style="font-size: 11px; color: #64748b; display: block; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;" title="{}">{}</span>'
            '</div>',
            obj.subject, subject, obj.message, message
        )
    message_preview.short_description = "Subject & Message"

    def received_date(self, obj):
        return format_html(
            '<span style="background-color: #f1f5f9; color: #475569; padding: 3px 6px; border-radius: 4px; font-size: 11px; font-weight: 500; display: inline-block; white-space: nowrap;">'
            '<i class="far fa-calendar-alt mr-1" style="color: #64748b;"></i> {}'
            '</span>',
            obj.created_at.strftime('%b %d, %Y, %I:%M %p')
        )
    received_date.short_description = "Received Date"

    def has_add_permission(self, request):
        return False
