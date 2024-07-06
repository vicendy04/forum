"""Defines URL patterns for accounts."""

from django.urls import path

from . import views

app_name = "users"
urlpatterns = [
    path("register/", views.UserRegisterView.as_view(), name="register"),
    path("profile/", views.view_or_update_profile, name="profile"),
]
