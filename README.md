# 📝 Notes API

> A production-style REST API for a note-taking and task management application, built with **FastAPI, PostgreSQL, SQLAlchemy 2.0, Alembic, and Docker**.

[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?logo=python\&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.1+-009688?logo=fastapi\&logoColor=white)](https://fastapi.tiangolo.com/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16+-4169E1?logo=postgresql\&logoColor=white)](https://www.postgresql.org/)
[![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.0+-D71F00)](https://www.sqlalchemy.org/)
[![Alembic](https://img.shields.io/badge/Alembic-Migrations-6BA81E)](https://alembic.sqlalchemy.org/)
[![Docker](https://img.shields.io/badge/Docker-Compose-2496ED?logo=docker\&logoColor=white)](https://www.docker.com/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

## 🚀 Overview

**Notes API** is a backend service designed for a note-taking application with task management, tags, and user authentication.

The project was built as a practical backend engineering project to explore modern Python API development and demonstrate how the different layers of a real-world application fit together:

* REST API design with **FastAPI**
* Database modeling with **SQLAlchemy 2.0**
* Schema validation with **Pydantic**
* PostgreSQL database integration
* Version-controlled database migrations with **Alembic**
* JWT-based authentication and authorization
* Containerized development with **Docker Compose**
* Dependency management with **uv**
* Interactive API documentation with **Swagger / OpenAPI**

The goal is not just to expose endpoints, but to provide a clean foundation that can be extended into a larger production application.

---

## ✨ Features

### 🔐 Authentication & Authorization

* User authentication using JWT tokens
* Protected API endpoints
* Token-based authorization
* Configuration through environment variables

### 📋 Task Management

* Create tasks
* Retrieve tasks
* Update tasks
* Delete tasks
* Associate tasks with application users

### 🏷️ Tags

* Support for tagging application data
* Structured data models for future extension of tag functionality

### 🗄️ Database

* PostgreSQL as the primary database
* SQLAlchemy 2.0 ORM
* Explicit database models
* Pydantic schemas for request/response validation
* Alembic migrations for version-controlled schema changes

### 🐳 Development & Deployment

* Dockerized application
* Docker Compose development environment
* Reproducible dependency installation with `uv`
* Environment-based configuration
* Automatic API documentation through FastAPI/OpenAPI

---

## 🛠️ Tech Stack

| Technology            | Purpose                           |
| --------------------- | --------------------------------- |
| **Python 3.11+**      | Backend language                  |
| **FastAPI**           | REST API framework                |
| **PostgreSQL**        | Relational database               |
| **SQLAlchemy 2.0**    | ORM / database access             |
| **Alembic**           | Database migrations               |
| **Pydantic**          | Data validation and serialization |
| **Pydantic Settings** | Application configuration         |
| **JWT**               | Authentication                    |
| **Docker**            | Containerization                  |
| **Docker Compose**    | Local service orchestration       |
| **uv**                | Python dependency management      |
| **Swagger / OpenAPI** | Interactive API documentation     |

---

## 🏗️ Architecture

The application follows a layered backend structure designed to keep API routing, business logic, database access, and data validation separated.

```text
┌───────────────────────────┐
│        API Client         │
│   Web / Mobile / Postman  │
└─────────────┬─────────────┘
              │ HTTP / JSON
              ▼
┌───────────────────────────┐
│        FastAPI API        │
│      Routes / Endpoints   │
└─────────────┬─────────────┘
              │
              ▼
┌───────────────────────────┐
│       Pydantic Schemas    │
│ Validation / Serialization│
└─────────────┬─────────────┘
              │
              ▼
┌───────────────────────────┐
│       DAO / DB Layer      │
│    Database Operations    │
└─────────────┬─────────────┘
              │ SQLAlchemy
              ▼
┌───────────────────────────┐
│        PostgreSQL         │
└───────────────────────────┘

        ▲
        │
┌───────┴───────────────────┐
│         Alembic           │
│    Database Migrations    │
└───────────────────────────┘
```

---

## 📁 Project Structure

```text
.
├── app/
│   ├── api/                  # API routes and endpoints
│   ├── dao/                  # Database access layer
│   ├── models/               # SQLAlchemy models
│   ├── schemas/              # Pydantic schemas
│   └── main.py               # FastAPI application entry point
│
├── migration/                # Alembic migration scripts
│
├── .env.example              # Environment variable template
├── .gitignore
├── Dockerfile                # Application container
├── docker-compose.yaml       # Application + PostgreSQL services
├── alembic.ini               # Alembic configuration
├── Makefile                  # Development commands
├── pyproject.toml            # Project metadata and dependencies
├── uv.lock                   # Locked dependency versions
├── LICENSE
└── README.md
```

---

# ⚡ Quick Start

## Prerequisites

Make sure you have the following installed:

* [Docker](https://www.docker.com/)
* Docker Compose
* [Git](https://git-scm.com/)
* [uv](https://docs.astral.sh/uv/) — required for local development outside Docker

---

## 1. Clone the repository

```bash
git clone https://github.com/loppify/api_notes_practice.git
cd api_notes_practice
```

---

## 2. Configure environment variables

Create your local environment file:

```bash
cp .env.example .env
```

Then configure the required database and application settings.

Example:

```env
DB_NAME=postgres
DB_USER=postgres
DB_PASSWORD=password
DB_HOST=postgres
DB_PORT=5432
SECRET_KEY=hex32generatedKey
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=10
```

> **Important:** Never commit your real `.env` file or production secrets to Git.

---

# 🐳 Running with Docker

The easiest way to run the complete application is with Docker Compose.

### Start the application

```bash
docker compose up --build -d
```

### Apply database migrations

```bash
docker compose exec app alembic upgrade head
```

The API will then be available at:

```text
http://localhost:8000
```

---

# 📚 API Documentation

FastAPI automatically generates interactive OpenAPI documentation.

Once the application is running, open:

### Swagger UI

```text
http://localhost:8000/docs
```

### ReDoc

```text
http://localhost:8000/redoc
```

Swagger UI allows you to explore endpoints, inspect request/response schemas, and send requests directly from your browser.

---

# 💻 Local Development

If you prefer to run the FastAPI application directly on your machine while keeping PostgreSQL inside Docker:

### 1. Start PostgreSQL

```bash
docker compose up -d postgres
```

### 2. Install dependencies

```bash
uv sync
```

### 3. Configure the database connection

Update `.env` for local database access:

```env
DB_HOST=localhost
DB_PORT=5432
```

### 4. Run migrations

```bash
uv run alembic upgrade head
```

### 5. Start the development server

```bash
uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at:

```text
http://localhost:8000
```

---

# 🗃️ Database Migrations

Database schema changes are managed using **Alembic**.

Apply all available migrations:

```bash
uv run alembic upgrade head
```

Create a new migration:

```bash
uv run alembic revision --autogenerate -m "describe your change"
```

Rollback the latest migration:

```bash
uv run alembic downgrade -1
```

Using migrations keeps database schema changes reproducible across development and deployment environments.

---

# 🔌 API

The API exposes RESTful endpoints for authentication and task-related operations.

The complete and authoritative API specification is available through the generated Swagger documentation:

```text
GET /docs
```

Example request:

```bash
curl http://localhost:8000/
```

For authenticated endpoints, obtain a JWT through the authentication flow and provide it using the standard Bearer authentication scheme:

```text
Authorization: Bearer <your-token>
```

---

# 🔒 Configuration & Security

Configuration is managed through environment variables rather than hard-coded application values.

Typical configuration includes:

* Database credentials
* Database host and port
* Authentication secrets
* Application environment
* Other runtime configuration

For local development:

```bash
cp .env.example .env
```

For production environments, use your deployment platform's secret/environment-variable management rather than committing credentials to the repository.

---

# 🧪 Development Workflow

A typical development workflow looks like this:

```text
1. Create / modify SQLAlchemy models
              ↓
2. Generate an Alembic migration
              ↓
3. Apply migration to PostgreSQL
              ↓
4. Create / update Pydantic schemas
              ↓
5. Implement API endpoint
              ↓
6. Run the application
              ↓
7. Test through Swagger / API client
```

This project is intentionally structured to make that workflow straightforward and repeatable.

---

# 🗺️ Roadmap

Potential improvements and future work include:

* [ ] Expand automated test coverage
* [ ] Add integration tests with PostgreSQL
* [ ] Improve API error handling
* [ ] Add pagination for collection endpoints
* [ ] Add filtering and sorting
* [ ] Improve tag management
* [ ] Add refresh-token support
* [ ] Add password reset functionality
* [ ] Add rate limiting
* [ ] Add CI/CD with GitHub Actions
* [ ] Add production deployment configuration
* [ ] Add API versioning
* [ ] Add structured application logging
* [ ] Add health/readiness endpoints

---

# 🎯 What This Project Demonstrates

This project demonstrates practical experience with the core components of modern Python backend development:

**API Development**

Building RESTful APIs with FastAPI and OpenAPI.

**Database Engineering**

Designing relational models and working with PostgreSQL through SQLAlchemy 2.0.

**Data Validation**

Using Pydantic schemas to validate incoming requests and serialize API responses.

**Authentication**

Implementing JWT-based authentication and protecting API resources.

**Database Versioning**

Managing schema evolution through Alembic migrations.

**Containerization**

Running the application and PostgreSQL together using Docker Compose.

**Modern Python Tooling**

Using `uv` for fast, reproducible dependency management.

---

# 📌 Project Status

This project is actively structured as a backend engineering practice project and a foundation for further API development.

It is intentionally focused on learning and applying real-world backend patterns rather than building a fully-featured production SaaS application.

---

# 📄 License

This project is licensed under the **MIT License**.

See [LICENSE](LICENSE) for details.

---

## 👤 Author

**loppify**

GitHub: [@loppify](https://github.com/loppify)

---

<p align="center">
  Built with Python, FastAPI, PostgreSQL, SQLAlchemy & Docker.
</p>
