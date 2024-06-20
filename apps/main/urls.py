"""Defines URL patterns for main."""

from django.urls import path
from . import views

app_name = "apps.main"
urlpatterns = [
    # Homepage
    path("", views.CategoryListView.as_view(), name="category-list"),
    # Page hiện các thread theo category
    path("c/<int:pk>/", views.CategoryDetailView.as_view(), name="thread-list"),
]
