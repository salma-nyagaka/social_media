# # # # #!/bin/bash
# # # # echo "Before install script running..."
# # # # # Remove existing files if they exist
# # # if [ -f /opt/twiga/social_media ]; then
# # #     sudo rm /opt/twiga/social_media
# # # fi


# # # # # Ensure sudo is available and stop any service running on port 80
# # # # if command -v sudo >/dev/null 2>&1; then
# # # #     echo "Stopping any process on port 8080"
# # # #     sudo fuser -k 80/tcp || true
# # # # else
# # # #     echo "sudo command not found"
# # # #     exit 1
# # # # fi

# # # # # Add any additional cleanup commands here
# # # # # Add any additional cleanup commands here
# # # # docker stop $(docker ps -q) || true
# # # # docker rm $(docker ps -a -q) || true
# # # #!/bin/bash
# # # apt-get update
# # #!/bin/bash
# # # Clean up any existing Docker installations
# # sudo apt-get remove -y docker docker-engine docker.io containerd runc

# # # Install dependencies
# # sudo apt-get update
# # sudo apt-get install -y apt-transport-https ca-certificates curl software-properties-common

# # # Add Docker’s official GPG key
# # curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -

# # # Add Docker’s stable repository
# # sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"

# # # Update package list
# # sudo apt-get update

# # # Install Docker
# # sudo apt-get install -y docker-ce docker-ce-cli containerd.io

# # # Start and enable Docker
# # sudo systemctl start docker
# # sudo systemctl enable docker

# # # Install Docker Compose
# # sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
# # sudo chmod +x /usr/local/bin/docker-compose

# # # Remove the existing directory or file
# # sudo rm -rf /opt/twiga/social_media/

# #!/bin/bash
# # Clean up any existing Docker installations
# sudo apt-get remove -y docker docker-engine docker.io containerd runc

# # Install dependencies
# sudo apt-get update
# sudo apt-get install -y apt-transport-https ca-certificates curl software-properties-common

# # Add Docker’s official GPG key
# # curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -

# # Add Docker’s stable repository
# # sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"

# # Update package list
# sudo apt-get update

# # Install Docker
# # sudo apt-get install -y docker-ce docker-ce-cli containerd.io

# # Start and enable Docker
# sudo systemctl start docker
# sudo systemctl enable docker

# # Install Docker Compose
# # sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
# # sudo chmod +x /usr/local/bin/docker-compose

# # Remove the existing directory or file
# sudo rm -rf /opt/twiga/social_media/
#!/bin/bash

# Clean up any existing Docker installations
sudo apt-get remove -y docker docker-engine docker.io containerd runc

# Clean up unnecessary files to free up space
sudo apt-get clean
sudo rm -rf /var/lib/apt/lists/*
sudo rm -rf /var/log/*
sudo rm -rf /tmp/*
sudo rm -rf /var/tmp/*

# Remove all Docker containers, images, volumes, and networks
docker stop $(docker ps -aq) || true
docker rm $(docker ps -aq) || true
docker rmi -f $(docker images -aq) || true
docker volume rm $(docker volume ls -q) || true
docker network rm $(docker network ls | grep -v 'bridge\|host\|none' | awk '{print $1}') || true
docker system prune -a --volumes --force || true

# Install dependencies
sudo apt-get update
sudo apt-get install -y apt-transport-https ca-certificates curl software-properties-common

# Add Docker’s official GPG key
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -

# Add Docker’s stable repository
sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"

# Update package list
sudo apt-get update

# Install Docker
sudo apt-get install -y docker-ce docker-ce-cli containerd.io

# Start and enable Docker
sudo systemctl start docker
sudo systemctl enable docker

# Install Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Remove the existing directory or file
sudo rm -rf /opt/twiga/social_media/
