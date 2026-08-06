from django.db import models
from seo.models import SEOFields

class BaseSection(models.Model):
    is_active = models.BooleanField(default=True, help_text="Toggle to hide/show this section on the frontend.")
    order = models.PositiveIntegerField(default=0, help_text="Ordering of this section on the page (lower numbers appear first).")

    class Meta:
        abstract = True
        ordering = ['order']

class SingletonModel(models.Model):
    """Singleton Django Model"""
    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        self.pk = 1
        super(SingletonModel, self).save(*args, **kwargs)

    @classmethod
    def load(cls):
        obj, created = cls.objects.get_or_create(pk=1)
        return obj
