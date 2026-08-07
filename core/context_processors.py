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
        from django.contrib.auth.models import User
        from products.models import Product, Category
        from blog.models import Post, BlogCategory
        from contactapp.models import ContactMessage
        from certificates.models import Certificate

        total_products = Product.objects.count()
        total_posts = Post.objects.count()
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

        blog_category_data = []
        for cat in BlogCategory.objects.all():
            blog_category_data.append({
                'name': cat.name,
                'count': cat.posts.count()
            })

        return {
            'admin_metrics': {
                'total_products': total_products,
                'total_posts': total_posts,
                'total_messages': total_messages,
                'total_certificates': total_certificates,
                'total_users': total_users,
                'recent_messages': recent_messages,
                'category_data': category_data,
                'blog_category_data': blog_category_data,
            }
        }
    except Exception as e:
        import logging
        logger = logging.getLogger(__name__)
        logger.error(f"Error in admin_dashboard_metrics context processor: {e}")
        return {}

