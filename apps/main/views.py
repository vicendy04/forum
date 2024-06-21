from django.views.generic import ListView, DetailView
from .models import Category, Thread, Post


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
        return context
