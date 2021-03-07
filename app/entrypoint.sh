#!/bin/sh
sleep 10
flask db migrate upgrade
celery -A wsgi:celery worker --workdir /app -D --logfile=celery.log
gunicorn --chdir /app -w 2 wsgi:app -b :5000
