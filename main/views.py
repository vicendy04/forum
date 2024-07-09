from django.shortcuts import get_object_or_404, render
from django.template.loader import render_to_string
from django.http import HttpResponse
from django.views.generic import CreateView
from django.views.decorators.http import require_POST

from .helpers import get_paged_object
from .models import Thread, Forum, ThreadPrefix
from .forms import ThreadForm, CommentForm


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
            comment = form.save()

            html_content = render_to_string(
                "main/includes/comment_list.html", {"comment": comment}
            )
            return HttpResponse(content=html_content)


class ThreadCreateView(CreateView):
    """Controller xử lý form thêm mới thread"""

    model = Thread
    form_class = ThreadForm

    def get_initial(self):
        initial = super().get_initial()

        # Sử dụng để điền trước thông tin vào form dựa vào url
        forum = get_object_or_404(Forum, slug=self.kwargs["slug"])
        # Thiết lập giá trị mặc định cho trường prefix
        no_prefix = ThreadPrefix.objects.get(name="No Prefix")

        initial["forum"] = forum
        initial["prefix"] = no_prefix
        return initial
