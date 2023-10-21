from random import randint

from django.conf import settings

from api.event_triggers import attacked_lucky_unlucky, attacking_lucky_unlucky, go_ryu
from api.models.action import Defend, FinalDamage, Attack
from api.models.match import MatchIA
from walterone.celery import app


def get_range_value(percentage, top_value):
    return randint(top_value-int(top_value*percentage/100), top_value)


def get_defend_value(match_ia, damage):
    if Defend.objects.filter(match_ia=match_ia) and match_ia.defend.active:
        defend_value = get_range_value(
            settings.DEFEND_RANGE_PERCENTAGE,
            match_ia.defend.shield)
    else:
        defend_value = 0

    if match_ia.go_ryu > 0:
        match_ia.go_ryu -= 1
        defend_value += go_ryu(damage)

    return defend_value


def get_attacker_damage(match_ia, damage):
    if Defend.objects.filter(match_ia=match_ia) and match_ia.defend.active:
        defend_value = get_range_value(
            settings.DEFEND_RANGE_PERCENTAGE,
            match_ia.defend.shield)
    else:
        defend_value = 0

    if match_ia.go_ryu > 0:
        match_ia.go_ryu -= 1
        match_ia.save()
        damage = go_ryu(damage)

    return damage - defend_value


@app.task(bind=True)
def attack_task(self, attack_id, attacker_ia_id, attacked_ia_id, match_id, damage):
    match_ia_attacked = MatchIA.objects.get(ia=attacked_ia_id, match=match_id)
    match_ia_attacker = MatchIA.objects.get(ia=attacker_ia_id, match=match_id)

    is_lucky = False
    if match_ia_attacked.lucky_unlucky > 0:
        is_lucky = attacked_lucky_unlucky()
        match_ia_attacked.lucky_unlucky -= 1

    is_unlucky = False
    if match_ia_attacker.lucky_unlucky > 0:
        is_unlucky = attacking_lucky_unlucky()
        match_ia_attacker.lucky_unlucky -= 1
        match_ia_attacker.save()

    final_damage = 0
    if not is_lucky or not is_unlucky:
        reduced = get_defend_value(match_ia_attacked, damage)
        induced = get_attacker_damage(match_ia_attacker, damage)

        final_damage = induced - reduced
        if final_damage < 0:
            final_damage = 0

        match_ia_attacked.life -= final_damage


    match_ia_attacked.alive = match_ia_attacked.life >= 0

    match_ia_attacked.save()

    damage = FinalDamage.objects.create(
        match_id=match_id,
        compute_damage=final_damage,
        attack_to=match_ia_attacked.ia.name,
        attack_to_role=match_ia_attacked.ia.role,
        attack_from_role=match_ia_attacker.ia.role,
        attack_from=match_ia_attacker.ia.name)
    damage.save()
