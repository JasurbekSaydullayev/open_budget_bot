#!/bin/bash

python manage.py makemigrations
python manage.py migrate

python manage.py runserver 0.0.0.0:0707 &


exec python manage.py runbot
