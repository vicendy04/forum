"""
Phục vụ cho mục đích trước mắt là tránh vi phạm don't repeat yourself
"""

from django.core.paginator import Paginator


def get_paged_list(request, objects_list, paginate_by):
    """Hàm giúp phân trang"""

    paginator = Paginator(objects_list, paginate_by)
    page_number = request.GET.get("page")

    # https://docs.djangoproject.com/en/5.0/ref/paginator/#django.core.paginator.Paginator.get_page
    paginated_objects = paginator.get_page(page_number)
    return paginated_objects, paginator
