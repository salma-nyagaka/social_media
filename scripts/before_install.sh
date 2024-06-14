#!/bin/bash

# Clean up unnecessary files to free up space
sudo apt-get clean
sudo rm -rf /var/lib/apt/lists/*
sudo rm -rf /var/log/*
sudo rm -rf /tmp/*
sudo rm -rf /var/tmp/*

# Stop and remove all Docker containers
docker stop $(docker ps -a -q) || true
docker rm $(docker ps -a -q) || true

# Remove all Docker volumes
docker volume rm $(docker volume ls -q) || true

# Remove all Docker networks
docker network rm $(docker network ls -q) || true

# Remove unused Docker resources including networks, images, containers, and volumes
docker system prune -a -f --volumes

# Start and enable Docker
sudo systemctl start docker
sudo systemctl enable docker
