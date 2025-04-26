from django.urls import path
from .views import (
    trip_list,
    trip_create,
    trip_detail,
    segment_create,
    register,
    search_flights,
)
from django.contrib.auth import views as auth_views

urlpatterns = [
    path("", trip_list, name="trip_list"),
    path("trips/create/", trip_create, name="trip_create"),
    path("trips/<int:trip_id>/", trip_detail, name="trip_detail"),
    path("trips/<int:trip_id>/segments/create/", segment_create, name="segment_create"),
    path(
        "login/",
        auth_views.LoginView.as_view(template_name="registration/login.html"),
        name="login",
    ),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("register/", register, name="register"),
    path("search-flights/<int:segment_id>/", search_flights, name="search_flights"),
]
