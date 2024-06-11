Here's a table of contents for the provided documentation:

## Table of Contents

1. [Introduction](#introduction)
2. [System Design](#system-design)
   - [Microservices Architecture](#microservices-architecture)
   - [Communication Protocols](#communication-protocols)
   - [Data Storage Strategies](#data-storage-strategies)
3. [Project Setup](#project-setup)
   - [Prerequisites](#prerequisites)
   - [Installation](#installation)
4. [Running the Application](#running-the-application)
5. [API Endpoints](#api-endpoints)
   - [User Service API Endpoints](#user-service-api-endpoints)
   - [Post Service API Endpoints](#post-service-api-endpoints)
6. [ERD Diagram](#erd-diagram)


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

- Python 3.12
- Django 3.2+
- PostgreSQL 16
- RabbitMQ
- Celery

### Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/salma-nyagaka/social_media.git
   cd social_media_project
   ```

### Running the Application
1.  **Build and run your Docker**:
   - Used to start up all the services defined in a Docker Compose file, while also building or rebuilding the service images if necessary.
   ```bash
   docker-compose up --build
   ```


2. **Run the tests**:
   ```bash
   docker-compose run tests
   ```

## API Endpoints
### User Service API Endpoints

| Method | Endpoint                          | Description                             |
|--------|-----------------------------------|-----------------------------------------|
| POST   | `{{base_url}}/users/create_user/` | Create a new user.                      |
| POST   | `{{base_url}}/users/login/`       | User login.                             |
| GET    | `{{base_url}}/users/get_current_user/` | Get the current authenticated user.     |
| PATCH  | `{{base_url}}/users/update/<id>/` | Update profile                 |
| GET    | `{{base_url}}/users/all`          | List all active users.                  |
| GET    | `{{base_url}}/users/<id>/`        | Retrieve a specific user.               |
| DELETE | `{{base_url}}/users/delete/<id>/` | Delete own profile               |
| POST   | `{{base_url}}/users/follow/<id>/` | Follow a user.                          |
| POST   | `{{base_url}}/users/unfollow/<id>/` | Unfollow a user.                        |
| GET    | `{{base_url}}/users/followers` | List followers of a user.               |


### Post Service API Endpoints

| Method | Endpoint                          | Description                             |
|--------|-----------------------------------|-----------------------------------------|
| POST   | `{{base_url}}/blogs/`             | Create a new post.                      |
| GET    | `{{base_url}}/blogs/<id>/`        | Retrieve a specific post.               |
| GET    | `{{base_url}}/blogs/all/`         | List all posts.                         |
| PUT    | `{{base_url}}/blogs/update/<id>/` | Update user's post.                 |
| DELETE | `{{base_url}}/blogs/delete/<id>/` | Delete user's post.                 |
| POST   | `{{base_url}}/blogs/comments/`    | Create a comment on a post.             |
| GET    | `{{base_url}}/blogs/comments/all/` | List all comments.                      |
| GET    | `{{base_url}}/blogs/comments/<id>/` | Retrieve a specific comment.            |
| PUT    | `{{base_url}}/blogs/comments/update/<id>/` | Update a  comment.              |
| DELETE | `{{base_url}}/blogs/comments/delete/<id>/` | Delete a comment.              |

## ERD Diagram