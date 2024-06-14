#!/bin/bash

# Navigate to the project directory
cd /opt/twiga/social_media

# Run the new container
docker-compose build
docker-compose up -d
