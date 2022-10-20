from random import randint

from django.conf import settings

from api.models.match import MatchIA


def set_lucky_unlucky(match_ia_id):
    """
    The IA has a 80% to avoid all the damage and
    20% to do damage in each attack
    """
    match_ia_instance = MatchIA.objects.get(id=match_ia_id)
    match_ia_instance.lucky_unlucky = settings.LUCKY_UNLUCKY_DEFAULT
    match_ia_instance.save()


def attacked_lucky_unlucky():
    """
    false: if lucky_unlucky disable or unlucky(>80%)
    true: if lucky_unlucky enable and lucky(<=80%)
    """
    lucky_value = False

    percentage = randint(1, 100)
    if percentage <= 80:
        lucky_value = True

    return lucky_value


def attacking_lucky_unlucky():
    """
    false: if lucky_unlucky disable or unlucky(>20%)
    true: if lucky_unlucky enable and lucky(<=20%)
    """
    unlucky_value = False

    percentage = randint(1, 100)
    if percentage <= 20:
        unlucky_value = True

    return unlucky_value


def set_go_ryu(match_ia_id):
    """
    The IA increase the damage between 40-50% 
    and increase the damage received between 40-50%
    """
    match_ia_instance = MatchIA.objects.get(id=match_ia_id)
    match_ia_instance.go_ryu = settings.GO_RYU_DEFAULT
    match_ia_instance.save()


def go_ryu(damage):
    """
    The IA increase the damage between 40-50% 
    and increase the damage received between 40-50%
    """

    percentage = randint(40, 50)
    return damage+int(damage*(percentage/100))


def set_karin_gift(match_ia_id):
    """
    The Ia recover a 20-30% of life lost
    """

    percentage = randint(20, 30)
    match_ia_instance = MatchIA.objects.get(id=match_ia_id)
    life_recovered = int(settings.LIFE_DEFAULT*(percentage/100))
    if life_recovered + match_ia_instance.life <= settings.LIFE_DEFAULT:
        match_ia_instance.life += life_recovered
        match_ia_instance.save()
