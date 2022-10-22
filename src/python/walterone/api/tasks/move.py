from api.event_triggers import \
    set_lucky_unlucky,\
    set_go_ryu,\
    set_karin_gift
from api.models.match import MatchIA
from api.models.zone import Zone
from walterone.celery import app


@app.task(bind=True)
def lucky_unlucky_task(self, match_ia_id):
    set_lucky_unlucky(match_ia_id)


@app.task(bind=True)
def go_ryu_task(self, match_ia_id):
    set_go_ryu(match_ia_id)


@app.task(bind=True)
def karin_gift_task(self, match_ia_id):
    set_karin_gift(match_ia_id)


@app.task(bind=True)
def where_am_i_task(self, zone_id, match_ia_id):
    match_ia = MatchIA.objects.get(id=match_ia_id)
    match_ia.where_am_i = Zone.objects.get(id=zone_id)
    match_ia.save()
