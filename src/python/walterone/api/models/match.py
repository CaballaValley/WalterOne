from django.db import models


class Match(models.Model):
    name = models.CharField(
        null=False,
        blank=False,
        max_length=32
    )

    map = models.ForeignKey(
        'Map',
        null=False,
        on_delete=models.CASCADE
    )

    ias = models.ManyToManyField(
        'IA',
        through='MatchIA'
    )

    damage = models.IntegerField(default=8)


class MatchIA(models.Model):
    ia = models.ForeignKey(
        'IA',
        on_delete=models.CASCADE
    )
    match = models.ForeignKey(
        'Match',
        on_delete=models.CASCADE
    )

    life = models.IntegerField(default=50)
