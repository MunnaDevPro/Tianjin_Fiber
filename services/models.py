from django.db import models
from core.models import SingletonModel, BaseSection
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill

class ServicesHeader(SingletonModel):
    title = models.CharField(max_length=200, default="Manufacturing Services")
    subtitle = models.TextField()
    bg_image = ProcessedImageField(upload_to='services/', processors=[ResizeToFill(1920, 600)], format='WEBP', options={'quality': 80}, null=True, blank=True)

    def __str__(self):
        return self.title

class ServiceItem(BaseSection):
    title = models.CharField(max_length=200)
    description = models.TextField()
    image = ProcessedImageField(upload_to='services/items/', processors=[ResizeToFill(800, 600)], format='WEBP', options={'quality': 80})

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

class BusinessModelSection(SingletonModel):
    title = models.CharField(max_length=200, default="OEM & ODM Solutions")
    subtitle = models.TextField(default="Whether you have your own unique product design or want to leverage our existing high-quality manufacturing lines under your own brand, we offer flexible models to suit your business needs.")

    def __str__(self):
        return self.title

class BusinessModelItem(BaseSection):
    section = models.ForeignKey(BusinessModelSection, related_name='items', on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=100) # e.g. OEM
    full_name = models.CharField(max_length=200) # e.g. Original Equipment Manufacturer
    quote = models.CharField(max_length=200) # e.g. "Your Design, Our Manufacturing"
    description = models.TextField()
    icon = models.CharField(max_length=50, default="briefcase")
    features = models.TextField(help_text="Format: Key: Value, one per line. E.g. Design: Yours", blank=True)
    color_theme = models.CharField(max_length=50, choices=[('blue', 'Blue'), ('magenta', 'Magenta')], default='blue')

    def __str__(self):
        return self.title
        
    def get_features_list(self):
        feature_list = []
        for line in self.features.split('\n'):
            if ':' in line:
                key, val = line.split(':', 1)
                feature_list.append({"key": key.strip(), "value": val.strip()})
        return feature_list
