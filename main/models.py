from django.db import models
from django.urls import reverse

# sử dụng để tự động điền slug khi tạo Category hoặc Thread mới
from django.template.defaultfilters import slugify


# Create your models here.
class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Category(TimeStampedModel):
    """Category chứa nhiều Thread"""

    name = models.CharField(max_length=50)
    description = models.TextField(blank=True, null=True)
    slug = models.SlugField(default="", null=False)

    class Meta:
        verbose_name_plural = "categories"
        db_table = "Category"

    def __str__(self):
        return self.name

    # Tạo mẫu url chung
    def get_absolute_url(self):
        return reverse("main:category_detail", kwargs={"slug": self.slug})

    # https://learndjango.com/tutorials/django-slug-tutorial
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        return super().save(*args, **kwargs)


class Thread(TimeStampedModel):
    """Thread mà người dùng đang thảo luận"""

    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name="threads"
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


class Post(TimeStampedModel):
    """Post đăng trong một Thread"""

    thread = models.ForeignKey(Thread, on_delete=models.CASCADE, related_name="posts")
    content = models.TextField()

    class Meta:
        verbose_name_plural = "posts"
        db_table = "Post"

    def __str__(self):
        return self.content

    # thông thường sẽ dùng để trả về page chi tiết của model đó
    def get_absolute_url(self):
        return reverse("main:thread_detail", kwargs={"slug": self.thread.slug})
