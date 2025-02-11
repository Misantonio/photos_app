import os

from django.core.management.base import BaseCommand

from gallery.models import Image
from gallery.utils import get_all_images_list
from photoviewer.settings import MEDIA_ROOT

class Command(BaseCommand):
    help = "Record images in the database"

    def handle(self, *args, **options):
        images_paths = get_all_images_list(MEDIA_ROOT)
        for image_path in images_paths:
            filename = os.path.basename(image_path)
            Image.objects.get_or_create(filename=filename, path=image_path)
        self.stdout.write(
            self.style.SUCCESS(f"Recorded {len(images_paths)} images")
        )
        
    