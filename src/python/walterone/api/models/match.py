from random import choice
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


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

    class Meta:
        constraints = [
             models.UniqueConstraint(fields=['ia', 'match'], name='match_ia')
        ]

    @classmethod
    def if_ia_in_match(cls, ia_id, match_id):
        queryset = cls.objects.filter(ia_id=ia_id, match_id=match_id)
        return queryset.exists()


@receiver(post_save, sender=MatchIA)
def move_ia_to_first_zone(sender, instance, created, **kwargs):
    if created:
        zones = [zone for zone in instance.match.map.zone_set.all()]
        zone = choice(zones)
        instance.match.move_set.create(to_zone=zone, ia=instance.ia)
