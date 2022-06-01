# pull official base image
FROM python:3.9.6-alpine

# set work directory
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install psycopg2 dependencies
RUN apk update \
    && apk add postgresql-dev gcc python3-dev musl-dev build-base bash

# install dependencies
RUN pip install --upgrade pip
COPY ./config/dependencies/requirements.txt .
RUN pip install psycopg2
RUN pip install -r requirements.txt
# copy entrypoint.sh
COPY ./deploy/docker/entrypoint.sh /walterwhite-entrypoint.sh
RUN sed -i 's/\r$//g' /walterwhite-entrypoint.sh
RUN chmod +x /walterwhite-entrypoint.sh

# copy project
COPY ./src/python/walterone .

# run entrypoint.sh
ENTRYPOINT ["/walterwhite-entrypoint.sh"]
