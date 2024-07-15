from django.db import models
from django.template.defaultfilters import (
    slugify,
)
from django.urls import reverse

from forum_project import (
    settings,
)


# Create your models here.
class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class SlugifiedModel(models.Model):
    slug = models.SlugField(unique=True)

    class Meta:
        abstract = True

    # https://learndjango.com/tutorials/django-slug-tutorial
    def save(self, *args, **kwargs):
        self.slug = slugify(self.get_slug())
        return super().save(*args, **kwargs)

    def get_slug(self):
        raise NotImplementedError("Chua ghi de get_slug()")


class Forum(TimeStampedModel, SlugifiedModel):
    """Một Forum chứa nhiều Thread"""

    name = models.CharField(max_length=50)
    description = models.TextField(blank=True, null=True)

    class Meta:
        db_table = "forum"

    def __str__(self):
        return self.name

    def get_slug(self):
        return self.name

    # Tạo mẫu url chung
    def get_absolute_url(self):
        return reverse("main:forum_detail", kwargs={"slug": self.slug})


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
    forum = models.ForeignKey(Forum, on_delete=models.CASCADE, related_name="threads")
    prefix = models.ForeignKey(
        ThreadPrefix, on_delete=models.SET_NULL, null=True, related_name="threads"
    )
    title = models.CharField(max_length=120)
    is_pinned = models.BooleanField(default=False)

    class Meta:
        db_table = "thread"

    def __str__(self):
        return self.title

    def get_slug(self):
        return self.title

    def get_absolute_url(self):
        return reverse("main:thread_detail", kwargs={"slug": self.slug})


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
    # comment.users_like.all(), or get them from a user object, such as user.comments_liked.all()
    users_like = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        through="Like",
        related_name="comments_liked",
    )

    class Meta:
        db_table = "comment"

    def __str__(self):
        return self.content

    # thông thường sẽ dùng để trả về page chi tiết của model đó
    def get_absolute_url(self):
        return reverse("main:thread_detail", kwargs={"slug": self.thread.slug})

    @property
    def total_likes(self):
        return self.users_like.count()


class Like(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "like"
        unique_together = ("user", "comment")

    def __str__(self):
        return f"{self.user} likes {self.comment}"
