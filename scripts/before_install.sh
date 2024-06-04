#!/bin/bash
# This script runs before the Install phase
# e.g., stopping services or backing up data
#!/bin/bash
docker stop $(docker ps -q) || true
docker rm $(docker ps -a -q) || true
