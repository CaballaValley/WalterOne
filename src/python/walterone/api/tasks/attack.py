from random import randint

from django.conf import settings

from api.event_triggers import attacked_lucky_unlucky, attacking_lucky_unlucky
from api.models.action import Defend
from api.models.match import MatchIA
from walterone.celery import app


def get_range_value(percentage, top_value):
    return randint(top_value-int(top_value*percentage/100), top_value)


def get_defend_value(match_ia):
    if Defend.objects.filter(match_ia=match_ia) and match_ia.defend.active:
        defend_value = get_range_value(
            settings.DEFEND_RANGE_PERCENTAGE,
            match_ia.defend.shield)
    else:
        defend_value = 0

    return defend_value


def calculate_damage(attacker_ia_id, match_id, reduced, damage):
    match_ia_attacker = MatchIA.objects.get(ia=attacker_ia_id, match=match_id)

    is_unlucky = False
    if match_ia_attacker.lucky_unlucky > 0:
        is_unlucky = attacking_lucky_unlucky()
        match_ia_attacker.lucky_unlucky -= 1
        match_ia_attacker.save()

    calculated_damage = 0
    if not is_unlucky:
        damage_reduced = get_defend_value(match_ia_attacker)

        damage_range_result = get_range_value(
                settings.DAMAGE_RANGE_PERCENTAGE,
                damage-damage_reduced)

        calculated_damage = damage_range_result + reduced

    return calculated_damage


@app.task(bind=True)
def attack_task(self, attacker_ia_id, attacked_ia_id, match_id, damage):
    match_ia_attacked = MatchIA.objects.get(ia=attacked_ia_id, match=match_id)

    is_lucky = False
    if match_ia_attacked.lucky_unlucky > 0:
        is_lucky = attacked_lucky_unlucky()
        match_ia_attacked.lucky_unlucky -= 1

    if not is_lucky:
        reduced = get_defend_value(match_ia_attacked)
        match_ia_attacked.life -= calculate_damage(
            attacker_ia_id, match_id, reduced, damage)

    match_ia_attacked.alive = match_ia_attacked.life >= 0

    match_ia_attacked.save()
