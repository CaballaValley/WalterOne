from walterone.celery import app

@app.task(bind=True)
def attack_task(self, data):
    print(f'Request: {data}')
