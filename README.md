[![codecov](https://codecov.io/gh/salma-nyagaka/social_media/graph/badge.svg?token=OCYCVUXSBN)](https://codecov.io/gh/salma-nyagaka/social_media)
## Table of Contents


1. [Introduction](#introduction)
2. [System Design](#system-design)
   - [Microservices Architecture](#microservices-architecture)
   - [Authentication](#authentication)
   - [Communication Protocols](#communication-protocols)
   - [Data Storage Strategies](#data-storage-strategies)
3. [Project Setup](#project-setup)
   - [Prerequisites](#prerequisites)
   - [Installation](#installation)
4. [Running the Application](#running-the-application)
5. [Sentry Configuration](#sentry-configuration)
6. [API Endpoints](#api-endpoints)
   - [User Service API Endpoints](#user-service-api-endpoints)
   - [Post Service API Endpoints](#post-service-api-endpoints)
7. [ERD Diagram](#erd-diagram)
8. [Collection](#collection)


## Introduction

The Social Media Project is a scalable, real-time notification system for a social media platform. Users can follow each other and receive real-time notifications about new posts, comments, and messages. The project is built using Django Rest Framework and RabbitMQ for asynchronous communication.

## System Design

### Microservices Architecture

The system is designed as a collection of independent microservices that communicate via APIs. The key microservices are:

1. **User Service**: Manages user accounts and profiles.
2. **Post Service**: Handles creation, storage, and retrieval of posts.
3. **Notification Service**: Generates and delivers real-time notifications to users.

Each microservice is responsible for a specific aspect of the application and operates independently. This design allows for easier scaling and maintenance.

### Authentication

To secure our endpoints and manage authentication, we  have used JSON Web Tokens (JWT). After logging in, copy the token, select **__Authorization__** on postman,
choose **__Bearer Token__** then paste your **Token**. You can also include it in your environment settings and pass the variable name holding the token


### Communication Protocols

The microservices communicate asynchronously using RabbitMQ as the message broker. This ensures efficient and reliable delivery of messages between services.
The setup in the settings file ensures that your Django application can send emails via the specified SMTP server using the credentials provided.

- **User Service** sends messages to the Notification Service when a user follows another user and send an activation email to the user's account.
- **Post Service** sends messages to the Notification Service when a new post or comment is created.

### Data Storage Strategies

The data is stored in a PostgreSQL database. Each microservice has its own database schema to maintain separation of concerns. The following strategies are employed:

- **User Service**: Stores user account information and profiles.
- **Post Service**: Stores posts and comments.
- **Notification Service**: Stores notification history and user preferences.

To improve performance and scalability, caching mechanisms via the Redis server are used to reduce database load.

## Project Setup

### Prerequisites

- Python 3.12
- Django 3.2+
- PostgreSQL 16
- RabbitMQ
- Celery
- Redis
- Sentry account

### Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/salma-nyagaka/social_media.git
   cd social_media_project
   ```


### Running the Application
1.  **Update .env file**:
   - Update the .env file(Note that this file is not meant to be uploaded. This is for testing purposes) 

2.  **Build and run your Docker**:
   - Used to start up all the services defined in a Docker Compose file, while also building or rebuilding the service images if necessary.

   ```bash
   docker-compose  up --build
   ```


3. **Run the tests**:
   ```bash
   docker-compose run tests
   ```

## Sentry Configuration

To monitor and debug issues in your application, you can integrate Sentry, an error tracking service. Here’s how you can set up Sentry in your Django application:

1. **Update settings.py**:
   - Update the the Sentry DSN in the settings file:


2. **Verify Sentry Integration**:
   - You can test if Sentry is correctly set up by triggering an error in your application and checking if it appears in your Sentry dashboard.

   - You should have something like this incase of an error
     <img width="1506" alt="Screenshot 2024-06-11 at 20 45 33" src="https://github.com/salma-nyagaka/social_media/assets/36000749/bbaaba47-1b08-4c39-9906-a241666d52f0">

   
## API Endpoints
**_Create a `base_url` and a `token` (generated upon login)   in the selected environment that will be used by by our endpoints._**

### User Service API Endpoints

| Method | Endpoint                          | Description                             |
|--------|-----------------------------------|-----------------------------------------|
| POST   | `{{base_url}}/users/create_user/` | Create a new user.                      |
| POST   | `{{base_url}}/users/login/`       | User login to generate a token                             |
| GET    | `{{base_url}}/users/get_current_user/` | Get the current authenticated user.     |
| PATCH  | `{{base_url}}/users/update/<id>/` | Update profile                 |
| GET    | `{{base_url}}/users/all`          | List all active users.                  |
| GET    | `{{base_url}}/users/<id>/`        | Retrieve a specific user.               |
| DELETE | `{{base_url}}/users/delete/<id>/` | Delete own profile               |
| POST   | `{{base_url}}/users/follow/<id>/` | Follow a user.                          |
| POST   | `{{base_url}}/users/unfollow/<id>/` | Unfollow a user.                        |
| GET    | `{{base_url}}/users/followers` | List followers of a user.               |


### Post Service API Endpoints

**__Note__**: Only users that follow the author can receive notifications
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
![sma drawio](https://github.com/salma-nyagaka/social_media/assets/36000749/8a39bb70-0dd4-4f99-9ad1-005b2d0b7a34)

## Collection
[TWIGA.postman_collection.json](https://github.com/user-attachments/files/15793816/TWIGA.postman_collection.json)

