# FROM python:3.12-slim

# # Set the working directory in the container
# WORKDIR /app

# # Install system dependencies and build tools
# RUN apt-get update && apt-get install -y \
#     build-essential \
#     libpq-dev \
#     gcc \
#     gfortran \
#     libopenblas-dev \
#     liblapack-dev \
#     && rm -rf /var/lib/apt/lists/*

# # Copy the current directory contents into the container at /app
# COPY . /app

# # Install any needed packages specified in requirements.txt
# RUN pip install --upgrade pip setuptools wheel
# RUN pip install --no-cache-dir -r requirements.txt

# # Ensure gunicorn is installed
# RUN pip install gunicorn

# # Verify that gunicorn is installed and available in the PATH
# RUN echo "Verifying gunicorn installation..." && gunicorn --version

# # Make port 8000 available to the world outside this container
# EXPOSE 8000

# # Define environment variable
# ENV NAME World
# ENV DJANGO_SETTINGS_MODULE social_media_project.settings

# # Run gunicorn when the container launches
# CMD ["gunicorn", "--bind", "0.0.0.0:8000", "social_media_project.wsgi:application"]
# Use an official Python runtime as a parent image
FROM python:3.12-slim

# Set the working directory in the container
WORKDIR /app

# Install system dependencies and build tools
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    gcc \
    gfortran \
    libopenblas-dev \
    liblapack-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements.txt first for better caching
COPY requirements.txt .

# Upgrade pip, setuptools, and wheel
RUN pip install --upgrade pip setuptools wheel

# # Install packages only if requirements.txt has changed
# RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Ensure gunicorn is installed
RUN pip install gunicorn

# Verify that gunicorn is installed and available in the PATH
RUN echo "Verifying gunicorn installation..." && gunicorn --version

# Make port 8000 available to the world outside this container
EXPOSE 8000

# Define environment variables
ENV NAME World
ENV DJANGO_SETTINGS_MODULE social_media_project.settings

# Run gunicorn when the container launches
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "social_media_project.wsgi:application"]
