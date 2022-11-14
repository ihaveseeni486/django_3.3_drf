from django.db import models
from django.template.defaultfilters import slugify
from django.urls import reverse

from main import settings


class Phone(models.Model):
    name = models.CharField(max_length=50)
    price = models.IntegerField(null=True)
    image = models.CharField(max_length=150)
    release_date = models.DateField(null=True)
    lte_exists = models.BooleanField(null=True)
    slug = models.SlugField(max_length=200, unique=True, db_index=True, verbose_name="URL")

    def get_absolute_url(self):
        return reverse('phone_detail', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        return super().save(*args, **kwargs)

