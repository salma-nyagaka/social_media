#!/bin/bash
echo "After install script running..."

# Stop and remove any running container to avoid conflicts
sudo docker stop social_media_app || true
sudo docker rm social_media_app || true

# Copy the latest files to the target directory
sudo cp -r /opt/twiga/social_media/social_media_project /opt/twiga/social_media/deployed_app

# Navigate to the project directory
cd /opt/twiga/social_media/social_media_project

# Build and run the new container with the new name
sudo docker build -t social_media_image .
sudo docker run -d -p 8080:8000 --name social_media_app social_media_image
