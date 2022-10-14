from django.db import models


class Zone(models.Model):
    name = models.CharField(
        null=False,
        blank=False,
        max_length=32
    )

    neighbors = models.ManyToManyField(
        'Zone',
        blank=True
    )

    map = models.ForeignKey(
        'Map',
        on_delete=models.CASCADE,
        null=False
    )

    def __str__(self):
        return f"{self.name}: {self.map}"
