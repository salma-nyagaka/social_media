#!/bin/bash
set -e

# Navigate to the project directory
cd /opt/twiga/social_media


# Run the new container
# docker run -d --name social_media_app limsapi/social_media:latest
docker-compose build
docker-compose up -d
