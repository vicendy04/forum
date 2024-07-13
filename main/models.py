from django.db import models
from django.urls import reverse
from django.template.defaultfilters import (
    slugify,
)

from forum_project import (
    settings,
)  # sử dụng để tự động điền slug khi tạo Forum hoặc Thread mới


# Create your models here.
class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class SlugifiedModel(models.Model):
    slug = models.SlugField(null=False, unique=True)

    class Meta:
        abstract = True

    # https://learndjango.com/tutorials/django-slug-tutorial
    def save(self, *args, **kwargs):
        self.slug = slugify(self.get_slug())
        return super().save(*args, **kwargs)

    def get_slug(self):
        raise NotImplementedError("Chua ghi de get_slug()")


# Tạo một model mới thay vì đổi tên model cũ
class Forum(TimeStampedModel, SlugifiedModel):
    """Một Forum chứa nhiều Thread"""

    name = models.CharField(max_length=50)
    description = models.TextField(blank=True, null=True)

    class Meta:
        db_table = "forum"

    def __str__(self):
        return self.name

    # Tạo mẫu url chung
    def get_absolute_url(self):
        return reverse("main:forum_detail", kwargs={"slug": self.slug})

    def get_slug(self):
        return self.name


class ThreadPrefix(SlugifiedModel):
    name = models.CharField(max_length=50, unique=True)
    color = models.CharField(max_length=7, default="#2386CC")

    class Meta:
        verbose_name_plural = "thread prefixes"
        db_table = "thread_prefix"

    def __str__(self):
        return self.name

    def get_slug(self):
        return self.name


class Thread(TimeStampedModel, SlugifiedModel):
    """Thread mà người dùng đang thảo luận"""

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="threads_created",
    )
    forum = models.ForeignKey(
        Forum,
        on_delete=models.CASCADE,
        related_name="threads",
    )
    prefix = models.ForeignKey(
        ThreadPrefix, on_delete=models.SET_NULL, null=True, related_name="threads"
    )
    title = models.CharField(max_length=120)
    is_pinned = models.BooleanField(default=False)

    class Meta:
        db_table = "thread"

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("main:thread_detail", kwargs={"slug": self.slug})

    def get_slug(self):
        return self.title


# Tạo một model mới thay vì đổi tên model cũ
class Comment(TimeStampedModel):
    """Comment đăng trong một Thread"""

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="comments_created",
    )
    thread = models.ForeignKey(
        Thread, on_delete=models.CASCADE, related_name="comments"
    )
    content = models.TextField()

    class Meta:
        db_table = "comment"

    def __str__(self):
        return self.content

    # thông thường sẽ dùng để trả về page chi tiết của model đó
    def get_absolute_url(self):
        return reverse("main:thread_detail", kwargs={"slug": self.thread.slug})
