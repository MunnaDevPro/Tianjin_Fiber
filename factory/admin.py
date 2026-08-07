from django.contrib import admin
from django.utils.html import format_html
from .models import FactoryHeader, FactoryGallerySection, FactoryImage, FactoryVideoSection, FactoryVideo, FactoryCTA

@admin.register(FactoryHeader)
class FactoryHeaderAdmin(admin.ModelAdmin):
    pass

class FactoryImageInline(admin.StackedInline):
    model = FactoryImage
    extra = 1

@admin.register(FactoryGallerySection)
class FactoryGallerySectionAdmin(admin.ModelAdmin):
    inlines = [FactoryImageInline]
    fieldsets = (
        ('Title Section Details', {
            'fields': ('title', 'description'),
            'classes': ('collapse',),
        }),
    )

@admin.register(FactoryImage)
class FactoryImageAdmin(admin.ModelAdmin):
    list_display = ('image_preview', 'title', 'is_active', 'order')
    list_display_links = ('image_preview', 'title')
    list_editable = ('is_active', 'order')

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="width: 50px; height: 50px; object-fit: cover; border-radius: 8px; border: 1px solid #e2e8f0;" />', obj.image.url)
        return ""
    image_preview.short_description = 'Image'

class FactoryVideoInline(admin.StackedInline):
    model = FactoryVideo
    extra = 1

@admin.register(FactoryVideoSection)
class FactoryVideoSectionAdmin(admin.ModelAdmin):
    inlines = [FactoryVideoInline]

@admin.register(FactoryVideo)
class FactoryVideoAdmin(admin.ModelAdmin):
    list_display = ('title', 'youtube_url', 'is_active', 'order')
    list_display_links = ('title',)
    list_editable = ('is_active', 'order')

@admin.register(FactoryCTA)
class FactoryCTAAdmin(admin.ModelAdmin):
    pass
