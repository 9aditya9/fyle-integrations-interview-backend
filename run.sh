#!/bin/bash

source venv/bin/activate

python manage.py migrate
python manage.py runserver 
