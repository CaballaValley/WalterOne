from django.dispatch import receiver
from django.db.models.signals import post_save

from api.models.action import Attack, Move
from api.tasks.attack import attack_task
from api.tasks.move import lucky_unlucky_task


@receiver(post_save, sender=Attack)
def send_attack_to_celery(sender, instance, **kwargs):
    attack_task.apply_async(
        (instance.attack_from_id,
         instance.attack_to_id,
         instance.match_id,
         instance.damage))


@receiver(post_save, sender=Move)
def lucky_unlucky_task_to_celery(sender, instance, **kwargs):
    if instance.to_zone.lucky_unlucky:
        match_ia_id = instance.ia.matchia_set.get(match_id=instance.match.id).id
        lucky_unlucky_task.apply_async(
            (match_ia_id,))
