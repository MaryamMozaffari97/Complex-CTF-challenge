#!/bin/bash

# Create database migrations
python manage.py makemigrations

# Apply database migrations
echo "Apply database migrations"
python manage.py migrate

# Start server
echo "Starting server"
gunicorn --bind 0.0.0.0:8000 devhive.wsgi:application --workers 4