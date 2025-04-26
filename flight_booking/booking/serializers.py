# booking/serializers.py

from rest_framework import serializers
from .models import (
    Country,
    City,
    Airport,
    Airline,
    FlightClass,
    AirplaneModel,
    Airplane,
    Seat,
    Passenger,
    Flight,
    FlightSchedule,
    Booking,
)


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = "__all__"


class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = "__all__"


class AirportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Airport
        fields = "__all__"


class AirlineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Airline
        fields = "__all__"


class FlightClassSerializer(serializers.ModelSerializer):
    class Meta:
        model = FlightClass
        fields = "__all__"


class AirplaneModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = AirplaneModel
        fields = "__all__"


class AirplaneSerializer(serializers.ModelSerializer):
    class Meta:
        model = Airplane
        fields = "__all__"


class SeatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Seat
        fields = "__all__"


class PassengerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Passenger
        fields = "__all__"


class FlightSerializer(serializers.ModelSerializer):
    class Meta:
        model = Flight
        fields = "__all__"


class FlightScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = FlightSchedule
        fields = "__all__"


class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = "__all__"
