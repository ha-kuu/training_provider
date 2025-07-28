from rest_framework import serializers

class ResponseSerializerDSMS(serializers.Serializer):
    message = serializers.CharField()

class ValidateErrorSerializerDSMS(serializers.Serializer):
    pass