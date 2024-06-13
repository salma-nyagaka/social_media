#!/bin/bash
set -e

# Navigate to the project directory
cd /opt/twiga/social_media

# Check if the .env file exists, create if it doesn't
if [ ! -f .env ]; then
  echo "Creating .env file..."
  echo "SECRET_KEY=${SECRET_KEY}" > .env
  echo "DATABASE_URL=${DATABASE_URL}" >> .env
  echo "EMAIL_HOST_PASSWORD=${EMAIL_HOST_PASSWORD}" >> .env
  echo "DEFAULT_FROM_EMAIL=${DEFAULT_FROM_EMAIL}" >> .env
  echo "DOMAIN_NAME=${DOMAIN_NAME}" >> .env
fi

# Pull the latest Docker images
docker-compose pull

# Remove any existing containers
docker-compose down

# Start Docker containers without rebuilding every time
docker-compose up -d --build
