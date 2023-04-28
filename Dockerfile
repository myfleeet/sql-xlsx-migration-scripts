FROM python:3.8.2

WORKDIR /app

RUN apt-get update
RUN pip install psycopg2 openpyxl

COPY . /app