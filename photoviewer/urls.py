from django.urls import path, re_path
from gallery import views as gallery_views
from gallery.views import GalleryView
urlpatterns = [
    path('', GalleryView.as_view(), name='gallery'),  # Root URL
    path('<path:path>/', GalleryView.as_view(), name='gallery'),  # Handles both directories and images
]


from django.conf import settings
from django.conf.urls.static import static

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)