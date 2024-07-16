from django.urls import reverse_lazy
from forum_project import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill


# Create your models here.
class User(AbstractUser):  # <-- you can change me
    # symmetrical=False to define a non-symmetrical relationship
    # (if I follow you, it doesn’t mean that you automatically follow me)
    following = models.ManyToManyField(
        "self", through="Follow", related_name="followers", symmetrical=False
    )

    class Meta:
        db_table = "user"  # <-- you can change me

    # url for user profile
    def get_absolute_url(self):
        return reverse_lazy("users:user_profile", kwargs={"username": self.username})

    @property
    def total_comments(self):
        return self.comments_created.count()

    @property
    def reaction_score(self):
        # comments_liked is related_name attr, specificed in Comment model
        return self.comments_liked.count()


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    display_name = models.CharField(max_length=32)
    date_of_birth = models.DateField(blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    avatar = models.ImageField(
        default="default.jpg", upload_to="profile_pics/%Y/%m/%d/", blank=True
    )
    avatar_thumbnail = ImageSpecField(
        source="avatar",
        processors=[ResizeToFill(460, 460)],
        format="JPEG",
        options={"quality": 60},
    )

    def __str__(self):
        return f"Profile của {self.user.username}"


class Follow(models.Model):
    user_from = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="following_set"
    )
    user_to = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="follower_set"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user_from", "user_to")
        indexes = [
            models.Index(fields=["-created_at"]),
        ]

    def __str__(self):
        return f"{self.user_from} follows {self.user_to}"
