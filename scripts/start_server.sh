#!/bin/bash
# Navigate to project directory
cd /opt/twiga/social_media
docker-compose run web python manage.py makemigrations
docker-compose run web python manage.py migrate

# Start Docker containers
# docker-compose up --build -d
docker-compose up -d