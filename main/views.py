from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.template.context_processors import csrf
from django.template.loader import render_to_string
from django.views.decorators.http import require_POST

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

    forum = get_object_or_404(Forum.objects.all(), slug=slug)
    threads = forum.threads.order_by("-is_pinned", "-created_at")

    context = {"forum": forum}
    context.update(get_paged_object(request, queryset=threads, paginate_by=5))

    return render(request, "main/forum_detail.html", context)


def thread_detail(request, slug):
    """Hiện các comment trong thread đó"""

    thread = get_object_or_404(Thread.objects.all(), slug=slug)
    comments = thread.comments.order_by("created_at")

    context = {"forum": thread.forum, "thread": thread, "form": CommentForm()}
    context.update(get_paged_object(request, queryset=comments, paginate_by=5))

    return render(request, "main/thread_detail.html", context)


@require_POST
def add_comment(request, slug):
    # Sử dụng htmx để cập nhật phần bình luận không cần reload
    if request.htmx:
        form = CommentForm(request.POST)

        if form.is_valid():
            thread = get_object_or_404(Thread, slug=slug)
            form.instance.thread = thread
            form.instance.user = request.user
            comment = form.save()

            html_content = render_to_string(
                "main/includes/comment_list.html", {"comment": comment}
            )
            return HttpResponse(content=html_content)


def add_thread(request, slug):
    """Controller xử lý form thêm mới thread"""
    if request.method == "POST":
        form = ThreadForm(request.POST)
        if form.is_valid():
            form.save(user=request.user)

            redirect(Thread, slug=slug)
    else:
        form = ThreadForm(forum_slug=slug)

    return render(request, "main/thread_form.html", {"form": form})


def like_comment(request, pk):
    """Like button"""

    if request.method == "POST" and request.htmx:
        comment = get_object_or_404(Comment, pk=pk)
        this_user_liked = comment.users_like.filter(
            username=request.user.username
        ).exists()

        if this_user_liked:
            comment.users_like.remove(request.user)
        else:
            comment.users_like.add(request.user)
        context = {"comment": comment}
        context.update(csrf(request))
        html_content = render_to_string("main/includes/like_form.html", context)
        return HttpResponse(content=html_content)
