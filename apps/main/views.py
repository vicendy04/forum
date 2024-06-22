from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView
from .models import Category, Thread, Post
from .forms import ThreadForm, PostForm


# Create your views here.
class CategoryListView(ListView):
    """Hiện mục category"""

    model = Category
    template_name = "main/index.html"
    context_object_name = "categories"


class CategoryDetailView(DetailView):
    """Hiện các thread của category đó"""

    model = Category
    template_name = "main/category_detail.html"
    context_object_name = "category"

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the entries
        category = self.get_object()
        threads = category.threads.order_by("-created_at")
        context["threads"] = threads
        return context


class ThreadDetailView(DetailView):
    """Hiện các post (comment) trong thread đó"""

    model = Thread
    template_name = "main/thread_detail.html"
    context_object_name = "thread"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        thread = self.get_object()
        posts = thread.posts.order_by("-created_at")
        context["posts"] = posts
        # Render form trong template với tên form là form
        context["form"] = PostForm()
        return context


class ThreadCreateView(CreateView):
    """Form thêm mới thread"""

    model = Thread
    form_class = ThreadForm
    template_name = "main/thread_form.html"


# A view that displays a form for creating an object, redisplaying
# the form with validation errors (if there are any) and saving the object.
class PostCreateView(CreateView):
    """Form thêm mới post"""

    model = Post
    form_class = PostForm
    template_name = "main/thread_detail.html"

    # Làm thêm vài thứ để xác thực trước khi lưu
    # Ở đây là xác định thread_id
    def form_valid(self, form):
        # Lấy thread_id từ url kwargs
        thread_id = self.kwargs.get("thread_id")
        form.instance.thread_id = thread_id
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy(
            "apps.main:thread_detail",
            kwargs={"pk": self.kwargs.get("thread_id")},
        )
