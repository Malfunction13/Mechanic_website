from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from home import views as home_views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('home.urls')),
    path('about/', home_views.about, name='about'),
    path('booking/', include('booking.urls'), name='booking'),
    path('services/', include('services.urls'), name='services')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)