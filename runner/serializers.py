from rest_framework import serializers
from runner.models import *

class UserDetailSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    email = serializers.CharField()
    tid = serializers.IntegerField()
    source = serializers.IntegerField()
    destination = serializers.IntegerField()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
