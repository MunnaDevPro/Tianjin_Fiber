from django.db import models
from core.models import SingletonModel, BaseSection
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill

class ServicesHeader(SingletonModel):
    title = models.CharField(max_length=200, default="Manufacturing Services")
    subtitle = models.TextField()
    bg_image = ProcessedImageField(upload_to='services/', processors=[ResizeToFill(1920, 600)], format='WEBP', null=True, blank=True)

    def __str__(self):
        return self.title

class ServiceItem(BaseSection):
    title = models.CharField(max_length=200)
    description = models.TextField()
    image = ProcessedImageField(upload_to='services/items/', processors=[ResizeToFill(800, 600)], format='WEBP')

    def __str__(self):
        return self.title

class ProcessSection(SingletonModel):
    title = models.CharField(max_length=200, default="Our Comprehensive Manufacturing")
    subtitle = models.TextField()

    def __str__(self):
        return self.title

class ProcessStep(BaseSection):
    process = models.ForeignKey(ProcessSection, related_name='steps', on_delete=models.CASCADE)
    icon = models.CharField(max_length=50, default="check-circle")
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=200)

    def __str__(self):
        return self.title

class ServicesCTA(SingletonModel):
    title = models.CharField(max_length=200, default="Need a Custom Specification?")
    description = models.TextField()
    btn_text = models.CharField(max_length=50, default="Contact Engineering")
    btn_link = models.CharField(max_length=200, default="/contact/")

    def __str__(self):
        return self.title
