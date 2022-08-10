from walterone.celery import app

@app.task(bind=True)
def attack_task(self, data):
    # from celery.contrib import rdb
    # rdb.set_trace()
    print(f'Request: data')
