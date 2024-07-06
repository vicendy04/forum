from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings


# Create your models here.
class User(AbstractUser):  # <-- you can change me
    class Meta:
        db_table = "user"  # <-- you can change me


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    display_name = models.CharField(max_length=32)
    date_of_birth = models.DateField(blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    avatar = models.ImageField(
        default="default.jpg", upload_to="profile_pics/%Y/%m/%d/", blank=True
    )

    def __str__(self):
        return f"Profile của {self.user.username}"
