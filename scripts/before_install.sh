#!/usr/bin/env bash

#!/bin/bash
DEPLOYMENT_GROUP=$(aws deploy list-deployment-groups --application-name credrails --output text --query "deploymentGroups[0]")
export DEPLOYMENT_GROUP


# Update OS & install Python3
sudo apt-get update
# sudo apt-get install -y python3 python3-dev python3-pip python3-venv
# pip install --user --upgrade virtualenv

pip install -r requirements.txt

# Delete the app directory to ensure a clean installation
sudo rm -rf /opt/twiga/social_media
