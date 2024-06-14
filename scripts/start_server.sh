#!/bin/bash
# Navigate to project directory
cd /opt/twiga/social_media

docker-compose pull
docker-compose up -d --build
