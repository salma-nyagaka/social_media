# # Use an official Python runtime as a parent image
# FROM python:3.12.1-slim

# # Set the working directory in the container
# WORKDIR /app

# # Copy the current directory contents into the container at /app
# COPY . /app

# # Install any needed packages specified in requirements.txt
# RUN pip install --no-cache-dir -r requirements.txt

# # Ensure gunicorn is installed
# RUN pip install gunicorn

# # Make port 80 available to the world outside this container
# EXPOSE 80

# # Define environment variable
# ENV NAME World

# # Run gunicorn when the container launches
# CMD ["gunicorn", "--bind", "0.0.0.0:80", "social_media_project.wsgi:application"]


# Use an official Python runtime as a parent image
FROM python:3.12.1-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN apt-get update && \
    apt-get install -y apache2 apache2-dev && \
    pip install --no-cache-dir -r requirements.txt && \
    pip install mod_wsgi

# Enable mod_wsgi module
RUN mod_wsgi-express install-module

# Copy Apache configuration file
COPY ./scripts/apache/django.conf /etc/apache2/sites-available/000-default.conf

# Make port 80 available to the world outside this container
EXPOSE 80

# Run Apache when the container launches
CMD ["apache2ctl", "-D", "FOREGROUND"]
