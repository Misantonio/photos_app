import os

from django.db import models


class Image(models.Model):
    filename = models.CharField(max_length=100)  # Store
    path = models.CharField(max_length=500, unique=True)  # Store image path
    uploaded_at = models.DateTimeField(auto_now_add=True)
    tagged = models.BooleanField(default=False)

    def __str__(self):
        return self.filename


class Tag(models.Model):
    name = models.CharField(max_length=100, unique=True)  # Store recognized objects (e.g., "cat", "dog")

    def __str__(self):
        return self.name
    

class ImageTag(models.Model):
    image = models.ForeignKey(Image, on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('image', 'tag')  # Ensure an image-tag pair is unique