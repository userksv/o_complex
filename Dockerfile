FROM python:3.11-slim-buster

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /code

RUN apt-get update && \
    apt-get install -y build-essential python3-dev && \
    apt-get install -y --no-install-recommends gcc

COPY requirements.txt /code/

RUN pip install --upgrade pip && \
    pip install -r requirements.txt

COPY . /code/

RUN python manage.py makemigrations
RUN python manage.py migrate --no-input
