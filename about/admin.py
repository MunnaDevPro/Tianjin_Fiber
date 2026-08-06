from django.contrib import admin
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
    list_display = ('name', 'role', 'is_active', 'order')
    list_editable = ('is_active', 'order')

@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ('name', 'role', 'is_active', 'order')
    list_editable = ('is_active', 'order')
