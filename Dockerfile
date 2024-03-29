FROM python:3.6 as build

WORKDIR /app
ADD . .
RUN pip install -r requirements/production.txt
ENTRYPOINT ENV_FOR_DYNACONF=production celery worker -A opulence.engine.app --queues=engine --loglevel=info --pool=gevent --hostname=engine_1@%h
