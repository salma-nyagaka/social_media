#!/bin/bash
# Navigate to project directory
cd /opt/twiga/social_media
docker pull limsapi/social_media:latest

docker run -d --env-file /opt/.env --name social_media_app limsapi/social_media:latest