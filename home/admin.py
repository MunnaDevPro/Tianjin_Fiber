from django.contrib import admin
from .models import HomeHero, HeroSlide, HomeFactory, HomeFactoryFeature, HomeValues, HomeValueItem, HomeMission

class HeroSlideInline(admin.TabularInline):
    model = HeroSlide
    extra = 1

@admin.register(HomeHero)
class HomeHeroAdmin(admin.ModelAdmin):
    inlines = [HeroSlideInline]

class HomeFactoryFeatureInline(admin.StackedInline):
    model = HomeFactoryFeature
    extra = 1

@admin.register(HomeFactory)
class HomeFactoryAdmin(admin.ModelAdmin):
    inlines = [HomeFactoryFeatureInline]

class HomeValueItemInline(admin.StackedInline):
    model = HomeValueItem
    extra = 1

@admin.register(HomeValues)
class HomeValuesAdmin(admin.ModelAdmin):
    inlines = [HomeValueItemInline]

@admin.register(HomeMission)
class HomeMissionAdmin(admin.ModelAdmin):
    pass
