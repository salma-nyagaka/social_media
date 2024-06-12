#!/bin/bash
# Navigate to project directory
cd /opt/twiga/social_media
docker-compose run web python manage.py makemigrations
docker-compose run web python manage.py migrate

# Start Docker containers without rebuilding every time
docker-compose up -d
