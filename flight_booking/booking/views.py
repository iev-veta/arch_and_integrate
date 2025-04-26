from django.shortcuts import render
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
from .serializers import (
    CountrySerializer,
    CitySerializer,
    AirportSerializer,
    AirlineSerializer,
    FlightClassSerializer,
    AirplaneModelSerializer,
    AirplaneSerializer,
    SeatSerializer,
    PassengerSerializer,
    FlightSerializer,
    FlightScheduleSerializer,
    BookingSerializer,
)
from rest_framework import viewsets, generics
from rest_framework.response import Response
from django.utils.dateparse import parse_date


def index(request):
    countries = Country.objects.all()
    cities = City.objects.all()
    airports = Airport.objects.all()
    airlines = Airline.objects.all()
    flight_classes = FlightClass.objects.all()
    airplane_models = AirplaneModel.objects.all()
    airplanes = Airplane.objects.all()
    seats = Seat.objects.all()
    passengers = Passenger.objects.all()
    flights = Flight.objects.all()
    flight_schedules = FlightSchedule.objects.all()
    bookings = Booking.objects.all()

    context = {
        "countries": countries,
        "cities": cities,
        "airports": airports,
        "airlines": airlines,
        "flight_classes": flight_classes,
        "airplane_models": airplane_models,
        "airplanes": airplanes,
        "seats": seats,
        "passengers": passengers,
        "flights": flights,
        "flight_schedules": flight_schedules,
        "bookings": bookings,
    }

    return render(request, "booking/index.html", context)


class CountryViewSet(viewsets.ModelViewSet):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer


class CityViewSet(viewsets.ModelViewSet):
    queryset = City.objects.all()
    serializer_class = CitySerializer


class AirportViewSet(viewsets.ModelViewSet):
    queryset = Airport.objects.all()
    serializer_class = AirportSerializer


class AirlineViewSet(viewsets.ModelViewSet):
    queryset = Airline.objects.all()
    serializer_class = AirlineSerializer


class FlightClassViewSet(viewsets.ModelViewSet):
    queryset = FlightClass.objects.all()
    serializer_class = FlightClassSerializer


class AirplaneModelViewSet(viewsets.ModelViewSet):
    queryset = AirplaneModel.objects.all()
    serializer_class = AirplaneModelSerializer


class AirplaneViewSet(viewsets.ModelViewSet):
    queryset = Airplane.objects.all()
    serializer_class = AirplaneSerializer


class SeatViewSet(viewsets.ModelViewSet):
    queryset = Seat.objects.all()
    serializer_class = SeatSerializer


class PassengerViewSet(viewsets.ModelViewSet):
    queryset = Passenger.objects.all()
    serializer_class = PassengerSerializer


class FlightViewSet(viewsets.ModelViewSet):
    queryset = Flight.objects.all()
    serializer_class = FlightSerializer


class FlightScheduleViewSet(viewsets.ModelViewSet):
    queryset = FlightSchedule.objects.all()
    serializer_class = FlightScheduleSerializer


class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer


class FilteredFlightsView(generics.ListAPIView):
    serializer_class = FlightScheduleSerializer

    def get_queryset(self):
        queryset = FlightSchedule.objects.all()

        departure_city = self.request.query_params.get("departure_city")
        arrival_city = self.request.query_params.get("arrival_city")
        departure_date = self.request.query_params.get("departure_date")
        arrival_date = self.request.query_params.get("arrival_date")

        if departure_city:
            queryset = queryset.filter(
                flight__departure_airport__city__name__icontains=departure_city
            )
        if arrival_city:
            queryset = queryset.filter(
                flight__arrival_airport__city__name__icontains=arrival_city
            )
        if departure_date:
            departure_date = parse_date(departure_date)
            queryset = queryset.filter(departure_time__date__gte=departure_date)
        if arrival_date:
            arrival_date = parse_date(arrival_date)
            queryset = queryset.filter(arrival_time__date__lte=arrival_date)

        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)

        # Добавляем информацию о наличии свободных мест и другую необходимую информацию
        response_data = []
        for flight_schedule in serializer.data:
            flight_id = flight_schedule["id"]
            flight = Flight.objects.get(id=flight_schedule["flight"])
            airplane = Airplane.objects.get(id=flight_schedule["airplane"])
            departure_airport = Airport.objects.get(id=flight.departure_airport_id)
            arrival_airport = Airport.objects.get(id=flight.arrival_airport_id)
            airline = Airline.objects.get(id=flight.airline_id)

            available_seats = Seat.objects.filter(airplane_id=airplane.id).exclude(
                booking__flight_schedule_id=flight_id
            )

            flight_info = {
                "departure_time": flight_schedule["departure_time"],
                "arrival_time": flight_schedule["arrival_time"],
                "departure_city": departure_airport.city.name,
                "departure_country": departure_airport.city.country.name,
                "departure_airport": departure_airport.name,
                "departure_airport_code": departure_airport.iata_code,
                "arrival_city": arrival_airport.city.name,
                "arrival_country": arrival_airport.city.country.name,
                "arrival_airport": arrival_airport.name,
                "arrival_airport_code": arrival_airport.iata_code,
                "airplane": airplane.model.name,
                "airline": airline.name,
                "available_seats": [
                    {
                        "seat_code": seat.seat_code,
                        "flight_class": seat.flight_class.name,
                    }
                    for seat in available_seats
                ],
            }
            response_data.append(flight_info)

        return Response(response_data)
