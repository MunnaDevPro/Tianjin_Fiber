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
            '<i class="fas fa-calendar-alt mr-1" style="color: #64748b;"></i> {}'
            '</span>',
            obj.created_at.strftime('%b %d, %Y, %I:%M %p')
        )
    received_date.short_description = "Received Date"

    def has_add_permission(self, request):
        return False


from django import forms
from django.utils.safestring import mark_safe
from .models import HostingerEmailSettings, SentEmailLog, ReceivedEmail

class HostingerEmailSettingsForm(forms.ModelForm):
    smtp_password = forms.CharField(
        widget=forms.PasswordInput(render_value=True, attrs={'class': 'vTextField', 'autocomplete': 'new-password'}),
        required=False,
        help_text="Your Hostinger email account password (stored securely)."
    )

    class Meta:
        model = HostingerEmailSettings
        fields = '__all__'

@admin.register(HostingerEmailSettings)
class HostingerEmailSettingsAdmin(admin.ModelAdmin):
    form = HostingerEmailSettingsForm
    fieldsets = (
        ("Hostinger Outgoing Mail (SMTP)", {
            'description': mark_safe(
                '<div style="background: #f5f3ff; border: 1px solid #ddd6fe; border-left: 4px solid #7c3aed; padding: 12px 16px; border-radius: 6px; margin-bottom: 16px;">'
                '<div style="font-weight: 700; color: #6d28d9; font-size: 13px; margin-bottom: 4px;">'
                '<i class="fas fa-shield-alt mr-1"></i> Hostinger Webmail Integration'
                '</div>'
                '<div style="font-size: 12px; color: #475569; line-height: 1.5;">'
                'Enter your Hostinger email account credentials below. These are used when sending proposals, quotes, and emails directly from your dashboard.'
                '</div>'
                '</div>'
            ),
            'fields': ('is_active', 'smtp_host', 'smtp_port', 'smtp_user', 'smtp_password', 'use_ssl', 'use_tls')
        }),
        ("Hostinger Incoming Mail (IMAP)", {
            'description': mark_safe(
                '<div style="background: #f0fdf4; border: 1px solid #bbf7d0; border-left: 4px solid #16a34a; padding: 12px 16px; border-radius: 6px; margin-bottom: 16px;">'
                '<div style="font-weight: 700; color: #15803d; font-size: 13px; margin-bottom: 4px;">'
                '<i class="fas fa-inbox mr-1"></i> Hostinger IMAP Webmail Retrieval'
                '</div>'
                '<div style="font-size: 12px; color: #475569; line-height: 1.5;">'
                'Incoming mail configuration to retrieve and sync customer replies directly from Hostinger servers.'
                '</div>'
                '</div>'
            ),
            'fields': ('imap_host', 'imap_port', 'use_imap_ssl')
        }),
        ("Sender Identity & Signature", {
            'description': mark_safe(
                '<div style="background: #f8fafc; border: 1px solid #e2e8f0; border-left: 4px solid #0284c7; padding: 12px 16px; border-radius: 6px; margin-bottom: 16px;">'
                '<div style="font-weight: 700; color: #0369a1; font-size: 13px; margin-bottom: 4px;">'
                '<i class="fas fa-signature mr-1"></i> Outbound Email Identity'
                '</div>'
                '<div style="font-size: 12px; color: #475569; line-height: 1.5;">'
                'Configure the display name and corporate signature appended to messages sent from the dashboard.'
                '</div>'
                '</div>'
            ),
            'fields': ('sender_name', 'default_signature')
        }),
    )

    def has_add_permission(self, request):
        if HostingerEmailSettings.objects.exists():
            return False
        return super().has_add_permission(request)

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(ReceivedEmail)
class ReceivedEmailAdmin(admin.ModelAdmin):
    change_form_template = 'admin/contactapp/receivedemail/change_form.html'
    list_display = ('sender_display', 'subject_display', 'attachment_chip', 'read_badge', 'received_time')
    list_display_links = ('sender_display', 'subject_display')
    list_filter = ('is_read', 'has_attachment', 'received_at')
    search_fields = ('sender_name', 'sender_email', 'subject', 'body_text')
    readonly_fields = ('message_id', 'uid', 'sender_name', 'sender_email', 'recipient', 'subject', 'snippet', 'body_text', 'body_html', 'has_attachment', 'attachment_names', 'is_read', 'is_starred', 'folder', 'received_at', 'created_at')
    list_per_page = 25
    actions = ['mark_as_read', 'mark_as_unread']

    def change_view(self, request, object_id, form_url='', extra_context=None):
        try:
            email_obj = ReceivedEmail.objects.get(pk=object_id)
            if not email_obj.is_read:
                email_obj.is_read = True
                email_obj.save(update_fields=['is_read'])
        except Exception:
            pass
        return super().change_view(request, object_id, form_url, extra_context=extra_context)

    def sender_display(self, obj):
        initial = (obj.sender_name or obj.sender_email or 'U')[0].upper()
        return format_html(
            '<div style="display: flex; align-items: center; gap: 10px; line-height: 1.3; text-transform: none !important;">'
            '<div style="width: 32px; height: 32px; border-radius: 50%; background: #e0f2fe; color: #0369a1; font-weight: 700; font-size: 12px; display: flex; align-items: center; justify-content: center; flex-shrink: 0; border: 1px solid #bae6fd;">{}</div>'
            '<div style="min-width: 0;">'
            '<strong style="color: #0f172a; font-size: 13px; display: block;" class="text-truncate">{}</strong>'
            '<span style="color: #64748b; font-size: 11.5px; text-transform: lowercase !important;" class="text-truncate d-block">{}</span>'
            '</div>'
            '</div>',
            initial, obj.sender_name or obj.sender_email, obj.sender_email
        )
    sender_display.short_description = "From"

    def subject_display(self, obj):
        unread_style = "font-weight: 700; color: #0f172a;" if not obj.is_read else "font-weight: 500; color: #334155;"
        return format_html(
            '<div style="max-width: 380px; line-height: 1.35; text-transform: none !important;">'
            '<span style="{} font-size: 12.5px; display: block; margin-bottom: 2px;" title="{}">{}</span>'
            '<span style="color: #64748b; font-size: 11.5px; display: block;" title="{}">{}</span>'
            '</div>',
            unread_style, obj.subject, Truncator(obj.subject).chars(50),
            obj.snippet, Truncator(obj.snippet).chars(70)
        )
    subject_display.short_description = "Subject & Preview"

    def attachment_chip(self, obj):
        if obj.has_attachment:
            return format_html(
                '<span style="display: inline-flex; align-items: center; gap: 5px; background: #eff6ff; color: #1d4ed8; border: 1px solid #bfdbfe; padding: 3px 8px; border-radius: 6px; font-size: 11px; font-weight: 600;" title="{}">'
                '<i class="fas fa-paperclip text-primary"></i> File'
                '</span>',
                obj.attachment_names or 'Attached file'
            )
        return format_html('<span style="color: #cbd5e1; font-size: 13px;">—</span>')
    attachment_chip.short_description = "File"

    def read_badge(self, obj):
        if not obj.is_read:
            return format_html(
                '<span style="display: inline-flex; align-items: center; gap: 5px; background: #ede9fe; color: #6d28d9; border: 1px solid #ddd6fe; padding: 3px 8px; border-radius: 9999px; font-size: 11px; font-weight: 700;">'
                '<span style="width: 7px; height: 7px; border-radius: 50%; background: #7c3aed;"></span> Unread'
                '</span>'
            )
        return format_html(
            '<span style="color: #94a3b8; font-size: 11px; font-weight: 500;">Read</span>'
        )
    read_badge.short_description = "Status"

    def received_time(self, obj):
        return format_html(
            '<span style="display: inline-flex; align-items: center; gap: 6px; background-color: #f8fafc; color: #475569; border: 1px solid #e2e8f0; padding: 4px 8px; border-radius: 6px; font-size: 11px; font-weight: 500; white-space: nowrap;">'
            '<i class="fas fa-calendar-alt text-primary" style="font-size: 11px;"></i> {}'
            '</span>',
            obj.received_at.strftime('%b %d, %Y, %I:%M %p')
        )
    received_time.short_description = "Received Date"

    def mark_as_read(self, request, queryset):
        queryset.update(is_read=True)
    mark_as_read.short_description = "Mark selected as Read"

    def mark_as_unread(self, request, queryset):
        queryset.update(is_read=False)
    mark_as_unread.short_description = "Mark selected as Unread"

    def has_add_permission(self, request):
        return False


