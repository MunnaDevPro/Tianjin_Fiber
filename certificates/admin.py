from django.contrib import admin
from .models import CertificatesHeader, Certificate, CertificatesCTA

@admin.register(CertificatesHeader)
class CertificatesHeaderAdmin(admin.ModelAdmin):
    pass

@admin.register(Certificate)
class CertificateAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_active', 'order')
    list_editable = ('is_active', 'order')

@admin.register(CertificatesCTA)
class CertificatesCTAAdmin(admin.ModelAdmin):
    pass
