from django.core.cache import cache
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from navigation.models import Navbar, Footer, SocialLink
from products.models import Category
from contactapp.models import ContactPageSettings

def global_settings(request):
    cache_key = 'global_settings_context'
    cached_data = cache.get(cache_key)
    if cached_data is not None:
        return cached_data

    try:
        navbar = Navbar.objects.first()
        footer = Footer.objects.first()
        contact_settings = ContactPageSettings.objects.first()
        social_links = list(SocialLink.objects.filter(is_active=True))
        categories = list(Category.objects.filter(is_active=True))
        
        data = {
            'navbar': navbar,
            'footer': footer,
            'contact_settings': contact_settings,
            'social_links': social_links,
            'categories': categories,
        }
        cache.set(cache_key, data, 900)  # Cache for 15 minutes
        return data
    except Exception:
        return {
            'navbar': None,
            'footer': None,
            'contact_settings': None,
            'social_links': [],
            'categories': [],
        }

@receiver([post_save, post_delete], sender=Navbar)
@receiver([post_save, post_delete], sender=Footer)
@receiver([post_save, post_delete], sender=ContactPageSettings)
@receiver([post_save, post_delete], sender=SocialLink)
@receiver([post_save, post_delete], sender=Category)
def clear_global_settings_cache(sender, **kwargs):
    cache.delete('global_settings_context')

