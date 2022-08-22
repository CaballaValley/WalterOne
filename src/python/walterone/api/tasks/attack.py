from api.models.match import MatchIA
from walterone.celery import app

@app.task(bind=True)
def attack_task(self, attacked_ia_id, match_id, damage):
    match_ia = MatchIA.objects.get(ia=attacked_ia_id, match=match_id)
    reduced = match_ia.defend.shield if match_ia.defend and match_ia.defend.active else 0
    match_ia.life -= damage + reduced
    if match_ia.life <= 0:
        match_ia.alive = False
    match_ia.save()
