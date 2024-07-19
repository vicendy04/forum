from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.template.context_processors import csrf
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.views.decorators.http import require_POST
from django_htmx.http import HttpResponseClientRedirect

from .forms import CommentForm, ThreadForm
from .helpers import get_paged_object
from .models import Comment, Forum, Thread


def forum_list(request):
    """Hiện các forum hiện có và thread mới nhất"""

    forums = Forum.objects.all()
    latest_threads = Thread.objects.order_by("-created_at")[:5]

    context = {
        "forums": forums,
        "latest_threads": latest_threads,
    }

    return render(request, "main/index.html", context)


def forum_detail(request, slug):
    """Hiện các thread của Forum đó"""

    forum = get_object_or_404(Forum.objects.prefetch_related("threads"), slug=slug)
    threads = forum.threads.order_by("-is_pinned", "-created_at")

    context = {"forum": forum}
    context.update(get_paged_object(request, queryset=threads, paginate_by=5))

    return render(request, "main/forum_detail.html", context)


def thread_detail(request, slug):
    """Hiện các comment trong thread đó"""

    thread = get_object_or_404(Thread.objects.prefetch_related("comments"), slug=slug)
    comments = thread.comments.order_by("created_at")

    context = {"forum": thread.forum, "thread": thread, "form": CommentForm()}
    context.update(get_paged_object(request, queryset=comments, paginate_by=5))

    return render(request, "main/thread_detail.html", context)


# @login_required and htmx can't be used together
def add_comment(request, slug):
    if not request.user.is_authenticated:
        login_url = reverse_lazy("users:login")
        thread_detail_url = reverse_lazy("main:thread_detail", kwargs={"slug": slug})
        query_string = "?next=" + thread_detail_url
        redirect_url = f"{login_url}{query_string}"
        return HttpResponseClientRedirect(redirect_url)

    # Sử dụng htmx để cập nhật phần bình luận không cần reload
    if request.method == "POST" and request.htmx:
        form = CommentForm(request.POST)

        if form.is_valid():
            thread = get_object_or_404(Thread.objects.all(), slug=slug)
            form.instance.thread = thread
            form.instance.user = request.user
            comment = form.save()

            html_content = render_to_string(
                "main/includes/comment_list.html", {"comment": comment}
            )
            return HttpResponse(content=html_content)


@login_required
def add_thread(request, slug):
    """Controller xử lý form thêm mới thread"""
    if request.method == "POST":
        form = ThreadForm(data=request.POST, forum_slug=slug)
        if form.is_valid():
            thread = form.save(commit=False)
            thread.user = request.user
            thread.save()
            return redirect("thread_detail", slug=thread.slug)

    else:
        form = ThreadForm(forum_slug=slug)

    return render(request, "main/thread_form.html", {"form": form})


def like_comment(request, pk):
    """Like button"""

    if request.method == "POST" and request.htmx:
        comment = get_object_or_404(
            Comment.objects.prefetch_related("users_like"), pk=pk
        )
        this_user_liked = comment.users_like.filter(id=request.user.id).exists()

        if this_user_liked:
            comment.users_like.remove(request.user)
        else:
            comment.users_like.add(request.user)

        context = {"comment": comment}
        context.update(csrf(request))
        html_content = render_to_string("main/includes/like_form.html", context)
        return HttpResponse(content=html_content)
