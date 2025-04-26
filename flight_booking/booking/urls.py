from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from .views import (
    CountryViewSet,
    CityViewSet,
    AirportViewSet,
    AirlineViewSet,
    FlightClassViewSet,
    AirplaneModelViewSet,
    AirplaneViewSet,
    SeatViewSet,
    PassengerViewSet,
    FlightViewSet,
    FlightScheduleViewSet,
    BookingViewSet,
    FilteredFlightsView,
)

router = DefaultRouter()
router.register(r"countries", CountryViewSet)
router.register(r"cities", CityViewSet)
router.register(r"airports", AirportViewSet)
router.register(r"airlines", AirlineViewSet)
router.register(r"flight-classes", FlightClassViewSet)
router.register(r"airplane-models", AirplaneModelViewSet)
router.register(r"airplanes", AirplaneViewSet)
router.register(r"seats", SeatViewSet)
router.register(r"passengers", PassengerViewSet)
router.register(r"flights", FlightViewSet)
router.register(r"flight-schedules", FlightScheduleViewSet)
router.register(r"bookings", BookingViewSet)


urlpatterns = [
    path("", views.index, name="index"),
    path("", include(router.urls)),
    path("filtered-flights/", FilteredFlightsView.as_view(), name="filtered-flights"),
]
