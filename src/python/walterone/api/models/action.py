from django.db import models

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

    def __str__(self):
        attack_to_match_ia = MatchIA.objects.get(
            match=self.match,
            ia=self.attack_to)
        return str(
            f"{self.timestamp} ({self.id}) - {self.attack_from} strikes with base damage {self.damage} to IA {attack_to_match_ia.ia}"
        )

class FinalDamage(models.Model):
    ''' Damage of an attack. '''
    # TODO juanma obliterate me to do this
    # please, if somebody read this code, change it in a good way with normal relations
    attack_from = models.CharField(max_length=20, default="")
    attack_from_role = models.CharField(max_length=20, default="BergenToy")
    attack_to = models.CharField(max_length=20, default="")
    attack_to_role = models.CharField(max_length=20, default="BergenToy")
    compute_damage = models.IntegerField(
        default=0
    )
    match_id = models.IntegerField(default=2)
    timestamp = models.DateTimeField(
        auto_now=True
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

    def __str__(self):
        return str(
            f"{self.timestamp} ({self.id})- {self.ia} moves to zone {self.to_zone.name}"
        )

    @classmethod
    def set_where_am_i(cls, match_ia_id):
        match_ia = MatchIA.objects.get(id=match_ia_id)
        match_ia.where_am_i = cls.objects.filter(
            ia=match_ia.ia, match=match_ia.match).last().to_zone
        match_ia.save()

