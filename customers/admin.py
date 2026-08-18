from django.contrib import admin
from django.utils.html import format_html
from .models import Customer

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('photo_preview', 'customer_info', 'phone_display', 'address_display', 'date_added')
    list_display_links = ('photo_preview', 'customer_info')
    search_fields = ('name', 'full_name', 'phone_number', 'address')
    list_filter = ('created_at',)
    ordering = ('-created_at',)

    def photo_preview(self, obj):
        if obj.photo:
            return format_html(
                '<img src="{}" style="width: 42px; height: 42px; object-fit: cover; border-radius: 50%; '
                'border: 2px solid #ffffff; box-shadow: 0 2px 4px rgba(0,0,0,0.08); transition: transform 0.2s;" '
                'onmouseover="this.style.transform=\'scale(1.15)\'" onmouseout="this.style.transform=\'scale(1)\'" />', 
                obj.photo.url
            )
        return format_html(
            '<div style="width: 42px; height: 42px; border-radius: 50%; background: linear-gradient(135deg, #e2e8f0 0%, #cbd5e1 100%); '
            'display: flex; align-items: center; justify-content: center; color: #475569; font-weight: bold; '
            'box-shadow: inset 0 2px 4px rgba(0,0,0,0.04); font-size: 0.95rem;">{}</div>', 
            obj.full_name[0].upper() if obj.full_name else '?'
        )
    photo_preview.short_description = 'Photo'

    def customer_info(self, obj):
        return format_html(
            '<div style="font-weight: 600; color: #0f172a; font-size: 0.85rem; line-height: 1.2;">{}</div>'
            '<div style="color: #64748b; font-size: 0.72rem; margin-top: 1px;">@{}</div>',
            obj.full_name, obj.name
        )
    customer_info.short_description = 'Customer'

    def phone_display(self, obj):
        return format_html(
            '<span style="background: #f1f5f9; color: #334155; padding: 4px 10px; border-radius: 12px; '
            'font-weight: 500; font-size: 0.78rem; display: inline-flex; align-items: center; border: 1px solid #e2e8f0;">'
            '<i class="fas fa-phone-alt" style="font-size: 0.65rem; margin-right: 5px; color: #64748b;"></i>{}'
            '</span>',
            obj.phone_number
        )
    phone_display.short_description = 'Phone Number'

    def address_display(self, obj):
        from django.utils.text import Truncator
        truncated = Truncator(obj.address).chars(50)
        return format_html(
            '<span style="color: #475569; font-size: 0.78rem; display: block; max-width: 250px; '
            'white-space: normal; line-height: 1.3;" title="{}">{}</span>',
            obj.address, truncated
        )
    address_display.short_description = 'Address'

    def date_added(self, obj):
        return format_html(
            '<div style="font-size: 0.78rem; color: #475569; font-weight: 500; display: inline-flex; align-items: center; white-space: nowrap;">'
            '<i class="far fa-calendar-alt" style="margin-right: 5px; color: #94a3b8;"></i>{}'
            '</div>',
            obj.created_at.strftime('%b %d, %Y %I:%M %p')
        )
    date_added.short_description = 'Created At'

