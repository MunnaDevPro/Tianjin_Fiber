from django.db import models
from core.models import SingletonModel, BaseSection
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill

class CertificatesHeader(SingletonModel):
    title = models.CharField(max_length=200, default="Certified Excellence")
    subtitle = models.TextField()
    bg_image = ProcessedImageField(upload_to='certificates/', processors=[ResizeToFill(1920, 1080)], format='WEBP', null=True, blank=True)

class Certificate(BaseSection):
    title = models.CharField(max_length=100)
    image = ProcessedImageField(upload_to='certificates/gallery/', processors=[ResizeToFill(800, 1200)], format='WEBP')
    
class CertificatesCTA(SingletonModel):
    title = models.CharField(max_length=200, default="Need Details About Our Standards?")
    description = models.TextField()
    btn1_text = models.CharField(max_length=50, default="Request Documents")
    btn1_link = models.CharField(max_length=200, default="/contact/")
    btn2_text = models.CharField(max_length=50, default="Back to Services")
    btn2_link = models.CharField(max_length=200, default="/services/")
