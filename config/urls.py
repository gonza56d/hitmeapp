"""Project urls."""

# Django
from django.contrib import admin
from django.urls import include, path


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(('hitmeapp.index.urls', 'index'), namespace='index')),
    path('users/', include(('hitmeapp.users.urls', 'users'), namespace='users')),
    path('asset_services/', include(('hitmeapp.assetservices.urls', 'assetservices'), namespace='assetservices')),
]
