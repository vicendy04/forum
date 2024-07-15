"""Defines URL patterns for main."""

from django.urls import path

from . import views

app_name = "main"

htmx_urlpatterns = [
    path(
        "t/<slug:slug>/add_comment/",
        views.add_comment,
        name="comment_create",
    ),
]

urlpatterns = [
    path("", views.forum_list, name="forum_list"),
    path("f/<slug:slug>/", views.forum_detail, name="forum_detail"),
    path("t/<slug:slug>/", views.thread_detail, name="thread_detail"),
    path(
        "f/<slug:slug>/new_thead/",
        views.add_thread,
        name="thread_create",
    ),
] + htmx_urlpatterns
