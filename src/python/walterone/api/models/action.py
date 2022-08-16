from django.core.exceptions import ValidationError
from django.db import models


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

    def clean(self):
        last_move = self.ia.move_set.latest('timestamp')
        is_neighbours = last_move.to_zone.neighbors.filter(id=self.to_zone.id)
        if not is_neighbours:
            raise ValidationError(
                {'to_zone': "this zone is far far from here"})
