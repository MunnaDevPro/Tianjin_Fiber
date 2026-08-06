from django.db import models
from core.models import SingletonModel, BaseSection
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill

class FactoryHeader(SingletonModel):
    title = models.CharField(max_length=200, default="State-of-the-Art Manufacturing")
    subtitle = models.TextField()
    bg_image = ProcessedImageField(upload_to='factory/', processors=[ResizeToFill(1920, 1080)], format='WEBP', null=True, blank=True)

class FactoryGallerySection(SingletonModel):
    title = models.CharField(max_length=200, default="Explore Our Factory Gallery")
    description = models.TextField()

class FactoryImage(BaseSection):
    gallery = models.ForeignKey(FactoryGallerySection, related_name='images', on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField()
    image = ProcessedImageField(upload_to='factory/gallery/', processors=[ResizeToFill(800, 600)], format='WEBP')
    image_full = ProcessedImageField(upload_to='factory/gallery/full/', processors=[ResizeToFill(1600, 1200)], format='WEBP')

class FactoryVideoSection(SingletonModel):
    title = models.CharField(max_length=200, default="Watch Our Manufacturing Process")
    description = models.TextField()

class FactoryVideo(BaseSection):
    video_section = models.ForeignKey(FactoryVideoSection, related_name='videos', on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField()
    youtube_url = models.URLField(null=True, blank=True)
    video_file = models.FileField(upload_to='factory/videos/', null=True, blank=True)

class FactoryCTA(SingletonModel):
    title = models.CharField(max_length=200, default="Interested in a Facility Tour?")
    description = models.TextField()
    btn_text = models.CharField(max_length=50, default="Schedule a Tour")
    btn_link = models.CharField(max_length=200, default="/contact/")
