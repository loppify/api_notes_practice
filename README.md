# Project Name

A REST API backend service designed for note taking app with tags for tasks and authentication

[Live Demo / Swagger UI](https://your-deployment-url.com/docs)

---

## Tech Stack

* **Language:** Python 3.11+
* **Package Manager:** uv
* **Framework:** FastAPI
* **Database & ORM:** PostgreSQL, SQLAlchemy
* **Database Migrations:** Alembic
* **Containerization:** Docker, Docker Compose
* **Validation & Settings:** Pydantic / Pydantic Settings

---

## Features

* Full CRUD operations for tasks. Not full users and tags
* Automated database migrations with Alembic
* Interactive API documentation via Swagger UI
* Fully containerized setup with Docker Compose

---

## Project Structure

```text
.
├── migration/            # Database migration scripts
├── app/
│   ├── api/              # API routes and endpoints
│   ├── dao/              # Database access objects and session setup
│   ├── models/           # SQLAlchemy database models
│   ├── schemas/          # Pydantic validation schemas
│   └── main.py           # Application entry point
├── .env.example          # Template for environment variables
├── alembic.ini           # Alembic configuration
├── docker-compose.yml    # Multi-container orchestration
├── Dockerfile            # App container definition
├── pyproject.toml        # Project configuration and dependencies
├── uv.lock               # Deterministic dependency lockfile
└── README.md

```

---

## Quick Start

### 1. Prerequisites

* [Docker](https://docs.docker.com/get-docker/) and [Docker Compose](https://docs.docker.com/compose/)
* [Git](https://git-scm.com/)

### 2. Clone the Repository

```bash
git clone [https://github.com/username/project-name.git](https://github.com/username/project-name.git)
cd project-name

```

### 3. Environment Variables

Create a `.env` file in the root directory based on `.env.example`:

```bash
cp .env.example .env

```

Example configuration (`.env`):

```env
DB_NAME=postgres
DB_USER=postgres
DB_PASSWORD=password

```

### 4. Run with Docker Compose

Build and start the application and PostgreSQL database:

```bash
docker compose up --build -d

```

Apply database migrations:

```bash
docker compose exec app alembic upgrade head

```

The API service will be available at: `http://localhost:8000`

---

## API Documentation

Once the server is running, you can explore and test the endpoints directly:

* **Interactive Swagger UI:** `http://localhost:8000/docs`

---

## Local Development (Without Docker for App)

If you prefer to run PostgreSQL in Docker and the FastAPI app locally:

1. **Start only the database:**
```bash
docker compose up -d postgres

```


2. **Install project dependencies and create the virtual environment:**
```bash
uv sync

```


3. **Update environment variables for local access in `.env`:**
```env
DB_HOST=localhost
DB_PORT=5432

```


4. **Apply database migrations:**
```bash
uv run alembic upgrade head

```


5. **Start the development server with auto-reload:**
```bash
uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

```
