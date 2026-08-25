from django.db import models
from core.models import BaseSection
from seo.models import SEOFields
from ckeditor.fields import RichTextField
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill

class BlogCategory(SEOFields, BaseSection):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)

    class Meta:
        verbose_name_plural = "Blog Categories"

    def __str__(self):
        return self.name

class Post(SEOFields, BaseSection):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    category = models.ForeignKey(BlogCategory, related_name='posts', on_delete=models.CASCADE)
    author = models.CharField(max_length=100, default="Admin")
    content = RichTextField()
    featured_image = ProcessedImageField(upload_to='blog/', processors=[ResizeToFill(800, 500)], format='WEBP', options={'quality': 80}, null=True, blank=True)
    published_date = models.DateField(auto_now_add=True)

    class Meta:
        ordering = ['-published_date']

    def __str__(self):
        return self.title
