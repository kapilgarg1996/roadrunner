from rest_framework import serializers
from bus.models import *
class StopSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stop

class RouteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Route

class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket

class RouteDetailSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    start_time = serializers.DateTimeField()
    journey_time = serializers.DateTimeField()
    fair = serializers.IntegerField()
    seats_avail = serializers.IntegerField()
    seats_config = serializers.CharField()
    bus_number = serializers.CharField()
    image = serializers.CharField()
    ac = serializers.BooleanField()
    seater = serializers.BooleanField()
    s_name = serializers.CharField()
    s_city = serializers.CharField()
    d_name = serializers.CharField()
    d_city = serializers.CharField()
    driver = serializers.CharField()
    conductor = serializers.CharField()

