import os
import urllib.parse

from gallery.constants import IMAGE_EXTENSIONS
from photoviewer.settings import MEDIA_ROOT


def get_parent_path(path: str):
    """ Return the parent path of the given path """
    parent_path = os.path.dirname(path).replace(MEDIA_ROOT, '')
    if not parent_path:
        return '/'
    return parent_path


def get_image_list(path: str) -> list[str]:
    """ Return a list of images in the given directory
    
    :param path: The directory to search for images
    :return: A list of images in the given directory
    """
    items = os.listdir(path)
    return [
        item
        for item in items
        if item.lower().endswith(tuple(IMAGE_EXTENSIONS))
    ]


def get_all_images_list(path: str) -> list[str]:
    """ Return a list of images paths in the given directory and its
    subdirectories relative to the given directory
    
    :param path: The directory to search for images
    :return: A list of images in the given directory
    """
    images = []
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.lower().endswith(tuple(IMAGE_EXTENSIONS)):
                images.append(os.path.relpath(os.path.join(root, file), path))
    return images


def url_compliant_path(path: str):
    return urllib.parse.quote(path)


