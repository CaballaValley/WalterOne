from django.db import models

# Create your models here.

class IA(models.Model):
    name = models.CharField(
        null=False,
        blank=False,
        max_length=32
    )