# Use an official Python runtime as a parent image
FROM python:3.12.1-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Ensure gunicorn is installed
RUN pip install gunicorn

# Verify that gunicorn is installed and available in the PATH
RUN echo "Verifying gunicorn installation..-----------------." && \
    gunicorn --version

# Make port 80 available to the world outside this container
EXPOSE 80

# Define environment variable
ENV NAME World

# Run gunicorn when the container launches
CMD ["gunicorn", "--bind", "0.0.0.0:80", "social_media_project.wsgi:application"]
