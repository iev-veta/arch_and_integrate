from django.db import models
from django.contrib.auth.models import User


class Country(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class City(models.Model):
    name = models.CharField(max_length=100)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Trip(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class TripSegment(models.Model):
    TRANSPORT_TYPES = [
        ("auto", "Auto"),
        ("walk", "Walk"),
        ("flight", "Flight"),
    ]

    trip = models.ForeignKey(Trip, related_name="segments", on_delete=models.CASCADE)
    departure_city = models.ForeignKey(
        City, related_name="departure_segments", on_delete=models.CASCADE
    )
    arrival_city = models.ForeignKey(
        City, related_name="arrival_segments", on_delete=models.CASCADE
    )
    transport_type = models.CharField(max_length=50, choices=TRANSPORT_TYPES)
    departure_time = models.DateTimeField(null=True, blank=True)
    arrival_time = models.DateTimeField(null=True, blank=True)
    order = models.IntegerField()

    class Meta:
        ordering = ["order"]

    def __str__(self):
        departure_str = (
            self.departure_time.strftime("%Y-%m-%d %H:%M")
            if self.departure_time
            else "N/A"
        )
        arrival_str = (
            self.arrival_time.strftime("%Y-%m-%d %H:%M") if self.arrival_time else "N/A"
        )
        return f"{self.departure_city} -> {self.arrival_city} ({self.transport_type}) on {departure_str} - {arrival_str}"


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100)
    passport_number = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.full_name
