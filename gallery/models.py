import os

from django.db import models

from tagger.models import Tag


class Image(models.Model):
    filename = models.CharField(max_length=100)  # Store
    path = models.CharField(max_length=500, unique=True)  # Store image path
    uploaded_at = models.DateTimeField(auto_now_add=True)
    tagged = models.BooleanField(default=False)
    tags = models.ManyToManyField(Tag, related_name='images', blank=True)

    def __str__(self):
        return self.filename
