# #!/bin/bash
# # Navigate to project directory
# cd /opt/twiga/social_media

# # Start Docker containers
# docker-compose up -d
#!/bin/bash
# Check if the application is running
curl -f http://localhost:8000 || exit 1
