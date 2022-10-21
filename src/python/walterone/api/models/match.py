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

    damage = models.IntegerField(default=12)

    def __str__(self):
        return f"{self.name}: {self.map.name}"


class MatchIA(models.Model):
    ia = models.ForeignKey(
        'IA',
        on_delete=models.CASCADE,
        null=False
    )
    match = models.ForeignKey(
        'Match',
        on_delete=models.CASCADE,
        null=False
    )

    where_am_i = models.ForeignKey(
        'Zone',
        on_delete=models.CASCADE,
        null=False
    )

    life = models.IntegerField(default=200)

    alive = models.BooleanField(default=True)

    lucky_unlucky = models.IntegerField(
        default=0
    )

    go_ryu = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.match}: {self.ia} ({self.life})"

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
