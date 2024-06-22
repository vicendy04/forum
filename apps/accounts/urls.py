"""Defines URL patterns for accounts."""

from django.urls import path, include

from . import views

app_name = "apps.accounts"
urlpatterns = [
    # Include default auth urls.
    path("", include("django.contrib.auth.urls")),
    # Registration page.
    path("register/", views.UserRegisterView.as_view(), name="register"),
]
