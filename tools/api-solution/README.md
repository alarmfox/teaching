# Deploy a Web API Using Docker

## Overview

This guide helps you deploy a sample application using Docker. The application exposes a REST API to manage network devices and uses a Postgres database for storage.

## Objectives

- Learn to run the application locally without Docker.
- Create a Dockerfile and build a Docker image.
- Use Docker Compose for automated deployment.

## Prerequisites

- Basic knowledge of Docker and Docker Compose.
- Python and Flask installed on your machine.
- Docker installed on your machine.

---

## Part 1: Run the Application Locally

### Step 1: Start the Postgres Database
The application uses a Postgres database for storage. Start a Postgres instance using Docker with the following command:

```sh
docker run -e POSTGRES_PASSWORD=postgres -p 5432:5432 postgres:alpine
```

> **Note:** The database password is set to `postgres`. If you change it, update the `.env` file accordingly.

### Step 2: Configure the Python Virtual Environment
Prepare a virtual environment for the Python application:

```sh
python -m venv env
source env/bin/activate
pip install -r requirements.txt
```

### Step 3: Configure the Application
The application reads the database connection string from the `.env` file. The connection string follows the format:

```plaintext
postgresql://user:password@hostname:port/database_name?query_params
```

Update the `.env` file if necessary, especially the `POSTGRES_PASSWORD`.

### Step 4: Run and Test the Application
Start the Flask REST server with the command below:

```sh
flask run
```

Test the API using Postman by importing the provided collection (`DTLab API.postman_collection.json`).

---

## Part 2: Create a Dockerfile

A Dockerfile is required to build a Docker image for the application. It typically contains the following sections:

1. **FROM Directive**: Specifies the base image (e.g., Python environment).
2. **COPY Directive**: Copies source code into the image.
3. **ENTRYPOINT Directive**: Specifies the command to start the application.

---

## Part 3: Build and Run the Docker Image

### Step 1: Build the Docker Image
Run the following command to build the Docker image:

```sh
docker build -t <image_name> .
```

### Step 2: Run the Docker Image
Execute the built image with the following command:

```sh
docker run -p 5000:5000 -e DB_URI=postgresql://postgres:postgres@localhost:5432/postgres?sslmode=disable <image_name>
```

---

## Part 4: Automate Deployment with Docker Compose

### Why Docker Compose?
Manually deploying multiple services with Docker can be time-consuming and error-prone. Docker Compose automates the deployment process using a `docker-compose.yml` file.

### Example Configuration
Below is an example structure for your application in the `docker-compose.yml` file:

```yaml
app:
    build:
        context: .
    environment:
        - DB_URI=postgresql://postgres:postgres@db:5432/postgres?sslmode=disable
    depends_on:
        - db

db:
    image: postgres:alpine
    environment:
        POSTGRES_PASSWORD: postgres
    ports:
        - "5432:5432"
```

### Step 1: Deploy Using Docker Compose
Run the following command to deploy the application and database:

```sh
docker-compose up
```

---

## Summary

- You learned how to run the application locally.
- You created and built a Docker image.
- You automated deployment using Docker Compose.

For further questions or issues, refer to the official documentation:
- [Flask Documentation](https://flask.palletsprojects.com/)
- [Postgres Documentation](https://www.postgresql.org/docs/)
- [Docker Documentation](https://docs.docker.com/)
- [Docker Compose Documentation](https://docs.docker.com/compose/)

