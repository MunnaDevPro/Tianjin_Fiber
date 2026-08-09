from django.core.cache import cache
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from navigation.models import Navbar, Footer, SocialLink
from products.models import Category
from contactapp.models import ContactPageSettings

def global_settings(request):
    try:
        navbar = Navbar.objects.first()
        footer = Footer.objects.first()
        contact_settings = ContactPageSettings.objects.first()
        social_links = list(SocialLink.objects.filter(is_active=True))
        categories = list(Category.objects.filter(is_active=True))
        
        return {
            'navbar': navbar,
            'footer': footer,
            'contact_settings': contact_settings,
            'social_links': social_links,
            'categories': categories,
        }
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


def admin_dashboard_metrics(request):
    if not request.path.startswith('/dashboard/'):
        return {}

    try:
        import sys
        import django
        from django.conf import settings
        from django.contrib.auth.models import User
        from products.models import Product, Category
        from contactapp.models import ContactMessage
        from certificates.models import Certificate
        from activitylog.models import UserSession
        
        # Try importing from optional modules safely
        try:
            from services.models import ServiceItem
            total_services = ServiceItem.objects.count()
        except ImportError:
            total_services = 0
            
        try:
            from about.models import TeamMember
            total_team_members = TeamMember.objects.count()
        except ImportError:
            total_team_members = 0

        total_products = Product.objects.count()
        total_messages = ContactMessage.objects.count()
        total_certificates = Certificate.objects.count()
        total_users = User.objects.count()

        recent_messages = list(ContactMessage.objects.order_by('-created_at')[:5])

        category_data = []
        for cat in Category.objects.all():
            category_data.append({
                'name': cat.name,
                'count': cat.products.count()
            })

        # Gather System Info
        db_engine = settings.DATABASES.get('default', {}).get('ENGINE', '').split('.')[-1]
        system_info = {
            'django_version': django.get_version(),
            'python_version': sys.version.split()[0],
            'timezone': settings.TIME_ZONE,
            'db_engine': db_engine.upper() if db_engine else 'SQLITE',
            'debug_mode': settings.DEBUG,
        }

        return {
            'admin_metrics': {
                'total_products': total_products,
                'total_messages': total_messages,
                'total_certificates': total_certificates,
                'total_users': total_users,
                'total_services': total_services,
                'total_team_members': total_team_members,
                'recent_messages': recent_messages,
                'category_data': category_data,
                'system_info': system_info,
            }
        }
    except Exception as e:
        import logging
        logger = logging.getLogger(__name__)
        logger.error(f"Error in admin_dashboard_metrics context processor: {e}")
        return {}