@admin.register(SentEmailLog)
class SentEmailLogAdmin(admin.ModelAdmin):
    list_display = ('recipient_info', 'subject_preview', 'status_badge', 'attachment_indicator', 'sent_by_user', 'sent_time')
    list_display_links = ('recipient_info', 'subject_preview')
    list_filter = ('status', 'sent_at')
    search_fields = ('recipient', 'cc', 'bcc', 'subject', 'message', 'sent_by__username')
    readonly_fields = ('recipient', 'cc', 'bcc', 'subject', 'message', 'attachment_name', 'status', 'error_message', 'sent_by', 'sent_at')
    list_per_page = 25

    def recipient_info(self, obj):
        email = obj.recipient.strip()
        initial = email[0].upper() if email else 'M'
        cc_html = format_html('<div style="font-size: 11px; color: #64748b; margin-top: 2px;"><i class="fas fa-reply-all mr-1 text-muted" style="font-size: 10px;"></i>Cc: {}</div>', obj.cc) if obj.cc else ''
        return format_html(
            '<div style="display: flex; align-items: center; gap: 10px; line-height: 1.3; text-transform: none !important;">'
            '<div style="width: 32px; height: 32px; border-radius: 50%; background: #ede9fe; color: #6d28d9; font-weight: 700; font-size: 12px; display: flex; align-items: center; justify-content: center; flex-shrink: 0; border: 1px solid #ddd6fe;">{}</div>'
            '<div style="min-width: 0;">'
            '<span style="color: #0f172a; font-size: 13px; font-weight: 600; text-transform: lowercase !important;" class="text-truncate d-block">{}</span>'
            '{}'
            '</div>'
            '</div>',
            initial, email, cc_html
        )
    recipient_info.short_description = "Recipient"

    def subject_preview(self, obj):
        first_line_msg = obj.message.replace('\n', ' ').strip()
        return format_html(
            '<div style="max-width: 340px; line-height: 1.35; text-transform: none !important;">'
            '<strong style="color: #1e293b; font-size: 12.5px; display: block; margin-bottom: 2px;" title="{}">{}</strong>'
            '<span style="color: #64748b; font-size: 11.5px; display: block;" title="{}">{}</span>'
            '</div>',
            obj.subject, Truncator(obj.subject).chars(48),
            first_line_msg, Truncator(first_line_msg).chars(65)
        )
    subject_preview.short_description = "Subject & Message"

    def status_badge(self, obj):
        if obj.status == 'Sent':
            return format_html(
                '<span style="display: inline-flex; align-items: center; gap: 5px; background-color: #ecfdf5; color: #047857; border: 1px solid #a7f3d0; padding: 4px 10px; border-radius: 9999px; font-weight: 600; font-size: 11px; white-space: nowrap;">'
                '<i class="fas fa-check-circle" style="color: #10b981; font-size: 11px;"></i> Sent'
                '</span>'
            )
        return format_html(
            '<span style="display: inline-flex; align-items: center; gap: 5px; background-color: #fff1f2; color: #be123c; border: 1px solid #fecdd3; padding: 4px 10px; border-radius: 9999px; font-weight: 600; font-size: 11px; white-space: nowrap;" title="{}">'
            '<i class="fas fa-times-circle" style="color: #ef4444; font-size: 11px;"></i> Failed'
            '</span>',
            obj.error_message or 'Unknown delivery error'
        )
    status_badge.short_description = "Status"

    def attachment_indicator(self, obj):
        if obj.attachment_name:
            return format_html(
                '<span style="display: inline-flex; align-items: center; gap: 5px; background: #eff6ff; color: #1d4ed8; border: 1px solid #bfdbfe; padding: 3px 8px; border-radius: 6px; font-size: 11px; font-weight: 500;" title="{}">'
                '<i class="fas fa-paperclip text-primary"></i> {}'
                '</span>',
                obj.attachment_name, Truncator(obj.attachment_name).chars(18)
            )
        return format_html('<span style="color: #cbd5e1; font-size: 13px;">—</span>')
    attachment_indicator.short_description = "Attachment"

    def sent_by_user(self, obj):
        user_name = obj.sent_by.username if obj.sent_by else 'Hostinger SMTP'
        return format_html(
            '<div style="display: inline-flex; align-items: center; gap: 6px; color: #334155; font-size: 12px; font-weight: 500;">'
            '<i class="fas fa-user-circle text-muted" style="font-size: 13px;"></i> {}'
            '</div>',
            user_name
        )
    sent_by_user.short_description = "Sender"

    def sent_time(self, obj):
        return format_html(
            '<span style="display: inline-flex; align-items: center; gap: 6px; background-color: #f8fafc; color: #475569; border: 1px solid #e2e8f0; padding: 4px 8px; border-radius: 6px; font-size: 11px; font-weight: 500; white-space: nowrap;">'
            '<i class="fas fa-calendar-alt text-primary" style="font-size: 11px;"></i> {}'
            '</span>',
            obj.sent_at.strftime('%b %d, %Y, %I:%M %p')
        )
    sent_time.short_description = "Sent At"

    def has_add_permission(self, request):
        return False

