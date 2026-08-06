from django.contrib import admin
from django.utils.html import format_html
from .models import Category, Product, ProductImage

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1
    fields = ('image', 'image_preview', 'alt_text', 'order')
    readonly_fields = ('image_preview',)

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="100" />', obj.image.url)
        return ""
    image_preview.short_description = 'Preview'

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_active', 'order', 'hero_preview')
    list_editable = ('is_active', 'order')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)
    fieldsets = (
        (None, {
            'fields': ('name', 'slug', 'is_active', 'order')
        }),
        ('Hero Section', {
            'fields': ('hero_text', 'hero_image', 'hero_image_alt')
        }),
        ('SEO Settings', {
            'fields': ('meta_title', 'meta_description', 'meta_keywords', 'canonical_url', 'og_title', 'og_description', 'og_image', 'robots_index', 'robots_follow'),
            'classes': ('collapse',)
        }),
    )

    def hero_preview(self, obj):
        if obj.hero_image:
            return format_html('<img src="{}" width="100" />', obj.hero_image.url)
        return ""
    hero_preview.short_description = 'Hero Image'

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'is_active', 'order', 'main_image_preview')
    list_editable = ('is_active', 'order')
    list_filter = ('category', 'is_active')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name', 'description')
    inlines = [ProductImageInline]
    fieldsets = (
        (None, {
            'fields': ('category', 'name', 'slug', 'is_active', 'order')
        }),
        ('Content', {
            'fields': ('description', 'features')
        }),
        ('Media', {
            'fields': ('main_image', 'main_image_alt')
        }),
        ('SEO Settings', {
            'fields': ('meta_title', 'meta_description', 'meta_keywords', 'canonical_url', 'og_title', 'og_description', 'og_image', 'robots_index', 'robots_follow'),
            'classes': ('collapse',)
        }),
    )

    def main_image_preview(self, obj):
        if obj.main_image:
            return format_html('<img src="{}" width="100" />', obj.main_image.url)
        return ""
    main_image_preview.short_description = 'Image'
