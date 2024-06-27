"""Defines URL patterns for main."""

from django.urls import path
from . import views

app_name = "main"
urlpatterns = [
    # Homepage
    path("", views.CategoryListView.as_view(), name="category_list"),
    # Page hiện các thread theo category
    path("c/<slug:slug>/", views.CategoryDetailView.as_view(), name="category_detail"),
    # Page hiện các post (comment) của thread
    path("t/<slug:slug>/", views.ThreadDetailView.as_view(), name="thread_detail"),
    # Page thêm thread
    path(
        "c/<int:category_id>/new_thead/",
        views.ThreadCreateView.as_view(),
        name="thread_create",
    ),
    # Url này được gọi khi submit comment
    path(
        "t/<slug:slug>/new_post/",
        views.PostCreateView.as_view(),
        name="post_create",
    ),
]
