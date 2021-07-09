# Django
from django.contrib import admin
from django.urls import include, path


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(('hitmeapp.index.urls', 'index'), namespace='index')),
]
