import os
import urllib.parse

from gallery.constants import IMAGE_EXTENSIONS


def get_parent_path(path):
    return "/".join(path.split("/")[:-1]) if path else None


def get_image_list(path: str) -> list[str]:
    """ Return a list of images in the given directory
    
    :param path: The directory to search for images
    :return: A list of images in the given directory
    """
    items = os.listdir(path)
    images = [
        f for f in items
        if f.lower().endswith(tuple(IMAGE_EXTENSIONS))
    ]
    return images


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


