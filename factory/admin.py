from django.contrib import admin
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

class FactoryVideoInline(admin.StackedInline):
    model = FactoryVideo
    extra = 1

@admin.register(FactoryVideoSection)
class FactoryVideoSectionAdmin(admin.ModelAdmin):
    inlines = [FactoryVideoInline]

@admin.register(FactoryCTA)
class FactoryCTAAdmin(admin.ModelAdmin):
    pass
