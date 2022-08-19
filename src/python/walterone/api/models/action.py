from django.core.exceptions import ValidationError
from django.db import models
from django.db import transaction
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

    def save(self, *args, **kwargs):
        with transaction.atomic():
            match_ia = self.ia.matchia_set.get(match=self.match)
            match_ia.where_am_i = self.to_zone
            match_ia.save()
            super(Move, self).save(*args, **kwargs)

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
