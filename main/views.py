from django.shortcuts import get_object_or_404
from django.views.generic import ListView, DetailView, CreateView
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


from .models import Thread, Forum, Comment
from .forms import ThreadForm, CommentForm


# Create your views here.
class ForumListView(ListView):
    """Hiện các Forum hiện có"""

    model = Forum
    template_name = "main/index.html"
    context_object_name = "forums"


class ForumDetailView(DetailView):
    """Hiện các thread của Forum đó"""

    model = Forum
    template_name = "main/forum_detail.html"
    context_object_name = "forum"

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the entries
        forum = self.object
        threads = forum.threads.order_by("-created_at").order_by("-is_pinned")
        context["threads"] = threads
        return context


class ThreadDetailView(DetailView):
    """Hiện các comment trong thread đó"""

    model = Thread
    template_name = "main/thread_detail.html"
    context_object_name = "thread"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        thread = self.object
        comments = thread.comments.order_by("created_at")

        # Phân trang các post
        paginator = Paginator(comments, 5)
        page_number = self.request.GET.get("page")

        try:
            comments_per_page = paginator.page(page_number)
        except PageNotAnInteger:
            comments_per_page = paginator.page(1)
        except EmptyPage:
            comments_per_page = paginator.page(paginator.num_pages)

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

    # Sử dụng get_success_url thay cho get_absolute_url trong model
    # def get_success_url(self):
    #     pass


class ThreadCreateView(CreateView):
    """Controller xử lý form thêm mới thread"""

    model = Thread
    form_class = ThreadForm
    template_name = "main/thread_form.html"
