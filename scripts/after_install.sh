#!/bin/bash

# Navigate to the project directory
cd /opt/twiga/social_media

# Stop and remove the existing container (if running)
sudo docker stop social_media_project || true
sudo docker stop social_media_app || true
sudo docker rm social_media_project || true
sudo docker rm social_media_app || true

# Remove all Docker volumes
sudo docker volume rm $(docker volume ls -q) || true

# Copy the .env file to the project directory
cp /opt/.env /opt/twiga/social_media/.env

# Bring down any existing containers
sudo docker-compose down

# Remove any existing containers
sudo docker stop social_media_app || true
sudo docker rm social_media_app || true
