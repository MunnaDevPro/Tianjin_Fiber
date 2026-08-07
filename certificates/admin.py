from django.contrib import admin
from django.utils.html import format_html
from .models import CertificatesHeader, Certificate, CertificatesCTA

@admin.register(CertificatesHeader)
class CertificatesHeaderAdmin(admin.ModelAdmin):
    pass

@admin.register(Certificate)
class CertificateAdmin(admin.ModelAdmin):
    list_display = ('image_preview', 'title', 'is_active', 'order')
    list_display_links = ('image_preview', 'title')
    list_editable = ('is_active', 'order')

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="width: 50px; height: 50px; object-fit: cover; border-radius: 8px; border: 1px solid #e2e8f0;" />', obj.image.url)
        return ""
    image_preview.short_description = 'Image'

@admin.register(CertificatesCTA)
class CertificatesCTAAdmin(admin.ModelAdmin):
    pass
