# # #!/bin/bash
# # echo "After install script running..."

# # # Stop and remove any running container to avoid conflicts
# # sudo docker stop myapp || true
# # sudo docker rm myapp || true

# # # Copy the latest files to the target directory
# sudo cp -r /home/ubuntu/opt/twiga/social_media/social_media_project /home/ubuntu/opt/twiga/social_media/deployed_app

# # # Navigate to the project directory
# # cd /home/ubuntu/opt/twiga/social_media/social_media_project

# # # Build and run the new container with the new name
# # sudo docker build -t social_media_image .
# # sudo docker run -d -p 8080:8000 --name myapp myapp

# #!/bin/bash
# echo "After install script running..."

# # Stop and remove any running container to avoid conflicts
# sudo docker stop myapp || true
# sudo docker rm myapp || true

# # Copy the latest files to the target directory
# sudo cp -r /home/ubuntu/opt/twiga/social_media/social_media_project /home/ubuntu/opt/twiga/social_media/deployed_app

# # Navigate to the project directory
# cd /home/ubuntu/opt/twiga/social_media/social_media_project

# # Build the Docker image
# sudo docker build -t social_media_image .

# # Run the new container with the correct image name
# sudo docker run -d -p 8080:8000 --name myapp social_media_image
#!/bin/bash
# Navigate to project directory
# cd /opt/twiga/social_media

# # Build Docker containers
# docker-compose down
# docker-compose up --build
#!/bin/bash
# Navigate to project directory
cd /opt/twiga/social_media


# Pull the pre-built Docker images
# docker-compose pull


# Remove any existing containers
docker-compose down

docker pull limsapi/social_media:latest
