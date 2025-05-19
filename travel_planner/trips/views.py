from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Trip, TripSegment, UserProfile
from .forms import TripForm, TripSegmentForm, CustomUserCreationForm
from django.contrib.auth import login
import requests
from urllib.parse import unquote


@login_required
def trip_list(request):
    trips = Trip.objects.filter(user=request.user)
    return render(request, "trips/trip_list.html", {"trips": trips})


@login_required
def trip_create(request):
    if request.method == "POST":
        form = TripForm(request.POST)
        if form.is_valid():
            trip = form.save(commit=False)
            trip.user = request.user
            trip.save()
            return redirect("trip_detail", trip_id=trip.id)
    else:
        form = TripForm()
    return render(request, "trips/trip_form.html", {"form": form})


@login_required
def trip_detail(request, trip_id):
    trip = Trip.objects.get(id=trip_id, user=request.user)
    segments = trip.segments.all()
    return render(
        request, "trips/trip_detail.html", {"trip": trip, "segments": segments}
    )


@login_required
def segment_create(request, trip_id):
    trip = Trip.objects.get(id=trip_id, user=request.user)
    if request.method == "POST":
        form = TripSegmentForm(request.POST)
        if form.is_valid():
            segment = form.save(commit=False)
            segment.trip = trip
            segment.order = trip.segments.count() + 1
            segment.save()
            return redirect("trip_detail", trip_id=trip.id)
    else:
        form = TripSegmentForm()
    return render(request, "trips/segment_form.html", {"form": form, "trip": trip})


def register(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("trip_list")
    else:
        form = CustomUserCreationForm()
    return render(request, "registration/register.html", {"form": form})


@login_required
def search_flights(request, segment_id):
    segment = TripSegment.objects.get(id=segment_id)
    departure_city = unquote(segment.departure_city.name)
    arrival_city = unquote(segment.arrival_city.name)
    departure_date = (
        segment.departure_time.strftime("%Y-%m-%d") if segment.departure_time else None
    )

    # Используем имя сервиса вместо 127.0.0.1
    # Основной запрос = интеграция
    response = requests.get(
        "http://flight_booking-web-1:8000/api/filtered-flights/",
        params={
            "departure_city": departure_city,
            "arrival_city": arrival_city,
            "departure_date": departure_date,
        },
        headers={"Host": "localhost"}, 
    )

    try:
        flights = response.json()
    except ValueError as e:
        # Логируем ошибку и возвращаем пустой список рейсов
        print(f"Error decoding JSON: {e}")
        print(f"Response content: {response.content}")
        flights = []

    return render(
        request,
        "trips/flight_search_results.html",
        {"segment": segment, "flights": flights},
    )
