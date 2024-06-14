# # #!/bin/bash
cd /opt/twiga/social_media


# Stop the existing container (if running)
docker stop # # #!/bin/bash
cd /opt/twiga/social_media


# Stop the existing container (if running)
docker stop social_media_project || true
docker stop social_media_app || true

# Remove the existing container
docker rm social_media_project || true
docker rm social_media_app || true



# Copy the .env file to the project directory
cp /opt/.env /opt/twiga/social_media/.env

docker-compose down
# Stop the existing container if it is running
docker stop social_media_app || true

# Remove the existing container if it exists
docker rm social_media_app || true
social_media_project || true
docker stop social_media_app || true

# Remove the existing container
docker rm social_media_project || true
docker rm social_media_app || true



# Copy the .env file to the project directory
cp /opt/.env /opt/twiga/social_media/.env

docker-compose down
# Stop the existing container if it is running
docker stop social_media_app || true

# Remove the existing container if it exists
docker rm social_media_app || true
