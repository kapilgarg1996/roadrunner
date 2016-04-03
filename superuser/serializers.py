from rest_framework import serializers

class SignSerializer(serializers.Serializer):
    status = serializers.IntegerField()
    detail = serializers.CharField()
    account = serializers.CharField()

class PassRequestSerializer(serializers.Serializer):
    status = serializers.IntegerField()
    detail = serializers.CharField()
    request = serializers.CharField()

