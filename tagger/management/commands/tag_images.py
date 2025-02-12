from django.core.management.base import BaseCommand

from gallery.models import Image
from tagger.models import Tag
from tagger.neural_networks.clip import ClipTagger
from tagger.corpus import ES_LABELS, EN_LABELS


TAGGERS = {
    'clip': ClipTagger,
}

LABELS_LANGUAGES = {
    'en': EN_LABELS,
    'es': ES_LABELS,
}


class Command(BaseCommand):
    help = "Tag images in the database"
    
    def add_arguments(self, parser):
        parser.add_argument(
            '--force-tag',
            dest='force_tag',
            help='Tells command to re-tag images even if they are already tagged',
            action='store',
            default=False,
        )
        parser.add_argument(
            '--taggers',
            dest='taggers',
            help='Comma-separated list of taggers to use',
            action='store',
            default='clip',
        )
        parser.add_argument(
            '--labels-lang',
            dest='labels_lang',
            help='Comma-separated list of taggers to use',
            action='store',
            default='es',
        )

    def handle(self, *args, **options):
        force_tag = options['force_tag']
        taggers = options['taggers'].split(',')
        langs = options['labels_lang'].split(',')
        
        labels = []
        for lang in langs:
            if lang in LABELS_LANGUAGES:
                labels.extend(LABELS_LANGUAGES[lang])
            else:
                self.stdout.write(
                    self.style.ERROR(f"Labels language '{lang}' not found")
                )
        
        if force_tag:
            self.stdout.write(self.style.WARNING("Forcing re-tagging of images"))
            images = Image.objects.all()
        else:
            images = Image.objects.filter(tagged=False)
            
        try:
            # Iterate over each image and assign a random tag
            for image in images:
                for tagger_name in taggers:
                    threshold = 0.1
                    tagger_class = TAGGERS.get(tagger_name)
                    if tagger_class:
                        tagger = tagger_class(image_path=image.path, dynamic_threshold=threshold, labels=labels)
                        tags = tagger.get_image_tags()

                        tag_objs = []
                        for tag_name in tags:
                            self.stdout.write(
                                self.style.SUCCESS(f"Tagging image '{image.filename}' with tag '{tag_name}'")
                            )
                            tag, created = Tag.objects.get_or_create(name=tag_name)
                            tag_objs.append(tag)
                        image.tags.set(tag_objs)
                        image.save()
                    else:
                        self.stdout.write(
                            self.style.ERROR(f"Tagger '{tagger_name}' not found")
                        )
            self.stdout.write(
                self.style.SUCCESS(f"Tagged {len(images)} images with tags")
            )
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f"Error occurred while tagging images: {e}")
            )
