# #!/bin/bash
# # This script runs after the Install phase
echo "After install script running..."
cd /var/www/twiga/social_media/social_media_project

# Stop and remove any running container to avoid conflicts
sudo docker stop mmm || true
sudo docker rm mmm || true

sudo cp -r /var/www/twiga/social_media/social_media_project /var/www/twiga/social_media/deployed_app


# Build and run the new container
sudo docker build -t mmm .
sudo docker run -d -p 8080:8000 --name mmm mmm


