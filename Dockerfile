FROM python:3.8-slim

ENV PYTHONUNBUFFERED 1

WORKDIR /opt/services/djangoapp/src
COPY . /opt/services/djangoapp/src/

RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc g++ libpq-dev && \
    pip install psycopg2-binary && \
    pip --no-cache-dir install --upgrade pip && \
    pip --no-cache-dir install --requirement requirements/production.txt && \
    apt-get remove -y gcc g++ && \
    apt-get autoremove -y && \
    rm -rf /var/lib/apt/lists/*

EXPOSE 8000

