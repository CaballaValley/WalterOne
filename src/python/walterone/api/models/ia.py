from django.contrib.auth.models import User
from django.db import models


class IA(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE
    )

    name = models.CharField(
        null=False,
        blank=False,
        max_length=32
    )

    def __str__(self):
        return f"{self.name}"
