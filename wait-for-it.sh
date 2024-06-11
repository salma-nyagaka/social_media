#!/bin/sh

# Wait for PostgreSQL to be ready
until nc -z -v -w30 db 5432
do
  echo "Waiting for PostgreSQL database connection..."
  sleep 1
done

# Run the next command
exec "$@"
