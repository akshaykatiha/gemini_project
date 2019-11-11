from django.contrib import admin
from django.urls import path, include
from services import urls as services_urls
from django.conf import settings
from django.conf.urls.static import static



urlpatterns = [
    path('admin/', admin.site.urls),
    path('services/', include(services_urls)),
    path('accounts/', include('django.contrib.auth.urls')),    
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


# if settings.DEBUG:
#     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
# This declaration is depriated from Django > 1.7

# Add Django site authentication urls (for login, logout, password management)
urlpatterns += [
    path('accounts/', include('django.contrib.auth.urls')),

]
