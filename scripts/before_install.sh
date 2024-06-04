# #!/bin/bash
# # This script runs before the Install phase
# # e.g., stopping services or backing up data
# #!/bin/bash
# #!/bin/bash

# # Any other necessary cleanup or preparation commands can be added here
# docker stop $(docker ps -q) || true
# docker rm $(docker ps -a -q) || true


#!/bin/bash
echo "Before install script running..."
# Remove existing files if they exist
if [ -f /var/www/twiga/social_media/social_media_project/Dockerfile ]; then
    sudo rm /var/www/twiga/social_media/social_media_project/Dockerfile
fi
# Add any additional cleanup commands here

sudo fuser -k 80/tcp
