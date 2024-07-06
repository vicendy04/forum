"""Defines URL patterns for main."""

from django.urls import path

from . import views


app_name = "main"

htmx_patterns = [
    path(
        "t/<slug:slug>/add_comment/",
        views.CommentCreateView.as_view(),
        name="comment_create",
    ),
]

urlpatterns = [
    path("", views.forum_list, name="forum_list"),
    path("f/<slug:slug>/", views.ForumDetailView.as_view(), name="forum_detail"),
    path("t/<slug:slug>/", views.ThreadDetailView.as_view(), name="thread_detail"),
    path(
        "f/<slug:slug>/new_thead/",
        views.ThreadCreateView.as_view(),
        name="thread_create",
    ),
] + htmx_patterns
