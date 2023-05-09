from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    name = models.CharField(max_length=127)
    email = models.EmailField(unique=True)

    address = models.OneToOneField(
        "addresses.Address", on_delete=models.CASCADE, related_name="user"
    )
