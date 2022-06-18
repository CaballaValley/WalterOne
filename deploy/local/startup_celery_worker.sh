#!/bin/sh

if [ ! -f config/env/.env.local ]
then
  export $(cat config/env/.env.local | xargs)
fi

cd src/python/walterone

celery -A api worker -l INFO