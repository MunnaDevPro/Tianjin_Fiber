from django.db import models
from django.utils.translation import gettext_lazy as _

class SEOFields(models.Model):
    meta_title = models.CharField(_("Meta Title"), max_length=255, blank=True, help_text=_("Optimal length is 50-60 characters."))
    meta_description = models.TextField(_("Meta Description"), blank=True, help_text=_("Optimal length is 150-160 characters."))
    meta_keywords = models.CharField(_("Meta Keywords"), max_length=255, blank=True, help_text=_("Comma-separated keywords."))
    canonical_url = models.URLField(_("Canonical URL"), blank=True, help_text=_("Leave blank to use the current page URL."))
    
    # Open Graph (Social Media)
    og_title = models.CharField(_("OG Title"), max_length=255, blank=True, help_text=_("Title for Facebook/LinkedIn sharing."))
    og_description = models.TextField(_("OG Description"), blank=True, help_text=_("Description for Facebook/LinkedIn sharing."))
    og_image = models.ImageField(_("OG Image"), upload_to='seo/og/', blank=True, null=True, help_text=_("Image for Facebook/LinkedIn sharing (1200x630px recommended)."))
    
    # Robots
    robots_index = models.BooleanField(_("Index"), default=True, help_text=_("Allow search engines to index this page."))
    robots_follow = models.BooleanField(_("Follow"), default=True, help_text=_("Allow search engines to follow links on this page."))

    class Meta:
        abstract = True
