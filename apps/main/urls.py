"""Defines URL patterns for main."""

from django.urls import path
from . import views

app_name = "apps.main"
urlpatterns = [
    # Homepage
    path("", views.CategoryListView.as_view(), name="category_list"),
    # Page hiện các thread theo category
    path("c/<int:pk>/", views.CategoryDetailView.as_view(), name="category_detail"),
    path("t/<int:pk>/", views.ThreadDetailView.as_view(), name="thread_detail"),
]
