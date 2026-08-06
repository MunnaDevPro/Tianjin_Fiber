from django.db import models
from core.models import SingletonModel, BaseSection
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill

class HomeHero(SingletonModel):
    title_black = models.CharField(max_length=100, default="Uncompromising")
    title_magenta = models.CharField(max_length=100, default="Quality.")
    title_gold = models.CharField(max_length=100, default="Protect.")
    title_prefix = models.CharField(max_length=100, default="Engineered to")
    subtitle = models.TextField(default="Direct from our 50,000 sqm production facility...")
    
    badge_text = models.CharField(max_length=50, default="Global Source Manufacturer")
    
    primary_cta_text = models.CharField(max_length=50, default="Explore Products")
    primary_cta_link = models.CharField(max_length=200, default="#products")
    
    secondary_cta_text = models.CharField(max_length=50, default="Request a Quote")
    secondary_cta_link = models.CharField(max_length=200, default="/contact/")

    class Meta:
        verbose_name = "Home Hero Section"
        verbose_name_plural = "Home Hero Section"

class HeroSlide(BaseSection):
    hero = models.ForeignKey(HomeHero, related_name='slides', on_delete=models.CASCADE)
    image = ProcessedImageField(upload_to='home/hero/', processors=[ResizeToFill(1920, 1080)], format='WEBP', options={'quality': 80})
    alt_text = models.CharField(max_length=100, default="Hero Slide")

class HomeFactory(SingletonModel):
    title = models.CharField(max_length=200, default="State-of-the-art Production Facilities")
    description = models.TextField()
    
    img_top_left = ProcessedImageField(upload_to='home/factory/', processors=[ResizeToFill(800, 600)], format='WEBP', null=True, blank=True)
    img_top_right = ProcessedImageField(upload_to='home/factory/', processors=[ResizeToFill(400, 600)], format='WEBP', null=True, blank=True)
    img_bottom_left = ProcessedImageField(upload_to='home/factory/', processors=[ResizeToFill(400, 600)], format='WEBP', null=True, blank=True)
    
    box_percentage = models.CharField(max_length=10, default="100%")
    box_text = models.CharField(max_length=100, default="Quality Inspected Before Shipping")

    class Meta:
        verbose_name = "Home Factory Section"
        verbose_name_plural = "Home Factory Section"

class HomeFactoryFeature(BaseSection):
    factory = models.ForeignKey(HomeFactory, related_name='features', on_delete=models.CASCADE)
    icon = models.CharField(max_length=50, default="factory")
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=200)

class HomeValues(SingletonModel):
    title = models.CharField(max_length=200, default="Our Core Values")
    description = models.TextField()
    image = ProcessedImageField(upload_to='home/values/', processors=[ResizeToFill(800, 600)], format='WEBP', null=True, blank=True)

    class Meta:
        verbose_name = "Home Values Section"
        verbose_name_plural = "Home Values Section"

class HomeValueItem(BaseSection):
    values_section = models.ForeignKey(HomeValues, related_name='items', on_delete=models.CASCADE)
    icon = models.CharField(max_length=50, default="shield")
    title = models.CharField(max_length=100)
    description = models.TextField()

class HomeMission(SingletonModel):
    title = models.CharField(max_length=200, default="Forging the strongest connections worldwide.")
    description = models.TextField()
    image = ProcessedImageField(upload_to='home/mission/', processors=[ResizeToFill(1200, 800)], format='WEBP', null=True, blank=True)

    stat1_number = models.CharField(max_length=20, default="20+")
    stat1_text = models.CharField(max_length=50, default="Years Experience")
    
    stat2_number = models.CharField(max_length=20, default="50+")
    stat2_text = models.CharField(max_length=50, default="Countries Served")
    
    stat3_number = models.CharField(max_length=20, default="100%")
    stat3_text = models.CharField(max_length=50, default="Quality Assured")

    class Meta:
        verbose_name = "Home Mission Section"
        verbose_name_plural = "Home Mission Section"
