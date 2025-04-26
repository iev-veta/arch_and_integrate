from django import forms
from .models import Trip, TripSegment
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import UserProfile


class TripForm(forms.ModelForm):
    class Meta:
        model = Trip
        fields = ["name"]


class TripSegmentForm(forms.ModelForm):
    class Meta:
        model = TripSegment
        fields = [
            "departure_city",
            "arrival_city",
            "transport_type",
            "departure_time",
            "arrival_time",
        ]
        widgets = {
            "departure_time": forms.DateTimeInput(attrs={"type": "datetime-local"}),
            "arrival_time": forms.DateTimeInput(attrs={"type": "datetime-local"}),
        }


class CustomUserCreationForm(UserCreationForm):
    full_name = forms.CharField(max_length=100, required=True)
    passport_number = forms.CharField(max_length=20, required=True)

    class Meta:
        model = User
        fields = (
            "username",
            "password1",
            "password2",
            "full_name",
            "passport_number",
        )

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
            UserProfile.objects.create(
                user=user,
                full_name=self.cleaned_data["full_name"],
                passport_number=self.cleaned_data["passport_number"],
            )
        return user
