from django.conf.urls import url, include
from django.contrib import admin

from request_handler.urls import urlpatterns


urlpatterns = [
    url(r'api/', include(urlpatterns)),
    url(r'', include(admin.site.urls)),

]
