from django.contrib import admin
from .models import ServicesHeader, ServiceItem, ProcessSection, ProcessStep, ServicesCTA

@admin.register(ServicesHeader)
class ServicesHeaderAdmin(admin.ModelAdmin):
    pass

@admin.register(ServiceItem)
class ServiceItemAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_active', 'order')
    list_editable = ('is_active', 'order')

class ProcessStepInline(admin.StackedInline):
    model = ProcessStep
    extra = 1

@admin.register(ProcessSection)
class ProcessSectionAdmin(admin.ModelAdmin):
    inlines = [ProcessStepInline]

@admin.register(ServicesCTA)
class ServicesCTAAdmin(admin.ModelAdmin):
    pass
