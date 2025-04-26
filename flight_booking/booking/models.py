from django.db import models


class Country(models.Model):
    name = models.CharField(max_length=50, unique=True)

    class Meta:
        db_table = "countries"


class City(models.Model):
    name = models.CharField(max_length=50, unique=True)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)

    class Meta:
        db_table = "cities"


class Airport(models.Model):
    name = models.CharField(max_length=100)
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    iata_code = models.CharField(max_length=3, unique=True)

    class Meta:
        db_table = "airports"


class Airline(models.Model):
    name = models.CharField(max_length=50)
    iata_code = models.CharField(max_length=2, unique=True)

    class Meta:
        db_table = "airlines"


class FlightClass(models.Model):
    name = models.CharField(max_length=20, unique=True)

    class Meta:
        db_table = "flight_classes"


class AirplaneModel(models.Model):
    name = models.CharField(max_length=50)
    seat_capacity = models.IntegerField()

    class Meta:
        db_table = "airplane_models"


class Airplane(models.Model):
    model = models.ForeignKey(AirplaneModel, on_delete=models.CASCADE)

    class Meta:
        db_table = "airplanes"


class Seat(models.Model):
    airplane = models.ForeignKey(Airplane, on_delete=models.CASCADE)
    flight_class = models.ForeignKey(FlightClass, on_delete=models.CASCADE)
    row_number = models.SmallIntegerField()
    seat_code = models.CharField(max_length=3)

    class Meta:
        db_table = "seats"
        unique_together = ("airplane", "seat_code")


class Passenger(models.Model):
    full_name = models.CharField(max_length=100)
    passport_number = models.CharField(max_length=20, unique=True)

    class Meta:
        db_table = "passengers"


class Flight(models.Model):
    flight_number = models.CharField(max_length=6)
    airline = models.ForeignKey(Airline, on_delete=models.CASCADE)
    departure_airport = models.ForeignKey(
        Airport, related_name="departure_flights", on_delete=models.CASCADE
    )
    arrival_airport = models.ForeignKey(
        Airport, related_name="arrival_flights", on_delete=models.CASCADE
    )

    class Meta:
        db_table = "flights"


class FlightSchedule(models.Model):
    flight = models.ForeignKey(Flight, on_delete=models.CASCADE)
    departure_time = models.DateTimeField()
    arrival_time = models.DateTimeField()
    airplane = models.ForeignKey(Airplane, on_delete=models.CASCADE)

    class Meta:
        db_table = "flight_schedules"


class Booking(models.Model):
    STATUS_CHOICES = [
        ("reserved", "Reserved"),
        ("paid", "Paid"),
        ("cancelled", "Cancelled"),
    ]

    flight_schedule = models.ForeignKey(FlightSchedule, on_delete=models.CASCADE)
    seat = models.ForeignKey(Seat, on_delete=models.CASCADE)
    passenger = models.ForeignKey(Passenger, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="reserved")

    class Meta:
        db_table = "bookings"
        unique_together = ("flight_schedule", "seat")
