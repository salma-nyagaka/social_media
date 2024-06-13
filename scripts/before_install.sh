#!/bin/bash
set -e

# Clean up unnecessary files to free up space
sudo apt-get clean
sudo rm -rf /var/lib/apt/lists/*
sudo rm -rf /var/log/*
sudo rm -rf /tmp/*
sudo rm -rf /var/tmp/*


# Start and enable Docker
sudo systemctl start docker
sudo systemctl enable docker

# Ensure the target directory is clean
sudo rm -rf /opt/twiga/social_media/
