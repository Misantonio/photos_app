from enum import Enum


class ImageExtension(Enum):
    JPG = "jpg"
    JPEG = "jpeg"
    PNG = "png"
    GIF = "gif"
    
    @classmethod
    def get_extensions(cls):
        return [extension.value for extension in cls]
    
    
IMAGE_EXTENSIONS = ImageExtension.get_extensions()
