#!/bin/sh

docker-compose run --rm web /usr/local/bin/python manage.py createsuperuser
