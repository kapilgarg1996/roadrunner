from rest_framework import serializers

class PaymentSerializer(serializers.Serializer):
    status = serializers.CharField()
    token = serializers.CharField(max_length=200)
