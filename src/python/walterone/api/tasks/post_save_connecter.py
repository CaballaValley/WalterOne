from django.dispatch import receiver
from django.db.models.signals import post_save

from api.models.action import Attack, Move
from api.tasks.attack import attack_task
from api.tasks.move import \
    lucky_unlucky_task,\
    go_ryu_task,\
    karin_gift_task,\
    where_am_i_task


@receiver(post_save, sender=Attack)
def send_attack_to_celery(sender, instance, **kwargs):
    attack_task.apply_async(
        (instance.id,
         instance.attack_from_id,
         instance.attack_to_id,
         instance.match_id,
         instance.damage))


@receiver(post_save, sender=Move)
def lucky_unlucky_task_to_celery(sender, instance, **kwargs):
    if instance.to_zone.lucky_unlucky:
        match_ia_id = instance.ia.matchia_set.get(match_id=instance.match.id).id
        lucky_unlucky_task.apply_async(
            (match_ia_id,))


@receiver(post_save, sender=Move)
def go_ryu_task_to_celery(sender, instance, **kwargs):
    if instance.to_zone.go_ryu:
        match_ia_id = instance.ia.matchia_set.get(match_id=instance.match.id).id
        go_ryu_task.apply_async(
            (match_ia_id,))


@receiver(post_save, sender=Move)
def karin_gift_task_to_celery(sender, instance, **kwargs):
    if instance.to_zone.karin_gift:
        match_ia_id = instance.ia.matchia_set.get(match_id=instance.match.id).id
        karin_gift_task.apply_async(
            (match_ia_id,))


@receiver(post_save, sender=Move)
def where_am_i_task_to_celery(sender, instance, **kwargs):
    match_ia_id = instance.ia.matchia_set.get(match_id=instance.match.id).id
    where_am_i_task.apply_async((instance.to_zone.id, match_ia_id,))
