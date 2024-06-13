#!/bin/bash
set -e

# Navigate to the project directory
cd /opt/twiga/social_media



docker-compose up -d --build

# # Pull the latest Docker images
# docker-compose pull

# # Remove any existing containers
# docker-compose down

# # Start Docker containers without rebuilding every time
# docker build -t  limsapi/social_media:latest .

# docker-compose up -d
