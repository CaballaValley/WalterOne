from api.celery import app

@app.task(bind=True)
def attack_task(data):
    print(f'Request: {data}')
