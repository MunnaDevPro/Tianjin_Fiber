from django.contrib import admin
from django.utils.html import format_html
from .models import Customer
from .forms import CustomerForm

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    form = CustomerForm
    list_display = ('customer_id', 'company_info', 'contact_info', 'location_info', 'customer_type_badge', 'status_badge', 'next_followup_display')
    list_display_links = ('customer_id', 'company_info')
    search_fields = ('customer_id', 'company_name', 'contact_person', 'email', 'phone', 'city', 'country')
    list_filter = ('customer_type', 'status', 'lead_source', 'first_contact_date', 'next_followup_date')
    ordering = ('-created_at',)

    fieldsets = (
        ('Basic Information', {
            'fields': ('customer_id', 'company_name', 'contact_person', 'position')
        }),
        ('Contact Details', {
            'fields': ('email', 'phone', 'whatsapp', 'website', 'linkedin')
        }),
        ('Location', {
            'fields': ('city', 'country')
        }),
        ('Lead & Product Information', {
            'fields': ('product_interest', 'customer_type', 'lead_source', 'status')
        }),
        ('Timeline & Notes', {
            'fields': ('first_contact_date', 'last_contact_date', 'next_followup_date', 'notes')
        }),
    )

    def company_info(self, obj):
        return format_html(
            '<div style="font-weight: 600; color: #0f172a; font-size: 0.85rem; line-height: 1.2;">{}</div>'
            '<div style="color: #64748b; font-size: 0.72rem; margin-top: 1px;">{}</div>',
            obj.company_name, obj.position or 'No Position'
        )
    company_info.short_description = 'Company / Position'

    def contact_info(self, obj):
        email_str = f'<div style="font-size: 0.75rem; color: #475569;"><i class="fas fa-envelope" style="margin-right: 4px; color: #94a3b8;"></i>{obj.email}</div>' if obj.email else ''
        phone_str = f'<div style="font-size: 0.75rem; color: #475569; margin-top: 2px;"><i class="fas fa-phone-alt" style="margin-right: 4px; color: #94a3b8;"></i>{obj.phone}</div>' if obj.phone else ''
        whatsapp_str = f'<div style="font-size: 0.75rem; color: #128c7e; margin-top: 2px;"><i class="fab fa-whatsapp" style="margin-right: 4px;"></i>{obj.whatsapp}</div>' if obj.whatsapp else ''
        
        info = f'<div style="font-weight: 500; color: #1e293b;">{obj.contact_person}</div>' + email_str + phone_str + whatsapp_str
        return format_html(info)
    contact_info.short_description = 'Contact Person'

    def location_info(self, obj):
        loc = []
        if obj.city:
            loc.append(obj.city)
        if obj.country:
            loc.append(obj.country)
        return ", ".join(loc) if loc else "-"
    location_info.short_description = 'Location'

    def customer_type_badge(self, obj):
        bg_colors = {
            'Lead': '#eff6ff',
            'Prospect': '#faf5ff',
            'Customer': '#f0fdf4',
            'Partner': '#f0fdfa'
        }
        text_colors = {
            'Lead': '#1e40af',
            'Prospect': '#6b21a8',
            'Customer': '#166534',
            'Partner': '#0f766e'
        }
        bg = bg_colors.get(obj.customer_type, '#f1f5f9')
        text = text_colors.get(obj.customer_type, '#475569')
        return format_html(
            '<span style="background: {}; color: {}; padding: 4px 10px; border-radius: 12px; '
            'font-weight: 600; font-size: 0.75rem; border: 1px solid rgba(0,0,0,0.03);">{}</span>',
            bg, text, obj.customer_type
        )
    customer_type_badge.short_description = 'Type'

    def status_badge(self, obj):
        bg_colors = {
            'Active': '#ecfdf5',
            'Inactive': '#fef2f2',
            'Pending': '#fffbeb',
            'Hot': '#fff5f5',
            'Warm': '#fff7ed',
            'Cold': '#eff6ff'
        }
        text_colors = {
            'Active': '#065f46',
            'Inactive': '#991b1b',
            'Pending': '#92400e',
            'Hot': '#e11d48',
            'Warm': '#c2410c',
            'Cold': '#1e40af'
        }
        bg = bg_colors.get(obj.status, '#f1f5f9')
        text = text_colors.get(obj.status, '#475569')
        return format_html(
            '<span style="background: {}; color: {}; padding: 4px 10px; border-radius: 12px; '
            'font-weight: 600; font-size: 0.75rem; border: 1px solid rgba(0,0,0,0.03);">{}</span>',
            bg, text, obj.status
        )
    status_badge.short_description = 'Status'

    def next_followup_display(self, obj):
        if obj.next_followup_date:
            from django.utils import timezone
            today = timezone.localdate()
            if obj.next_followup_date < today:
                color = '#ef4444' # Overdue
                icon_color = '#ef4444'
            elif obj.next_followup_date == today:
                color = '#f97316' # Today
                icon_color = '#f97316'
            else:
                color = '#475569' # Future
                icon_color = '#94a3b8'
                
            return format_html(
                '<div style="font-size: 0.78rem; color: {}; font-weight: 500; display: inline-flex; align-items: center; white-space: nowrap;">'
                '<i class="far fa-calendar-alt" style="margin-right: 5px; color: {};"></i>{}'
                '</div>',
                color, icon_color, obj.next_followup_date.strftime('%b %d, %Y')
            )
        return format_html('<span style="color: #94a3b8; font-size: 0.75rem;">None</span>')
    next_followup_display.short_description = 'Next Follow-up'

