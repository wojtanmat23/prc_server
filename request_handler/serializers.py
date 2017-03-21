from rest_framework import serializers

from request_handler.models import (
    AllowedRequest,
    ExternalRequest,
    Signal,
)


class WindowsRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = AllowedRequest
        fields = '__all__'


class ExternalRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExternalRequest
        fields = '__all__'


class SignalSerializer(serializers.ModelSerializer):

    class Meta:
        model = Signal
        fields = '__all__'
