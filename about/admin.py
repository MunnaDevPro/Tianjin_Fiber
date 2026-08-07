from django.contrib import admin
from django.utils.html import format_html
from .models import AboutHeader, AboutStory, AboutStoryPoint, AboutExcellence, AboutExcellenceCard, TeamMember, Testimonial

@admin.register(AboutHeader)
class AboutHeaderAdmin(admin.ModelAdmin):
    pass

class AboutStoryPointInline(admin.StackedInline):
    model = AboutStoryPoint
    extra = 1

@admin.register(AboutStory)
class AboutStoryAdmin(admin.ModelAdmin):
    inlines = [AboutStoryPointInline]

class AboutExcellenceCardInline(admin.StackedInline):
    model = AboutExcellenceCard
    extra = 1

@admin.register(AboutExcellence)
class AboutExcellenceAdmin(admin.ModelAdmin):
    inlines = [AboutExcellenceCardInline]

@admin.register(TeamMember)
class TeamMemberAdmin(admin.ModelAdmin):
    list_display = ('image_preview', 'name', 'role', 'is_active', 'order')
    list_display_links = ('image_preview', 'name')
    list_editable = ('is_active', 'order')

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="width: 50px; height: 50px; object-fit: cover; border-radius: 8px; border: 1px solid #e2e8f0;" />', obj.image.url)
        return ""
    image_preview.short_description = 'Photo'

@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ('image_preview', 'name', 'role', 'is_active', 'order')
    list_display_links = ('image_preview', 'name')
    list_editable = ('is_active', 'order')

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="width: 50px; height: 50px; object-fit: cover; border-radius: 8px; border: 1px solid #e2e8f0;" />', obj.image.url)
        return ""
    image_preview.short_description = 'Photo'
