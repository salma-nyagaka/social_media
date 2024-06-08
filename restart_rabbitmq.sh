#!/bin/sh

# Identify the process using port 5672
PID=$(lsof -t -i:5672)

# If a process is found, kill it
if [ -n "$PID" ]; then
  kill -9 $PID
  echo "Killed process $PID using port 5672"
else
  echo "No process found using port 5672"
fi

# Execute the command passed to the script
exec "$@"
