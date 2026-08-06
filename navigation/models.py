from django.db import models
from core.models import SingletonModel, BaseSection
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFit

class Navbar(SingletonModel):
    logo = ProcessedImageField(upload_to='navigation/', processors=[ResizeToFit(300, 100)], format='WEBP', options={'quality': 90}, blank=True, null=True)
    logo_alt = models.CharField(max_length=100, default="Site Logo")
    cta_text = models.CharField(max_length=50, default="Get Quote")
    cta_link = models.CharField(max_length=200, default="/contact/")

    class Meta:
        verbose_name = "Navbar Settings"
        verbose_name_plural = "Navbar Settings"

    def __str__(self):
        return "Navbar Configuration"

class Footer(SingletonModel):
    logo = ProcessedImageField(upload_to='navigation/', processors=[ResizeToFit(300, 100)], format='WEBP', options={'quality': 90}, blank=True, null=True)
    about_text = models.TextField(blank=True, default="Brief description about the company for the footer.")
    copyright_text = models.CharField(max_length=200, default="© 2026 Company Name. All Rights Reserved.")
    
    # Address details
    address = models.TextField(blank=True)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=50, blank=True)

    class Meta:
        verbose_name = "Footer Settings"
        verbose_name_plural = "Footer Settings"

    def __str__(self):
        return "Footer Configuration"

class SocialLink(BaseSection):
    platform = models.CharField(max_length=50, help_text="e.g., Facebook, Twitter, LinkedIn")
    icon_class = models.CharField(max_length=50, blank=True, null=True, help_text="FontAwesome or Lucide icon name (e.g., facebook, twitter, linkedin)")
    url = models.URLField()

    def save(self, *args, **kwargs):
        if not self.icon_class and self.platform:
            platform_lower = self.platform.lower()
            if 'facebook' in platform_lower:
                self.icon_class = 'facebook'
            elif 'twitter' in platform_lower or 'x.com' in platform_lower:
                self.icon_class = 'twitter'
            elif 'linkedin' in platform_lower:
                self.icon_class = 'linkedin'
            elif 'youtube' in platform_lower:
                self.icon_class = 'youtube'
            elif 'instagram' in platform_lower:
                self.icon_class = 'instagram'
            else:
                self.icon_class = 'link'
        super().save(*args, **kwargs)

    def __str__(self):
        return self.platform
