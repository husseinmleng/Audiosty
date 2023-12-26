#!/bin/sh

gunicorn -b :5000 --access-logfile - --error-logfile - wsgi:flaskApp