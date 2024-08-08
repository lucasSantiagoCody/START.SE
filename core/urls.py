from django.conf.urls.static import static
from django.urls import path, include
from django.conf import settings
from django.contrib import admin

urlpatterns = [
    path('admin/', admin.site.urls),
    path('user/', include('user.urls')),
    path('entrepreneur/', include('entrepreneur.urls')),
    path('investor/', include('investor.urls')),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
