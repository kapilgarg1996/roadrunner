from rest_framework import serializers

class SignSerializer(serializers.Serializer):
    status = serializers.IntegerField()
    detail = serializers.CharField()
    account = serializers.CharField(max_length=200)

class PassRequestSerializer(serializers.Serializer):
    status = serializers.IntegerField()
    detail = serializers.CharField()
    request = serializers.CharField(max_length=200)

