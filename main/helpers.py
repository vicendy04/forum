"""
Phục vụ cho mục đích trước mắt là tránh vi phạm don't repeat yourself
"""

from django.core.paginator import Paginator


def get_paged_object(request, queryset, paginate_by):
    """Hàm giúp phân trang"""

    paginator = Paginator(queryset, paginate_by)
    page_number = request.GET.get("page")
    # https://docs.djangoproject.com/en/5.0/ref/paginator/#django.core.paginator.Paginator.get_page
    page_obj = paginator.get_page(page_number)

    return {
        "page_obj": page_obj,
    }
