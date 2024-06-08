# Use the official Python image from the Docker Hub
FROM python:3.12-slim

# Install system dependencies for building Python packages
RUN apt-get update && apt-get install -y \
    build-essential \
    libssl-dev \
    libffi-dev \
    python3-dev \
    libjpeg-dev \
    zlib1g-dev \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install psycopg2-binary
# Copy the rest of your application code into the container
COPY . .

# Command to run your application
CMD ["python", "app.py"]
#  Make port 8000 available to the world outside this container
# EXPOSE 8000

# # Define environment variable
# ENV NAME World

# # Run Gunicorn server
# CMD ["gunicorn", "--workers", "3", "--bind", "0.0.0.0:8000", "your_project_name.wsgi:application"]