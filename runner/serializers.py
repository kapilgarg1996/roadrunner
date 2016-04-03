from rest_framework import serializers

class UserDetailSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    email = serializers.CharField()
    tid = serializers.IntegerField()
    source = serializers.IntegerField()
    destination = serializers.IntegerField()
