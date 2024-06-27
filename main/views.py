from django.shortcuts import get_object_or_404
from django.views.generic import ListView, DetailView, CreateView
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


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
        category = self.object
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
        thread = self.object
        posts = thread.posts.order_by("created_at")

        # Phân trang các post
        paginator = Paginator(posts, 5)
        page_number = self.request.GET.get("page")

        try:
            posts_per_page = paginator.page(page_number)
        except PageNotAnInteger:
            posts_per_page = paginator.page(1)
        except EmptyPage:
            posts_per_page = paginator.page(paginator.num_pages)

        context["posts_per_page"] = posts_per_page
        context["paginator"] = paginator
        # Render form trong template với tên form là form
        context["form"] = PostForm()
        return context


# Chỗ này cần refactor
class PostCreateView(CreateView):
    """Controller lưu form"""

    model = Post
    form_class = PostForm

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

    # Sử dụng get_success_url thay cho get_absolute_url trong models
    # def get_success_url(self):
    #     pass
