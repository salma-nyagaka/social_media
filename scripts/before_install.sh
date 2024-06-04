#!/bin/bash
# This script runs before the Install phase
# e.g., stopping services or backing up data
#!/bin/bash
#!/bin/bash
echo "Before install script running..."
# Remove existing Dockerfile if it exists
if [ -f /var/www/twiga/social_media/social_media_project/Dockerfile ]; then
    rm /var/www/twiga/social_media/social_media_project/Dockerfile
fi
# Any other necessary cleanup or preparation commands can be added here
docker stop $(docker ps -q) || true
docker rm $(docker ps -a -q) || true


