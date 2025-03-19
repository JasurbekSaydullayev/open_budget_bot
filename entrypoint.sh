#!/bin/bash

python manage.py makemigrations
python manage.py migrate

python manage.py runbot &
python manage.py runserver 0.0.0.0:707 &

wait
