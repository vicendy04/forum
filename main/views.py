from django.shortcuts import get_object_or_404, render
from django.template.loader import render_to_string
from django.http import HttpResponse
from django.views.generic import ListView, DetailView, CreateView

from .helpers import get_paged_list
from .models import Thread, Forum, Comment, ThreadPrefix
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


class ForumDetailView(DetailView):
    """Hiện các thread của Forum đó"""

    model = Forum
    context_object_name = "forum"

    def get_queryset(self):
        return super().get_queryset().prefetch_related("threads")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        forum = self.object
        threads = forum.threads.order_by("-is_pinned", "-created_at")
        threads_per_page, paginator = get_paged_list(
            self.request, threads, paginate_by=10
        )

        context["threads_per_page"] = threads_per_page
        context["paginator"] = paginator
        return context


class ThreadDetailView(DetailView):
    """Hiện các comment trong thread đó"""

    model = Thread
    context_object_name = "thread"

    def get_queryset(self):
        return (
            super().get_queryset().select_related("forum").prefetch_related("comments")
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        thread = self.object
        comments = thread.comments.order_by("created_at")
        comments_per_page, paginator = get_paged_list(
            self.request, comments, paginate_by=5
        )

        context["forum"] = thread.forum
        context["comments_per_page"] = comments_per_page
        context["paginator"] = paginator
        context["form"] = CommentForm()
        return context


class CommentCreateView(CreateView):
    """Controller lưu form"""

    model = Comment
    form_class = CommentForm

    # Làm thêm vài thứ để xác thực trước khi lưu
    def form_valid(self, form):
        # Lấy thread_id từ url kwargs
        thread = get_object_or_404(Thread, slug=self.kwargs["slug"])
        form.instance.thread_id = thread.id
        comment = form.save()

        # Sử dụng htmx để cập nhật phần bình luận không cần reload
        if self.request.htmx:
            html_content = render_to_string(
                "main/includes/comment_list.html", {"comment": comment}
            )
            return HttpResponse(html_content)


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
