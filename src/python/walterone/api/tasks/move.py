from api.event_triggers import \
    set_lucky_unlucky,\
    set_go_ryu,\
    set_karin_gift
from api.models.action import Move
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
def where_am_i_task(self, match_ia_id):
    Move.set_where_am_i(match_ia_id)
