from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from mall.views import index, contact

# The include function in the Django urls module is used to include URL patterns
# from other URL configuration modules into the current one.
urlpatterns = [
    path('admin/', admin.site.urls),
    path('mall/', include('mall.urls')),
    path('item/', include('item.urls')),
    path('dashboard/', include('dashboard.urls')),
    path('inbox/', include('message.urls')),
    path('', index, name='index'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
