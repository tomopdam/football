#!/bin/sh

python3 manage.py migrate --no-input
python3 manage.py collectstatic --no-input

# gunicorn --reload is obviously not used on production
gunicorn --reload footballtool.wsgi:application --bind 0.0.0.0:8000
