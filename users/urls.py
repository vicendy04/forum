"""Defines URL patterns for accounts."""

from django.urls import include, path

from . import views

app_name = "users"

htmx_urlpatterns = [
    path("check_username", views.check_username, name="check_username"),
]

urlpatterns = [
    # Include default auth urls.
    path("", include("django.contrib.auth.urls")),
    path("register/", views.register, name="register"),
    path("profile/", views.view_or_update_profile, name="profile"),
    path("<str:username>/", views.user_profile, name="user_profile"),
] + htmx_urlpatterns
