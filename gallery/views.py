import os
from collections import namedtuple

from django.conf import settings
from django.shortcuts import render, redirect
from django.views.generic import View

from gallery.constants import IMAGE_EXTENSIONS
from gallery.models import Image
from gallery.utils import get_parent_path, get_image_list



def get_relative_path(path, item=None, root=settings.MEDIA_ROOT):
    path = path.replace(root, '')
    if item:
        path = os.path.join(path, item)
    return path


class GalleryView(View):
    def dispatch(self, request, *args, **kwargs):
        path = kwargs.get('path', '')
        
        if request.GET.get('q'):
            return self._images_from_query(request)

        if path.lower().endswith(tuple(IMAGE_EXTENSIONS)):
            return self._image_detail(request, path)
        
        return self._images_from_path(request, path)
        
    def _images_from_path(self, request, path=''):
        if path == '/':
            return redirect('gallery')
        
        path = path.lstrip('/')
        absolute_path = os.path.join(settings.MEDIA_ROOT, path)

        if not os.path.exists(absolute_path):
            return render(request, 'gallery/404.html', status=404)
    
        items = os.listdir(absolute_path)
        directories = [
            {
                "relative_path": get_relative_path(absolute_path, directory),
                "name": directory
            }
            for directory in items
            if os.path.isdir(os.path.join(absolute_path, directory))
        ]
        images = get_image_list(absolute_path)
        images_paths = []
        for image in images:
            relative_path = get_relative_path(absolute_path, image)
            media_path = settings.MEDIA_URL + relative_path.lstrip('/')
            images_paths.append(
                {
                    "absolute_path": relative_path,
                    "media_path": media_path,
                    "filename": image,
                }
            )
        
        context = {
            'directories': directories,
            'images': images_paths,
            'parent_path': get_parent_path(absolute_path),
            'absolute_path': absolute_path,
        }
        return render(request, 'gallery/image_list.html', context)
    
    def _images_from_query(self, request):
        query = request.GET.get('q')
        images = Image.objects.filter(filename__contains=query)
    
        images_paths = []
        for image in images:
            relative_path = get_relative_path(image.path)
            images_paths.append(
                {
                    "relative_path": relative_path,
                    "media_path": os.path.join(settings.MEDIA_URL, relative_path),
                    "filename": image.filename,
                }
            )
        
        context = {
            'directories': [],
            'images': images_paths,
            'parent_path': settings.MEDIA_ROOT,
        }
        return render(request, 'gallery/image_list.html', context)
    
    def _image_detail(self, request, path):
        image_name = os.path.basename(path)
        absolute_path = os.path.join(settings.MEDIA_ROOT, path)
        
        if not os.path.exists(absolute_path):
            return render(request, 'gallery/404.html', status=404)

        absolute_dir_path = os.path.dirname(absolute_path)
        relative_dir = get_relative_path(path)
        media_path = os.path.join(settings.MEDIA_URL, relative_dir)
        
        context = {
            "media_path": media_path,
            "image_name": image_name,
            "parent_path": get_parent_path(path),
            "images": get_image_list(absolute_dir_path),
        }
        return render(request, 'gallery/image.html', context)
    
