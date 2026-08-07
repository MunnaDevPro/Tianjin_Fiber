from django.db import models
from core.models import SingletonModel, BaseSection
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill

class AboutHeader(SingletonModel):
    title = models.CharField(max_length=200, default="Building the Future of Global Manufacturing")
    subtitle = models.TextField()
    bg_image = ProcessedImageField(upload_to='about/', processors=[ResizeToFill(1920, 600)], format='WEBP', null=True, blank=True)

    def __str__(self):
        return self.title

class AboutStory(SingletonModel):
    title = models.CharField(max_length=200, default="A Legacy of", help_text="The first part of the title (e.g. 'A Legacy of')")
    title_highlight = models.CharField(max_length=200, default="Strength", help_text="The word that will be colored differently (e.g. 'Strength')")
    description = models.TextField()
    image = ProcessedImageField(upload_to='about/', processors=[ResizeToFill(800, 600)], format='WEBP', null=True, blank=True)

    def __str__(self):
        return f"{self.title} {self.title_highlight}"

class AboutStoryPoint(BaseSection):
    story = models.ForeignKey(AboutStory, related_name='points', on_delete=models.CASCADE)
    icon = models.CharField(max_length=50, default="check-circle-2", help_text="Lucide icon name (e.g., check-circle-2)")
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=200)

    def __str__(self):
        return self.title

class AboutExcellence(SingletonModel):
    title = models.CharField(max_length=200, default="Engineering", help_text="The first part of the title (e.g. 'Engineering')")
    title_highlight = models.CharField(max_length=200, default="Excellence", help_text="The word that will be colored gold (e.g. 'Excellence')")
    title_suffix = models.CharField(max_length=200, default="at Scale", blank=True, help_text="The last part of the title (e.g. 'at Scale')")
    description = models.TextField()
    
    stat1_number = models.CharField(max_length=20, default="500+")
    stat1_text = models.CharField(max_length=50, default="Monthly Tons")
    
    stat2_number = models.CharField(max_length=20, default="100%")
    stat2_text = models.CharField(max_length=50, default="QC Passed")
    
    stat3_number = models.CharField(max_length=20, default="50+")
    stat3_text = models.CharField(max_length=50, default="Countries")

    def __str__(self):
        return f"{self.title} {self.title_highlight}"

class AboutExcellenceCard(BaseSection):
    excellence = models.ForeignKey(AboutExcellence, related_name='cards', on_delete=models.CASCADE)
    icon = models.CharField(max_length=50, default="shield-check")
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=200)

    def __str__(self):
        return self.title

class TeamMember(BaseSection):
    name = models.CharField(max_length=100)
    role = models.CharField(max_length=100)
    image = ProcessedImageField(upload_to='about/team/', processors=[ResizeToFill(400, 500)], format='WEBP')
    email = models.EmailField(blank=True)
    twitter = models.URLField(blank=True)
    linkedin = models.URLField(blank=True)

    def __str__(self):
        return self.name

class Testimonial(BaseSection):
    name = models.CharField(max_length=100)
    role = models.CharField(max_length=100)
    image = ProcessedImageField(upload_to='about/testimonials/', processors=[ResizeToFill(150, 150)], format='WEBP', null=True, blank=True)
    text = models.TextField()

    def __str__(self):
        return self.name
