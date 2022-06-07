from django.db import models


class Action(models.Model):
    timestamp = models.TimeField(
        auto_now_add=True
        )
    match_ia = models.ForeignKey(
        'MatchIA',
        on_delete=models.CASCADE
    )

    class Meta:
        abstract = True

class Attack(Action):
    damage = models.IntegerField(
        default=10
    )
    attack_to = models.ForeignKey(
        'IA',
        on_delete=models.CASCADE,
        null=False
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

