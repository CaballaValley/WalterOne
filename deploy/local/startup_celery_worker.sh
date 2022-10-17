#!/bin/sh

if [ -f config/env/.env.local ]
then
  export $(cat config/env/.env.local | xargs)
fi

cd src/python/walterone

celery -A walterone worker -l DEBUG --concurrency 1