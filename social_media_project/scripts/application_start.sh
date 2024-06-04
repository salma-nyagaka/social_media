#!/bin/bash

# Navigate to app directory
cd /var/www/twiga/social_media/social_media_project

# Pull the latest code
git pull origin develop

# Build Docker image
docker build -t django-app .:latest .

# Stop the currently running container
docker stop django-app-container || true

# Remove the stopped container
docker rm django-app-container || true

# Run a new container with the latest image
docker run -d --name django-app-container -p 80:80 django-app:latest
