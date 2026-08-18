from django.db import models
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill

class Customer(models.Model):
    name = models.CharField(max_length=150, help_text="Short name or username")
    full_name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=20)
    address = models.TextField()
    photo = ProcessedImageField(
        upload_to='customers/photos/',
        processors=[ResizeToFill(400, 400)],
        format='WEBP',
        options={'quality': 85},
        blank=True,
        null=True
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.full_name
