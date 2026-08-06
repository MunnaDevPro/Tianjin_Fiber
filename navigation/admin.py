from django.contrib import admin
from .models import Navbar, Footer, SocialLink

@admin.register(Navbar)
class NavbarAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'cta_text')
    
@admin.register(Footer)
class FooterAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'email', 'phone')

@admin.register(SocialLink)
class SocialLinkAdmin(admin.ModelAdmin):
    list_display = ('platform', 'url', 'is_active', 'order')
    list_editable = ('is_active', 'order')
