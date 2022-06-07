from django.db import models

# Create your models here.

class Zone(models.Model):
    name = models.CharField(
        null=False,
        blank=False,
        max_length=32
    )

    neighbors = models.ManyToManyField(
        'Zone',
    )

    map = models.ForeignKey(
        'Map',
        on_delete=models.CASCADE,
        null=False
    )