from django.conf.urls import url
from request_handler.views import (
    AllowedRequestViewSet,
    ExternalRequestViewSet,
    Identify
)
from rest_framework_expiring_authtoken import views


urlpatterns = [
    url('^allowed_requests/$', AllowedRequestViewSet.as_view(), name='allowed_view'),
    url('^external_requests/$', ExternalRequestViewSet.as_view(), name='external_view'),
    url('^identify/$', Identify.as_view(), name='identify_view'),
    url('^auth/', views.obtain_expiring_auth_token, name='auth_view'),
]
