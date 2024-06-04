# #!/bin/bash
# # This script runs after the Install phase
# # e.g., cleaning up, setting permissions
# #!/bin/bash
# echo "Before install script running..."
# # Remove existing Dockerfile if it exists
# if [ -f /var/www/twiga/social_media/social_media_project/Dockerfile ]; then
#     rm /var/www/twiga/social_media/social_media_project/Dockerfile
# fi

# # Navigate to app directory
# cd /var/www/twiga/social_media/social_media_project

# # Pull the latest code
# git pull origin develop

# # Build Docker image
# docker build -t django-app .:latest .

# # Stop the currently running container
# docker stop django-app-container || true

# # Remove the stopped container
# docker rm django-app-container || true

# # Run a new container with the latest image
# docker run -d --name django-app-container -p 80:80 django-app:latest
#!/bin/bash
# echo "After install script running..."
# cd /var/www/twiga/social_media/social_media_project
# # Stop and remove any running container to avoid conflicts
# sudo docker stop myapp || true
# sudo docker rm myapp || true
# docker build -t myapp .
# sudo docker run -d -p 80:80 --name myapp myapp


#!/bin/bash
#!/bin/bash
echo "After install script running..."
cd /var/www/twiga/social_media/social_media_project

# Stop and remove any running container to avoid conflicts
container_id=$(sudo docker ps -q --filter "name=myapp")
if [ -n "$container_id" ]; then
    echo "Stopping and removing existing container"
    sudo docker stop myapp
    sudo docker rm myapp
fi

# Build and run the new Docker container on a different port, e.g., 8080
sudo docker build -t myapp .
sudo docker run -d -p 8080:80 --name myapp myapp


