from django.contrib import admin

# Register your models here.
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

admin.site.register(Country)
admin.site.register(City)
admin.site.register(Airport)
admin.site.register(Airline)
admin.site.register(FlightClass)
admin.site.register(AirplaneModel)
admin.site.register(Airplane)
admin.site.register(Seat)
admin.site.register(Passenger)
admin.site.register(Flight)
admin.site.register(FlightSchedule)
admin.site.register(Booking)
