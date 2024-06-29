from django.db import models
from django.urls import reverse

# sử dụng để tự động điền slug khi tạo Forum hoặc Thread mới
from django.template.defaultfilters import slugify


# Create your models here.
class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


# Tạo một model mới thay vì đổi tên model cũ
class Forum(TimeStampedModel):
    """Một Forum chứa nhiều Thread"""

    name = models.CharField(max_length=50)
    description = models.TextField(blank=True, null=True)
    slug = models.SlugField(default="", null=False)

    class Meta:
        verbose_name_plural = "forums"
        db_table = "Forum"

    def __str__(self):
        return self.name

    # Tạo mẫu url chung
    def get_absolute_url(self):
        return reverse("main:forum_detail", kwargs={"slug": self.slug})

    # https://learndjango.com/tutorials/django-slug-tutorial
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        return super().save(*args, **kwargs)


class Thread(TimeStampedModel):
    """Thread mà người dùng đang thảo luận"""

    forum = models.ForeignKey(
        Forum,
        on_delete=models.CASCADE,
        related_name="threads",
    )
    title = models.CharField(max_length=120)
    # Add slug functionality
    slug = models.SlugField(default="", null=False)

    class Meta:
        verbose_name_plural = "threads"
        db_table = "Thread"

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("main:thread_detail", kwargs={"slug": self.slug})

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        return super().save(*args, **kwargs)


# Tạo một model mới thay vì đổi tên model cũ
class Comment(TimeStampedModel):
    """Comment đăng trong một Thread"""

    thread = models.ForeignKey(
        Thread, on_delete=models.CASCADE, related_name="comments"
    )
    content = models.TextField()

    class Meta:
        verbose_name_plural = "comments"
        db_table = "Comment"

    def __str__(self):
        return self.content

    # thông thường sẽ dùng để trả về page chi tiết của model đó
    def get_absolute_url(self):
        return reverse("main:thread_detail", kwargs={"slug": self.thread.slug})
