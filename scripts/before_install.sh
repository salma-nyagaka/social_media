#!/usr/bin/env bash

#!/bin/bash
DEPLOYMENT_GROUP=$(aws deploy list-deployment-groups --application-name credrails --output text --query "deploymentGroups[0]")
export DEPLOYMENT_GROUP


# Clean CodeDeploy-agent files for a fresh install
sudo rm -rf /home/ubuntu/install

# Install CodeDeploy agent
sudo apt-get -y update
sudo apt-get -y install ruby wget
cd /home/ubuntu
wget https://aws-codedeploy-us-east-1.s3.amazonaws.com/latest/install
sudo chmod +x ./install 
sudo ./install auto

# Update OS & install Python3
sudo apt-get update
# sudo apt-get install -y python3 python3-dev python3-pip python3-venv
# pip install --user --upgrade virtualenv

pip install -r requirements.txt

# Delete the app directory to ensure a clean installation
sudo rm -rf /opt/twiga/social_media
