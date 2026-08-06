from django.db import models
from ckeditor.fields import RichTextField
from imagekit.models import ProcessedImageField, ImageSpecField
from imagekit.processors import ResizeToFill
from seo.models import SEOFields
from core.models import BaseSection

class Category(SEOFields, BaseSection):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    hero_text = models.CharField(max_length=255, help_text="Text to display in the hero section for this category.")
    hero_image = ProcessedImageField(upload_to='categories/', processors=[ResizeToFill(1920, 1080)], format='WEBP', options={'quality': 80}, blank=True, null=True)
    hero_image_alt = models.CharField(max_length=255, default="Category Hero Image", help_text="Alt text for SEO.")

    class Meta:
        verbose_name_plural = "Categories"
        ordering = ['order']

    def __str__(self):
        return self.name

class Product(SEOFields, BaseSection):
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    description = RichTextField()
    
    main_image = ProcessedImageField(upload_to='products/main/', processors=[ResizeToFill(800, 800)], format='WEBP', options={'quality': 85})
    main_image_thumb = ImageSpecField(source='main_image', processors=[ResizeToFill(400, 400)], format='WEBP', options={'quality': 80})
    main_image_alt = models.CharField(max_length=255, default="Product Image", help_text="Alt text for SEO.")

    features = models.TextField(help_text="Enter each feature on a new line", blank=True)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.name

    def get_features_list(self):
        return [f.strip() for f in self.features.split('\n') if f.strip()]

class ProductImage(models.Model):
    product = models.ForeignKey(Product, related_name='additional_images', on_delete=models.CASCADE)
    image = ProcessedImageField(upload_to='products/additional/', processors=[ResizeToFill(800, 800)], format='WEBP', options={'quality': 85})
    image_thumb = ImageSpecField(source='image', processors=[ResizeToFill(200, 200)], format='WEBP', options={'quality': 80})
    alt_text = models.CharField(max_length=255, default="Product Gallery Image")
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"Image for {self.product.name}"
