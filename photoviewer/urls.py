from django.urls import path, re_path
from gallery import views as gallery_views
urlpatterns = [
    re_path(r'^(?P<path>.+\.(?:png|jpg|jpeg|gif))/$', gallery_views.image_detail, name='image_detail'),
    path('', gallery_views.image_list, name='image_list'),  # Root URL
    path('<path:path>/', gallery_views.image_list, name='image_list'),  # Dynamic paths
]


from django.conf import settings
from django.conf.urls.static import static

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)