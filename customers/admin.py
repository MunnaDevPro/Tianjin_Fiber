from django.contrib import admin
from django.utils.html import format_html
from import_export.admin import ImportExportModelAdmin
from import_export import resources
from .models import Customer
from .forms import CustomerForm

class CustomerResource(resources.ModelResource):
    class Meta:
        model = Customer
        import_id_fields = ('id',)
        skip_unchanged = True
        report_skipped = True

@admin.register(Customer)
class CustomerAdmin(ImportExportModelAdmin):
    resource_classes = [CustomerResource]
    export_template_name = 'admin/customers/customer/export.html'
    
    form = CustomerForm
    list_display = ('customer_id_display', 'company_info', 'contact_info', 'location_info', 'customer_type_badge', 'status_badge', 'next_followup_display')
    list_display_links = ('customer_id_display', 'company_info')
    search_fields = ('customer_id', 'company_name', 'contact_person', 'email', 'phone', 'city', 'country')
    list_filter = ('customer_type', 'status', 'lead_source', 'first_contact_date', 'next_followup_date')
    ordering = ('-created_at',)

    class Media:
        css = {
            'all': ('css/customer_admin.css', 'css/import_export.css')
        }

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

    def customer_id_display(self, obj):
        return format_html('<span style="white-space: nowrap; font-size: 0.75rem; font-weight: 600; color: #334155;">{}</span>', obj.customer_id)
    customer_id_display.short_description = 'ID'
    customer_id_display.admin_order_field = 'customer_id'

    def company_info(self, obj):
        return format_html(
            '<div style="font-weight: 600; color: #0f172a; font-size: 0.80rem; line-height: 1.1; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; max-width: 160px;" title="{}">{}</div>'
            '<div style="color: #64748b; font-size: 0.70rem; margin-top: 2px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; max-width: 160px;" title="{}">{}</div>',
            obj.company_name, obj.company_name, obj.position or 'No Position', obj.position or 'No Position'
        )
    company_info.short_description = 'Company / Position'

    def contact_info(self, obj):
        email_str = f'<div style="font-size: 0.70rem; color: #475569; margin-top: 2px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; max-width: 160px;" title="{obj.email}"><i class="fas fa-envelope" style="margin-right: 4px; color: #94a3b8; font-size: 0.65rem;"></i>{obj.email.lower()}</div>' if obj.email else ''
        info = f'<div style="font-weight: 600; color: #1e293b; font-size: 0.80rem; line-height: 1.1; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; max-width: 160px;" title="{obj.contact_person}">{obj.contact_person}</div>' + email_str
        return format_html(info)
    contact_info.short_description = 'Contact Person'

    def location_info(self, obj):
        loc = []
        if obj.city:
            loc.append(obj.city)
        if obj.country:
            loc.append(obj.country)
        return format_html('<div style="white-space: nowrap; font-size: 0.75rem;">{}</div>', ", ".join(loc) if loc else "-")
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
            '<span style="background: {}; color: {}; padding: 3px 8px; border-radius: 12px; '
            'font-weight: 600; font-size: 0.70rem; border: 1px solid rgba(0,0,0,0.03); white-space: nowrap;">{}</span>',
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
            '<span style="background: {}; color: {}; padding: 3px 8px; border-radius: 12px; '
            'font-weight: 600; font-size: 0.70rem; border: 1px solid rgba(0,0,0,0.03); white-space: nowrap;">{}</span>',
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

