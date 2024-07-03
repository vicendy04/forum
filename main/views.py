from django.shortcuts import get_object_or_404
from django.views.generic import ListView, DetailView, CreateView

from .helpers import paginate_queryset
from .models import Thread, Forum, Comment, ThreadPrefix
from .forms import ThreadForm, CommentForm


# Create your views here.
class ForumListView(ListView):
    """Hiện các Forum hiện có"""

    model = Forum
    template_name = "main/index.html"
    context_object_name = "forums"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        latest_threads = Thread.objects.order_by("-created_at")[:5]

        context["latest_threads"] = latest_threads
        return context


class ForumDetailView(DetailView):
    """Hiện các thread của Forum đó"""

    model = Forum
    template_name = "main/forum_detail.html"
    context_object_name = "forum"

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)

        forum = self.object
        threads = forum.threads.order_by("-is_pinned", "-created_at")

        # Phân trang các thread
        threads_per_page, paginator = paginate_queryset(self.request, threads, 10)

        context["threads_per_page"] = threads_per_page
        context["paginator"] = paginator
        return context


class ThreadDetailView(DetailView):
    """Hiện các comment trong thread đó"""

    model = Thread
    template_name = "main/thread_detail.html"
    context_object_name = "thread"

    def get_queryset(self):
        # lấy trước để dùng cho breadcrumb
        queryset = super().get_queryset().select_related("forum")
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        thread = self.object
        comments = thread.comments.order_by("created_at")

        # Phân trang các comment
        comments_per_page, paginator = paginate_queryset(self.request, comments, 5)

        context["comments_per_page"] = comments_per_page
        context["paginator"] = paginator
        # Render form trong template với tên form là form
        context["form"] = CommentForm()
        return context


# Chỗ này cần refactor
class CommentCreateView(CreateView):
    """Controller lưu form"""

    model = Comment
    form_class = CommentForm

    # Làm thêm vài thứ để xác thực trước khi lưu
    def form_valid(self, form):
        # Lấy thread_id từ url kwargs
        slug = self.kwargs["slug"]
        thread = get_object_or_404(Thread, slug=slug)
        form.instance.thread_id = thread.id
        return super().form_valid(form)


class ThreadCreateView(CreateView):
    """Controller xử lý form thêm mới thread"""

    model = Thread
    form_class = ThreadForm
    template_name = "main/thread_form.html"

    def get_initial(self):
        """Return the initial data to use for forms on this view."""
        initial = super().get_initial()

        # Thiết lập giá trị mặc định cho trường prefix
        no_prefix = ThreadPrefix.objects.get(name="No Prefix")
        initial["prefix"] = no_prefix

        # Sử dụng để điền trước thông tin vào form dựa vào url
        form_slug = self.kwargs.get("slug")
        forum = get_object_or_404(Forum, slug=form_slug)
        initial["forum"] = forum

        return initial
