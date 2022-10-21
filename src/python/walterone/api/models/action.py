from django.core.exceptions import ValidationError
from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver

from api.models.match import MatchIA


class Action(models.Model):
    timestamp = models.DateTimeField(
        auto_now_add=True
        )
    match = models.ForeignKey(
        'Match',
        on_delete=models.CASCADE
    )

    class Meta:
        abstract = True


class Attack(Action):
    damage = models.IntegerField(
        default=10
    )
    attack_from = models.ForeignKey(
        'IA',
        on_delete=models.CASCADE,
        null=False,
        related_name="attack_from"
    )
    attack_to = models.ForeignKey(
        'IA',
        on_delete=models.CASCADE,
        null=False,
        related_name="attack_to"
    )


class Defend(models.Model):
    shield = models.IntegerField(
        default=4
    )
    active = models.BooleanField(
        default=False
    )

    timestamp = models.TimeField(
        auto_now=True
        )

    match_ia = models.OneToOneField(
        'MatchIA',
        on_delete=models.CASCADE,
        null=False,
        related_name='defend'
    )


class Find(Action):
    zone = models.ForeignKey(
        'Zone',
        on_delete=models.CASCADE,
        null=False
    )

    ia = models.ForeignKey(
        'IA',
        on_delete=models.CASCADE,
        null=False
    )


class Move(Action):
    to_zone = models.ForeignKey(
        'Zone',
        on_delete=models.CASCADE
    )

    ia = models.ForeignKey(
        'IA',
        on_delete=models.CASCADE
    )

    active = models.BooleanField(
        default=True
    )

    @classmethod
    def set_where_am_i(cls, match_ia_id):
        match_ia = MatchIA.objects.get(id=match_ia_id)
        match_ia.where_am_i = cls.objects.filter(
            ia=match_ia.ia, match=match_ia.match).last().to_zone
        match_ia.save()

    @classmethod
    def check_neighbours(cls, instance):
        match_ia = instance.ia.matchia_set.get(match_id=instance.match.id)
        last_zone = match_ia.where_am_i
        if last_zone and last_zone != instance.to_zone:
            is_neighbours = last_zone.neighbors.filter(
                id=instance.to_zone.id
            )
            if not is_neighbours:
                msg = f"this zone is far far from here {instance.to_zone.id}"
                raise ValidationError(
                    {
                        'to_zone': msg
                    }
                )


@receiver(pre_save, sender=Move)
def signal_check_neighbours(sender, instance, **kwargs):
    sender.check_neighbours(instance)
