from api.event_triggers import set_lucky_unlucky
from walterone.celery import app


@app.task(bind=True)
def lucky_unlucky_task(self, match_ia_id):
    set_lucky_unlucky(match_ia_id)
