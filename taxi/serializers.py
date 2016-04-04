from rest_framework import serializers
from taxi.models import *
class TaxiSerializer(serializers.ModelSerializer):
    class Meta:
        model = Taxi


class PlaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Place


class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking

