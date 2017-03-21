import os
import platform
import psutil
import sys
from io import StringIO

from rest_framework import generics, views
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework import status
from rest_framework.settings import api_settings

from request_handler.commands import (
    call_windows,
)
from request_handler.models import AllowedRequest, ExternalRequest
from request_handler.serializers import (
    SignalSerializer,
    WindowsRequestSerializer,
    ExternalRequestSerializer,
)


class Identify(views.APIView):
    """
    View identifying OS and platform that project runs on.
    """
    def get(self, request):
        return Response(
            {
                'system': platform.system(),
                'name': os.name,
                'release': platform.release(),
                'cpu': psutil.cpu_freq()[2],
                'cores': psutil.cpu_count(),

                'memory': psutil.virtual_memory()[0],
            }
        )


class AllowedRequestViewSet(generics.RetrieveAPIView,
                            generics.CreateAPIView,
                            views.APIView):

    """
    ViewSet handling incoming signals.

    retrieve: get allowed requests.
    create: perform posted signal action.
    """

    queryset = AllowedRequest.objects.none()

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return SignalSerializer
        else:
            return WindowsRequestSerializer

    def get_object(self):
        try:
            allowed = AllowedRequest.objects.get(id=1)
        except AllowedRequest.DoesNotExist:
            raise ValidationError({
                api_settings.NON_FIELD_ERRORS_KEY: ['Cannot retrieve allowed requests.']
            })
        return allowed

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            allowed = AllowedRequest.objects.get(pk=1)
        except AllowedRequest.DoesNotExist:
            raise ValidationError({
                api_settings.NON_FIELD_ERRORS_KEY: ['Cannot retrieve allowed requests.']
            })
        command = serializer.data['value']
        system = platform.system()
        if system == 'Windows':
            call_windows(allowed, command)
        else:
            raise ValidationError({
                api_settings.NON_FIELD_ERRORS_KEY: ['Cannot recognize system.']
            })
        return Response({'command': command}, status=status.HTTP_200_OK)


class ExternalRequestViewSet(generics.CreateAPIView,
                             views.APIView):
    """
    ViewSet handling python code send in request.

    create: run python3 code in the system console.
    """
    queryset = ExternalRequest.objects.none()
    serializer_class = ExternalRequestSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        code = serializer.data['external']
        try:
            with Capturing() as output:
                exec(code)
        except:
            raise ValidationError({
                api_settings.NON_FIELD_ERRORS_KEY: ['Cannot process request.']
            })

        return Response({'result': output}, status=status.HTTP_200_OK)


class Capturing(list):
    """
    Helper class capturing terminal output.
    """
    def __enter__(self):
        self._stdout = sys.stdout
        sys.stdout = self._stringio = StringIO()
        return self

    def __exit__(self, *args):
        self.extend(self._stringio.getvalue().splitlines())
        sys.stdout = self._stdout
