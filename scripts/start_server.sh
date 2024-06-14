#!/bin/bash

# Navigate to the project directory
cd /opt/twiga/social_media

# Pull the latest Docker image
docker pull limsapi/social_media:latest

# Copy the .env file to the project directory
cp /opt/.env /opt/twiga/social_media/.env

docker-compose down
# Stop the existing container if it is running
docker stop social_media_app || true

# Remove the existing container if it exists
docker rm social_media_app || true

# Run the new container
docker run -d --name social_media_app limsapi/social_media:latest
