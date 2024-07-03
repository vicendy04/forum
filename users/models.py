from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
class User(AbstractUser):  # <-- you can change me
    display_name = models.TextField(blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)

    class Meta:
        db_table = "user"  # <-- you can change me
