from django.db import models
from core.models import SingletonModel
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill

class ContactPageSettings(SingletonModel):
    title = models.CharField(max_length=200, default="Contact Us")
    subtitle = models.TextField(default="Get in touch with our team.")
    bg_image = ProcessedImageField(upload_to='contact/', processors=[ResizeToFill(1920, 600)], format='WEBP', options={'quality': 80}, null=True, blank=True)
    
    address = models.TextField(default="123 Industrial Ave, Tianjin, China")
    email = models.EmailField(default="info@tianjinfibernet.com")
    phone = models.CharField(max_length=50, default="+86 123 4567 8900")
    business_hours = models.TextField(default="Mon-Fri: 9:00 AM - 6:00 PM")
    map_iframe = models.TextField(blank=True, help_text="Google Maps iframe embed code")

    def __str__(self):
        return "Contact Page Settings"

class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True)
    subject = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.subject}"
