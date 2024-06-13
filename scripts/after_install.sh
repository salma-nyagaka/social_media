#!/usr/bin/env bash

# Kill any servers that may be running in the background 
sudo pkill -f runserver


# Change to the app directory
cd /opt/twiga/social_media


# Activate the virtual environment
virtualenv venv
source venv/bin/activate

source .env

# Install Python dependencies
pip install -r /opt/twiga/social_media/requirements.txt
pip install psycopg2-binary

systemctl restart apacge