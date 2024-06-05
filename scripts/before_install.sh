#!/bin/bash
echo "Before install script running..."
# Remove existing files if they exist
if [ -f /var/www/twiga/social_media/social_media_project/Dockerfile ]; then
    sudo rm /var/www/twiga/social_media/social_media_project/Dockerfile
fi


# Ensure sudo is available and stop any service running on port 80
if command -v sudo >/dev/null 2>&1; then
    echo "Stopping any process on port 80"
    sudo fuser -k 80/tcp || true
else
    echo "sudo command not found"
    exit 1
fi

# Add any additional cleanup commands here
# Add any additional cleanup commands here
docker stop $(docker ps -q) || true
docker rm $(docker ps -a -q) || true

# Fetch the latest code from the Git repository
if [ -d /var/www/twiga/social_media/social_media_project ]; then
    cd /var/www/twiga/social_media/social_media_project
    sudo git pull
