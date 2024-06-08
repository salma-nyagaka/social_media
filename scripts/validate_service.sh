# #!/bin/bash
# # Navigate to project directory
# cd /opt/twiga/social_media

# # Start Docker containers
# docker-compose up -d
#!/bin/bash
# Check if the application is running
# curl -f http://localhost:8000 || exit 1
#!/bin/bash

# URL to check
URL="http://localhost:8000"

# Perform the check
HTTP_RESPONSE=$(curl --write-out "%{http_code}" --silent --output /dev/null "$URL")

# Check if the HTTP response is 200 (OK)
if [ "$HTTP_RESPONSE" -ne 200 ]; then
  echo "Service validation failed. HTTP response code: $HTTP_RESPONSE"
  exit 1
else
  echo "Service validation succeeded. HTTP response code: $HTTP_RESPONSE"
  exit 0
fi
