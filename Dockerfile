FROM python:3.8.2

ENV IS_CONTAINER=true
WORKDIR /app

RUN apt-get update
RUN pip install psycopg2 openpyxl python-dateutil

COPY . /app