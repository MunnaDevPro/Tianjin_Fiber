from .models import SiteSettings, Category

def site_settings(request):
    settings = SiteSettings.objects.first()
    return {'site_settings': settings}

def categories_processor(request):
    return {'categories': Category.objects.all()}
