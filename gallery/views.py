import os
from collections import namedtuple

from django.conf import settings
from django.shortcuts import render, redirect

from gallery.constants import IMAGE_EXTENSIONS
from gallery.models import Image
from gallery.utils import get_parent_path, get_image_list, url_compliant_path


# create image named tuple
ImageTuple = namedtuple('ImagePaths', ['absolute_path', 'relative_path', 'filename'])

def get_path_url(path):
    return "%2F" + path


def image_detail(request, path):
    image_name = os.path.basename(path)
    absolute_image_dir_path = os.path.dirname(path)
    relative_image_path = os.path.join(settings.MEDIA_URL, image_name)
    
    if not os.path.exists(path):
        return render(request, 'gallery/404.html', status=404)
    
    if not image_name.lower().endswith(tuple(IMAGE_EXTENSIONS)):
        return render(request, 'gallery/404.html', status=404)
    
    context = {
        "image_path": relative_image_path,
        "image_name": image_name,
        "parent_path": get_parent_path(path),
        "images": get_image_list(absolute_image_dir_path),
    }

    return render(request, 'gallery/image.html', context)


def image_list_from_query(request):
    query = request.GET.get('q')
    
    images = Image.objects.filter(filename__contains=query)
    
    images_paths = [
        ImageTuple(
            absolute_path=get_path_url(os.path.join(settings.MEDIA_ROOT, image.path)),
            relative_path=os.path.join(settings.MEDIA_URL, image.filename),
            filename=image.filename,
        )
        for image in images
    ]

    context = {
        'directories': [],
        'images': images_paths,
        'parent_path': settings.MEDIA_ROOT,
    }
    return render(request, 'gallery/image_list.html', context)


def image_list_from_path(request, path=""):
    absolute_path = os.path.join(settings.MEDIA_ROOT, path) if not path else path
    
    if absolute_path == settings.MEDIA_ROOT:
        return redirect('image_list')
    
    if not os.path.exists(absolute_path):
        return render(request, 'gallery/404.html', status=404)
    
    items = os.listdir(absolute_path)
    directories = [
        (os.path.join(absolute_path, directory), directory)
        for directory in items
        if os.path.isdir(os.path.join(absolute_path, directory))
    ]
    images = get_image_list(absolute_path)
    images_paths = [
        ImageTuple(
            absolute_path=get_path_url(image),
            relative_path=os.path.join(settings.MEDIA_URL, image),
            filename=image
        )
        for image in images
    ]
    
    context = {
        'directories': directories,
        'images': images_paths,
        'parent_path': get_parent_path(path),
        'absolute_path': absolute_path,
    }
    return render(request, 'gallery/image_list.html', context)



def image_list(request, path=""):
    if request.GET.get('q'):
        return image_list_from_query(request)
    
    return image_list_from_path(request, path)
