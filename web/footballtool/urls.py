from django.contrib import admin
from django.urls import path, include

# for development
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('players.urls')),
]

urlpatterns += staticfiles_urlpatterns()
