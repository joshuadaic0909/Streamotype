#!/bin/bash
###########
envsubst '$FLASK_HOST $FLASK_PORT' < ./nginx.conf.d > /etc/nginx/nginx.conf
cat /etc/nginx/nginx.conf
service nginx start


gunicorn --access-logfile - --error-logfile - run:app --bind "0.0.0.0:$FLASK_PORT" 
