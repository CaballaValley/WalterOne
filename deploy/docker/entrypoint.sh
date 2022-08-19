#!/bin/sh

if [ "$DATABASE" = "postgres" ]
then
    echo "Waiting for postgres..."

    while ! nc -z $SQL_HOST $SQL_PORT; do
      sleep 0.1
    done

    echo "PostgreSQL started"
fi

cd /usr/src/app

python manage.py migrate
python manage.py loaddata fixtures/fixtures.json

celery -A walterone worker -l DEBUG -d

exec "$@"
