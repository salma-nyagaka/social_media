#!/bin/bash
set -e

# Navigate to the project directory
cd /opt/twiga/social_media

# Pull the latest Docker images
docker-compose pull

# Remove any existing containers
docker-compose down

# Start Docker containers without rebuilding every time
docker-compose up -d
