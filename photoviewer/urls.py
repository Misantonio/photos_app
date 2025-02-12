from django.urls import path, re_path
from gallery import views as gallery_views
from gallery.views import GalleryView, OpenImageFolderView
urlpatterns = [
    path('', GalleryView.as_view(), name='gallery'),  # Root URL
    path('open-folder/', OpenImageFolderView.as_view(), name='open_folder'),
    path('<path:path>/', GalleryView.as_view(), name='gallery'),
]


from django.conf import settings
from django.conf.urls.static import static

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)