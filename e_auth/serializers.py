from rest_framework import serializers

class TokenSerializer(serializers.Serializer):
    status = serializers.IntegerField()
    token = serializers.CharField(max_length=200)

class AuthSerializer(serializers.Serializer):
    status = serializers.IntegerField()
    authorized = serializers.BooleanField()
