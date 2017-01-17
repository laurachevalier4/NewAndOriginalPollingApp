from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r'^meet/', include('meet.urls')),
    url(r'^admin/', admin.site.urls),
]
