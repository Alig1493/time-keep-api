FROM python:3.9.4-slim-buster
WORKDIR /app

ENV PYTHONUNBUFFERED=1

COPY ./requirements.txt requirements.txt
RUN apt-get update && apt-get install iputils-ping libpq-dev gcc -y
RUN pip install -r requirements.txt --no-cache-dir

COPY . .
RUN useradd backend
RUN chown -R backend:backend .
USER backend
RUN ./manage.py collectstatic --no-input
