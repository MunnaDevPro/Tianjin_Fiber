from django.contrib import admin
from django.utils.html import format_html
from .models import ServicesHeader, ServiceItem, ProcessSection, ProcessStep, ServicesCTA

@admin.register(ServicesHeader)
class ServicesHeaderAdmin(admin.ModelAdmin):
    pass

@admin.register(ServiceItem)
class ServiceItemAdmin(admin.ModelAdmin):
    list_display = ('image_preview', 'title', 'is_active', 'order')
    list_display_links = ('image_preview', 'title')
    list_editable = ('is_active', 'order')

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="width: 50px; height: 50px; object-fit: cover; border-radius: 8px; border: 1px solid #e2e8f0;" />', obj.image.url)
        return ""
    image_preview.short_description = 'Image'

class ProcessStepInline(admin.StackedInline):
    model = ProcessStep
    extra = 1

@admin.register(ProcessSection)
class ProcessSectionAdmin(admin.ModelAdmin):
    inlines = [ProcessStepInline]

@admin.register(ProcessStep)
class ProcessStepAdmin(admin.ModelAdmin):
    list_display = ('title', 'icon', 'is_active', 'order')
    list_display_links = ('title',)
    list_editable = ('is_active', 'order')

@admin.register(ServicesCTA)
class ServicesCTAAdmin(admin.ModelAdmin):
    pass
