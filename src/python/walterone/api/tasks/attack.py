from random import randint

from django.conf import settings

from api.models.action import Defend
from api.models.match import MatchIA
from walterone.celery import app


def get_range_value(percentage, top_value):
    return randint(top_value-int(top_value*percentage/100), top_value)


@app.task(bind=True)
def attack_task(self, attacked_ia_id, match_id, damage):
    match_ia = MatchIA.objects.get(ia=attacked_ia_id, match=match_id)
    if Defend.objects.filter(match_ia=match_ia) and match_ia.defend.active:
        reduced = get_range_value(settings.DEFEND_RANGE_PERCENTAGE, match_ia.defend.shield)
    else:
        reduced = 0
    damage_range_result = get_range_value(settings.DAMAGE_RANGE_PERCENTAGE, damage)
    match_ia.life -= damage_range_result + reduced
    if match_ia.life <= 0:
        match_ia.alive = False
    match_ia.save()
