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

| Method | Endpoint                      | Description                             |
|--------|-------------------------------|-----------------------------------------|
| POST   | /users/                       | Create a new user.                      |
| GET    | /users/                       | List all users.                         |
| GET    | /users/<id>/                  | Retrieve a specific user.               |
| PATCH  | /users/<id>/                  | Update a specific user.                 |
| DELETE | /users/<id>/                  | Delete a specific user.                 |
| POST   | /users/login/                 | User login.                             |
| POST   | /users/follow/<id>/           | Follow a user.                          |
| POST   | /users/unfollow/<id>/         | Unfollow a user.                        |
| GET    | /users/followers/<id>/        | List followers of a user.               |
| GET    | /users/my_profile/            | Get the current authenticated user.     |
| GET    | /email_confirmation/<token>/  | Activate user account.                  |
| GET    | /token/refresh/               | Refresh JWT token.                      |

### Post Service

| Method | Endpoint                       | Description                             |
|--------|--------------------------------|-----------------------------------------|
| POST   | /posts/                        | Create a new post.                      |
| GET    | /posts/                        | List all posts.                         |
| GET    | /posts/<id>/                   | Retrieve a specific post.               |
| PUT    | /posts/<id>/                   | Update a specific post.                 |
| DELETE | /posts/<id>/                   | Delete a specific post.                 |
| POST   | /posts/<post_id>/comments/     | Create a comment on a post.             |
| GET    | /posts/<post_id>/comments/     | List comments on a post.                |

### Notification Service

| Method | Endpoint                       | Description                             |
|--------|--------------------------------|-----------------------------------------|
| GET    | /notifications/                | List all notifications for the current user. |
| POST   | /notifications/read/           | Mark notifications as read.             |

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any bugs or features.

## License

This project is licensed under the MIT License.

---

This comprehensive README file provides an overview of the project, system design details, setup instructions, and API documentation, displayed in a table format for better readability. It serves as a valuable resource for developers and contributors to understand, set up, and extend the application.