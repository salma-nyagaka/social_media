# Dockerfile
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the dependencies file to the working directory
COPY requirements.txt .

# Install any dependencies
RUN pip install -r requirements.txt

# Copy the content of the local directory to the working directory
COPY . .

# Expose the port the app runs on
EXPOSE 8000

# Define environment variable
ENV NAME World

# Run the application
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "social_media_project.wsgi:application"]
