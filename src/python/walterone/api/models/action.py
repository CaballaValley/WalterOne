from django.core.exceptions import ValidationError
from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver


class Action(models.Model):
    timestamp = models.TimeField(
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
        null=True,
        related_name="attack_from"
    )
    attack_to = models.ForeignKey(
        'IA',
        on_delete=models.CASCADE,
        null=False,
        related_name="attack_to"
    )

class Defend(Action):
    shield = models.IntegerField(
        default=4
    )
    active = models.BooleanField(default=False)

    ia = models.ForeignKey(
        'IA',
        on_delete=models.CASCADE,
        null=True
    )

    class Meta:
        constraints = [
             models.UniqueConstraint(fields=['ia', 'match'], name='match_ia_defend')
        ]


class Find(Action):
    zone = models.ForeignKey(
        'Zone',
        on_delete=models.CASCADE
    )

class Move(Action):
    to_zone = models.ForeignKey(
        'Zone', 
        on_delete=models.CASCADE
    )

    ia = models.ForeignKey(
        'IA',
        on_delete=models.CASCADE,
        null=True
    )

    @classmethod
    def check_neighbours(cls, instance):
        last_moves = cls.objects.filter(ia=instance.ia, match=instance.match)
        if last_moves:
            last_move = last_moves.latest('timestamp')
            if last_move:
                is_neighbours = last_move.to_zone.neighbors.filter(
                    id=instance.to_zone.id)
                if not is_neighbours:
                    raise ValidationError(
                        {'to_zone': f"this zone is far far from here {instance.to_zone.id}"})


@receiver(pre_save, sender=Move)
def signal_check_neighbours(sender, instance, **kwargs):
    sender.check_neighbours(instance)
