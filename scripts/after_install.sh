#!/bin/bash
set -e

# Navigate to the project directory
cd /opt/twiga/social_media

# Stop the existing container (if running)
docker stop social_media_project || true
docker stop social_media_app || true

# Remove the existing container
docker rm social_media_project || true
docker rm social_media_app || true

# Copy the .env file to the project directory
cp /opt/.env /opt/twiga/social_media/.env

# Bring down any existing containers
docker-compose down

# Remove any existing containers
docker stop social_media_app || true
docker rm social_media_app || true
