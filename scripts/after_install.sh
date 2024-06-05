# #!/bin/bash
# # This script runs after the Install phase
echo "After install script running..."
cd /var/www/twiga/social_media/social_media_project

# Stop and remove any running container to avoid conflicts
sudo docker stop myapp || true
sudo docker rm myapp || true

# Build and run the new container
sudo docker build -t myapp .
sudo docker run -d -p 8080:8000 --name myapp myapp


