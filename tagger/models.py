from django.db import models


class Tag(models.Model):
    name = models.CharField(max_length=100, unique=True, db_index=True)  # Indexed for faster tag lookups

    def __str__(self):
        return self.name
