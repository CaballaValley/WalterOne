from bdb import set_trace
from django.dispatch import receiver
from django.db.models.signals import post_save

from api.models.action import Attack
from api.tasks.attack import attack_task


@receiver(post_save, sender=Attack)
def send_attack_to_celery(sender, instance, **kwargs):
    attack_task.apply_async((instance.attack_to_id, instance.match_id, instance.damage))