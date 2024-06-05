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

# Navigate to the project directory
sudo cd /var/www/twiga/social_media/social_media_project || exit

# Ensure git is installed
if command -v git >/dev/null 2>&1; then
    echo "Updating repository..."
    if [ ! -d .git ]; then
        git init
        git remote add origin https://github.com/salma-nyagaka/social_media.git
        git fetch
    fi
    git pull origin main || { echo "git pull failed"; exit 1; }
else
    echo "git command not found"
    exit 1
fi


echo "Before install script completed."