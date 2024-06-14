#!/bin/bash
# Navigate to project directory
cd /opt/twiga/social_media
docker pull limsapi/social_media:latest
cp /opt/.env /opt/twiga/social_media/.env
docker run -d --name social_media_app limsapi/social_media:latest