from django.urls import reverse
from django.db import models


class Service(models.Model):
    name = models.CharField(max_length=10, blank=True)
    title = models.CharField(max_length=60, blank=True)
    short_description = models.CharField(max_length=250, blank=True)
    long_description = models.TextField(max_length=1000, blank=True)
    image = models.ImageField(default='service.jpg', upload_to='service_pics')

    def __str__(self):

        return self.name


