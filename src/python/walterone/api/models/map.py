from django.db import models


class Map(models.Model):
    name = models.CharField(
        null=False,
        blank=False,
        max_length=32
    )

    def __str__(self):
        return f"{self.name}"
