"""Defines URL patterns for main."""

from django.urls import path

from . import views

app_name = "main"
urlpatterns = [
    # Homepage
    path("", views.ForumListView.as_view(), name="forum_list"),
    # Page hiện các thread theo Forum
    path("f/<slug:slug>/", views.ForumDetailView.as_view(), name="forum_detail"),
    # Page hiện các comment của thread
    path("t/<slug:slug>/", views.ThreadDetailView.as_view(), name="thread_detail"),
    # Page thêm thread
    path(
        "f/<slug:slug>/new_thead/",
        views.ThreadCreateView.as_view(),
        name="thread_create",
    ),
    # Url này được gọi khi submit comment
    path(
        "t/<slug:slug>/new_comment/",
        views.CommentCreateView.as_view(),
        name="comment_create",
    ),
]
