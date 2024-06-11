<!-- ### README

# Social Media Project

## Table of Contents

- [Introduction](#introduction)
- [System Design](#system-design)
  - [Microservices Architecture](#microservices-architecture)
  - [Communication Protocols](#communication-protocols)
  - [Data Storage Strategies](#data-storage-strategies)
- [Project Setup](#project-setup)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Running the Application](#running-the-application)
  - [Running Tests](#running-tests)
- [API Endpoints](#api-endpoints)
- [ERD Diagram](#erd-diagram)

## Introduction

The Social Media Project is a scalable, real-time notification system for a social media platform. Users can follow each other and receive real-time notifications about new posts, comments, and messages. The project is built using Django Rest Framework and RabbitMQ for asynchronous communication.

## System Design

### Microservices Architecture

The system is designed as a collection of independent microservices that communicate via APIs. The key microservices are:

1. **User Service**: Manages user accounts and profiles.
2. **Post Service**: Handles creation, storage, and retrieval of posts.
3. **Notification Service**: Generates and delivers real-time notifications to users.

Each microservice is responsible for a specific aspect of the application and operates independently. This design allows for easier scaling and maintenance.

### Communication Protocols

The microservices communicate asynchronously using RabbitMQ as the message broker. This ensures efficient and reliable delivery of messages between services.

- **User Service** sends messages to the Notification Service when a user follows another user and when a user registers/creates a new account.
- **Post Service** sends messages to the Notification Service when a new post or comment is created.

### Data Storage Strategies

The data is stored in a PostgreSQL database. Each microservice has its own database schema to maintain separation of concerns. The following strategies are employed:

- **User Service**: Stores user account information and profiles.
- **Post Service**: Stores posts and comments.
- **Notification Service**: Stores notification history and user preferences.

To improve performance and scalability, caching mechanisms are used to reduce database load.

## Project Setup

### Prerequisites

- Python 3.12
- Django 3.2+
- PostgreSQL
- RabbitMQ
- Celery

### Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/salma-nyagaka/social_media.git
   cd social_media_project
   ```

2. **Create a virtual environment**:
   ```bash
   virtualenv venv
   source env/bin/activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure PostgreSQL**
    - **Create a New Role and Database** (optional):
    ```sql
    CREATE ROLE myuser
    ALTER ROLE myuser CREATEDB;
    CREATE DATABASE mydb OWNER myuser;
    ```

    - **Exit PostgreSQL prompt**:
    ```sql
    \q
    ```

6. **Configure environment variables**:
    - Create a `.env` file in the project root and add the following variables. These can be updated depending on your system settings:
   ```env
    export DOMAIN_NAME='http://127.0.0.1:8000'
    export SECRET_KEY="django-insecure-xi@@*gceecx#9^^311qpn6#l-e=ydu!5#9uxjrna5=7fw*ch^^"
    export EMAIL_HOST_USER="salmanyagaka@gmail.com"
    export EMAIL_HOST_PASSWORD="oycj urnx ceiw rexn"
    export DEFAULT_FROM_EMAIL="salmanyagaka@gmail.com"
    export DATABASE_NAME="mydb"
    export DATABASE_USER="mydb"
    export DATABASE_PASSWORD=""
    export DATABASE_HOST="localhost"
    export DATABASE_PORT='5432'
   ```

    - Run source .env to load the environment settings

6. **Apply database migrations**:
   ```bash
   python manage.py migrate
   ```


### Running the Application

1. **Start RabbitMQ**:
   Make sure RabbitMQ is installed and running on your machine. You can download it from the [official website](https://www.rabbitmq.com/download.html) and start it using the appropriate command for your operating system.

2. **Run the Django development server**:
   ```bash
   python manage.py runserver
   ```

3. **Start the Celery worker**:
   ```bash
   celery -A social_media_project worker -l info
   ```

### Running Tests

To run the tests, execute:
```bash
pytest
```

## API Endpoints

Sure! Below is the comprehensive README file with API endpoints displayed in a table format.

### README

# Social Media Project

## Table of Contents

- [Introduction](#introduction)
- [System Design](#system-design)
  - [Microservices Architecture](#microservices-architecture)
  - [Communication Protocols](#communication-protocols)
  - [Data Storage Strategies](#data-storage-strategies)
- [Project Setup](#project-setup)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Running the Application](#running-the-application)
  - [Running Tests](#running-tests)
- [API Endpoints](#api-endpoints)
  - [User Service](#user-service)
  - [Post Service](#post-service)
  - [Notification Service](#notification-service)
- [Contributing](#contributing)
- [License](#license)

## Introduction

The Social Media Project is a scalable, real-time notification system for a social media platform. Users can follow each other and receive real-time notifications about new posts, comments, and messages. The project is built using Django Rest Framework and RabbitMQ for asynchronous communication.

## System Design

### Microservices Architecture

The system is designed as a collection of independent microservices that communicate via APIs. The key microservices are:

1. **User Service**: Manages user accounts and profiles.
2. **Post Service**: Handles creation, storage, and retrieval of posts.
3. **Notification Service**: Generates and delivers real-time notifications to users.

Each microservice is responsible for a specific aspect of the application and operates independently. This design allows for easier scaling and maintenance.

### Communication Protocols

The microservices communicate asynchronously using RabbitMQ as the message broker. This ensures efficient and reliable delivery of messages between services.

- **User Service** sends messages to the Notification Service when a user follows another user.
- **Post Service** sends messages to the Notification Service when a new post or comment is created.

### Data Storage Strategies

The data is stored in a PostgreSQL database. Each microservice has its own database schema to maintain separation of concerns. The following strategies are employed:

- **User Service**: Stores user account information and profiles.
- **Post Service**: Stores posts and comments.
- **Notification Service**: Stores notification history and user preferences.

To improve performance and scalability, caching mechanisms are used to reduce database load.

## Project Setup

### Prerequisites

- Python 3.8+
- Django 3.2+
- PostgreSQL
- RabbitMQ

### Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/social_media_project.git
   cd social_media_project
   ```

2. **Create a virtual environment**:
   ```bash
   python -m venv env
   source env/bin/activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**:
   Create a `.env` file in the project root and add the following variables:
   ```env
   SECRET_KEY=your_secret_key
   DEBUG=True
   DATABASE_URL=postgres://user:password@localhost:5432/social_media_db
   RABBITMQ_URL=amqp://guest:guest@localhost:5672/
   ```

5. **Apply database migrations**:
   ```bash
   python manage.py migrate
   ```

6. **Create a superuser**:
   ```bash
   python manage.py createsuperuser
   ```

### Running the Application

1. **Start RabbitMQ**:
   Ensure RabbitMQ is installed and running on your local machine or a server. The standard port is 5672.

2. **Run the Django development server**:
   ```bash
   python manage.py runserver
   ```

3. **Start the Celery worker**:
   Make sure to configure Celery in your Django project to use RabbitMQ as the broker.
   ```bash
   celery -A social_media_project worker -l info
   ```

### Running Tests

To run the tests, execute:
```bash
pytest
```

## API Endpoints

### User Service

Certainly! Here is the properly formatted table with the given endpoints and descriptions.

### User Service API Endpoints

| Method | Endpoint                          | Description                             |
|--------|-----------------------------------|-----------------------------------------|
| POST   | `{{base_url}}/users/create_user/` | Create a new user.                      |
| POST   | `{{base_url}}/users/login/`       | User login.                             |
| GET    | `{{base_url}}/users/get_current_user/` | Get the current authenticated user.     |
| PATCH  | `{{base_url}}/users/update/<id>/` | Update a specific user.                 |
| GET    | `{{base_url}}/users/all`          | List all active users.                  |
| GET    | `{{base_url}}/users/<id>/`        | Retrieve a specific user.               |
| DELETE | `{{base_url}}/users/delete/<id>/` | Delete a specific user.                 |
| POST   | `{{base_url}}/users/follow/<id>/` | Follow a user.                          |
| POST   | `{{base_url}}/users/unfollow/<id>/` | Unfollow a user.                        |
| GET    | `{{base_url}}/users/followers/<id>/` | List followers of a user.               |


### Post Service API Endpoints

| Method | Endpoint                          | Description                             |
|--------|-----------------------------------|-----------------------------------------|
| POST   | `{{base_url}}/blogs/`             | Create a new post.                      |
| GET    | `{{base_url}}/blogs/<id>/`        | Retrieve a specific post.               |
| GET    | `{{base_url}}/blogs/all/`         | List all posts.                         |
| DELETE | `{{base_url}}/blogs/delete/<id>/` | Delete a specific post.                 |
| PUT    | `{{base_url}}/blogs/update/<id>/` | Update a specific post.                 |
| POST   | `{{base_url}}/blogs/comments/`    | Create a comment on a post.             |
| GET    | `{{base_url}}/blogs/comments/all/` | List all comments.                      |
| GET    | `{{base_url}}/blogs/comments/<id>/` | Retrieve a specific comment.            |
| PUT    | `{{base_url}}/blogs/comments/update/<id>/` | Update a specific comment.              |
| DELETE | `{{base_url}}/blogs/comments/delete/<id>/` | Delete a specific comment.              |

## ERD Diagram -->


Here's the updated system design document with prerequisites and instructions on how to run the Docker setup:

---

# System Design Document

## Overview

This document outlines the chosen microservices architecture, communication protocols, and data storage strategies for our scalable real-time notification system for a social media platform. The system is designed to handle user accounts, posts, and notifications with a focus on scalability, reliability, and real-time delivery.

## Architecture

### Microservices

1. **User Service**: Manages user accounts and authentication.
2. **Post Service**: Handles posts creation, updating, and retrieval.
3. **Notification Service**: Manages notifications for user activities such as new posts, comments, and follows.

### Communication Protocols

- **REST API**: Used for synchronous communication between services.
- **RabbitMQ**: Used for asynchronous communication to handle notifications and real-time updates.

### Data Storage Strategies

- **User Service**: Uses PostgreSQL for relational data storage.
- **Post Service**: Uses PostgreSQL for relational data storage.
- **Notification Service**: Uses Redis for fast access to notification data and PostgreSQL for persistent storage.

## Prerequisites

Before setting up the system, ensure that you have the following prerequisites installed:

- Docker
- Docker Compose
- Git

## Microservices Details

### User Service

- **Database**: PostgreSQL
- **Endpoints**:
  - `/users/` (GET, POST): Retrieve list of users, create a new user.
  - `/users/{id}/` (GET, PUT, DELETE): Retrieve, update, delete a user.

### Post Service

- **Database**: PostgreSQL
- **Endpoints**:
  - `/posts/` (GET, POST): Retrieve list of posts, create a new post.
  - `/posts/{id}/` (GET, PUT, DELETE): Retrieve, update, delete a post.
  - `/posts/{id}/comments/` (GET, POST): Retrieve list of comments for a post, add a comment.

### Notification Service

- **Database**: Redis (for fast access), PostgreSQL (for persistent storage)
- **Endpoints**:
  - `/notifications/` (GET): Retrieve list of notifications for a user.
  - `/notifications/{id}/` (PUT): Mark a notification as read.

## URL, Action Methods, and Descriptions

| URL                         | Action Method | Description                                                |
|-----------------------------|---------------|------------------------------------------------------------|
| `/users/`                   | GET           | Retrieve a list of users                                   |
| `/users/`                   | POST          | Create a new user                                          |
| `/users/{id}/`              | GET           | Retrieve details of a specific user                        |
| `/users/{id}/`              | PUT           | Update details of a specific user                          |
| `/users/{id}/`              | DELETE        | Delete a specific user                                     |
| `/posts/`                   | GET           | Retrieve a list of posts                                   |
| `/posts/`                   | POST          | Create a new post                                          |
| `/posts/{id}/`              | GET           | Retrieve details of a specific post                        |
| `/posts/{id}/`              | PUT           | Update a specific post                                     |
| `/posts/{id}/`              | DELETE        | Delete a specific post                                     |
| `/posts/{id}/comments/`     | GET           | Retrieve a list of comments for a specific post            |
| `/posts/{id}/comments/`     | POST          | Add a comment to a specific post                           |
| `/notifications/`           | GET           | Retrieve a list of notifications for the authenticated user|
| `/notifications/{id}/`      | PUT           | Mark a notification as read                                |

## Communication Flow

1. **User Registration**:
   - The client sends a POST request to the User Service (`/users/`).
   - The User Service creates a new user and returns the user details.

2. **Post Creation**:
   - The client sends a POST request to the Post Service (`/posts/`).
   - The Post Service creates a new post and publishes an event to RabbitMQ.
   - The Notification Service consumes the event and creates notifications for followers of the user who created the post.

3. **Retrieve Notifications**:
   - The client sends a GET request to the Notification Service (`/notifications/`).
   - The Notification Service retrieves the notifications from Redis and returns them to the client.

## Data Models

### User Model

```python
class User(models.Model):
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
```

### Post Model

```python
class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
```

### Notification Model

```python
class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True, blank=True)
    message = models.CharField(max_length=255)
    read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
```

## Running the Docker Setup

### Step 1: Clone the Repository

```sh
git clone https://github.com/yourusername/yourrepository.git
cd yourrepository
```

### Step 2: Build and Run the Docker Containers

```sh
docker-compose up --build
```

This command will build the Docker images and start the containers defined in your `docker-compose.yml` file.

### Step 3: Apply Database Migrations

```sh
docker-compose exec user_service python manage.py migrate
docker-compose exec post_service python manage.py migrate
docker-compose exec notification_service python manage.py migrate
```

### Step 4: Create a Superuser for Django Admin

```sh
docker-compose exec user_service python manage.py createsuperuser
```

Follow the prompts to create a superuser account.

### Step 5: Access the Application

- **User Service**: `http://localhost:8000`
- **Post Service**: `http://localhost:8001`
- **Notification Service**: `http://localhost:8002`

### Step 6: Run Tests (Optional)

```sh
docker-compose exec user_service python manage.py test
docker-compose exec post_service python manage.py test
docker-compose exec notification_service python manage.py test
```
