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
RUN pip install psycopg2-binary gunicorn

# Copy the wait-for-it script into the container
COPY wait-for-it.sh /wait-for-it.sh

# Make the wait-for-it script executable
RUN chmod +x /wait-for-it.sh

# Verify Gunicorn installation
RUN gunicorn --version

# Copy the rest of your application code into the container
COPY . .

# Command to run your application
# CMD ["gunicorn", "--bind", "0.0.0.0:8000", "social_media_project.wsgi:application"]
CMD ["/wait-for-it.sh", "db:5432", "--", "sh", "-c", "python manage.py makemigrations && python manage.py migrate && gunicorn --bind 0.0.0.0:8000 social_media_project.wsgi:application"]