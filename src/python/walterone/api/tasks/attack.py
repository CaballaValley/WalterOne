from django.conf import settings

from api.models.match import MatchIA
from walterone.celery import app

@app.task(bind=True)
def attack_task(self, attacked_ia_id, match_id, damage):
    match_ia = MatchIA.objects.get(ia=attacked_ia_id, match=match_id)
    match_ia.life -= damage
    match_ia.save()
