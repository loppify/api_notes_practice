# Notes and Tasks API

A backend practice project built with FastAPI, Pydantic, asynchronous SQLAlchemy, PostgreSQL, and Alembic.

I built this project to understand how request validation, relational models, database migrations, authentication, and authorization fit together. It is a completed learning project with follow-up fixes, rather than an ongoing note-taking product.

[API demo](https://api-notes-practice.onrender.com/) · [Swagger UI](https://api-notes-practice.onrender.com/docs) · [ReDoc](https://api-notes-practice.onrender.com/redoc)

## Implemented features

- User registration and JWT login with expiring access tokens.
- Password hashing during registration and password updates.
- Authenticated task listing filtered by the current user.
- Task and tag creation associated with the authenticated user.
- Ownership checks on task and tag update/delete operations.
- Task-tag relationships and tag usage counts.
- Pydantic request and response models.
- Asynchronous PostgreSQL access through SQLAlchemy and asyncpg.
- Versioned schema changes with Alembic.
- Docker Compose configuration and unit tests for selected model and security behavior.

## Stack

| Area | Tools |
| --- | --- |
| API | Python, FastAPI, Uvicorn |
| Validation | Pydantic, Pydantic Settings |
| Database | PostgreSQL, SQLAlchemy 2, asyncpg |
| Migrations | Alembic |
| Authentication | PyJWT, pwdlib with Argon2 |
| Development | uv, Docker Compose, pytest, Ruff |

## Run locally

Requirements: Python 3.11 or newer, [uv](https://docs.astral.sh/uv/), and Docker with Compose.

```bash
git clone https://github.com/loppify/api_notes_practice.git
cd api_notes_practice
cp .env.example .env
uv sync
```

Fill in `.env`. This example is for a local development database:

```dotenv
DB_NAME=notes
DB_USER=notes
DB_PASSWORD=local_notes_password
DB_HOST=localhost
DB_PORT=5432
SECRET_KEY=replace_with_a_random_secret
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=15
```

Generate a secret and copy its output into `SECRET_KEY`:

```bash
uv run python -c 'import secrets; print(secrets.token_hex(32))'
```

Start the database, apply migrations, and run the API:

```bash
docker compose up -d postgres
uv run alembic upgrade head
uv run uvicorn app.main:app --reload
```

Open [Swagger UI](http://127.0.0.1:8000/docs). The root URL redirects to this documentation.

### Run the complete application in Docker

With the same `.env` configured:

```bash
docker compose up --build
```

Compose overrides the application database host to `postgres`. The current container startup command applies migrations before starting Uvicorn. It uses reload mode and should be treated as a development configuration.

## Try the authenticated workflow

1. Register through `POST /auth/register` with a username, email, and password. The endpoint returns the new user ID.
2. Log in through `POST /auth/login`. Login accepts form-encoded `username` and `password`, not a JSON body.
3. Use Swagger's **Authorize** control or send `Authorization: Bearer <access_token>`.
4. Create a task through `POST /tasks/` and retrieve your list through `GET /tasks/`.
5. Create tags through `POST /tags/` and associate them with a task using `tag_ids`.

Example login:

```bash
curl -X POST http://127.0.0.1:8000/auth/login \
  -H 'Content-Type: application/x-www-form-urlencoded' \
  --data-urlencode 'username=demo' \
  --data-urlencode 'password=replace_with_your_password'
```

Use the generated OpenAPI documentation for the current request fields and response models.

## Database migrations

Apply existing migrations:

```bash
uv run alembic upgrade head
```

After changing a model, generate and inspect a migration:

```bash
uv run alembic revision --autogenerate -m "describe the schema change"
```

Review generated operations before applying them. The repository includes changes to task ownership/nullability and tag ownership and constraints.

## Tests and formatting

After configuring the local `.env`:

```bash
uv run python -m pytest app/tests -q
uv run ruff check .
uv run ruff format --check .
```

The tests cover password hashing, token decoding, tag counts, and selected user-model/database behavior. Database fixtures use SQLite. These are not comprehensive endpoint, PostgreSQL, or authorization tests.

## Repository structure

| Location | Responsibility |
| --- | --- |
| `app/api/` | Authentication, user, task, and tag routes |
| `app/schemas/` | Pydantic request/response models |
| `app/models/` | SQLAlchemy models and relationships |
| `app/dao/` | Queries, mutations, and session handling |
| `app/utils/` | Authentication and utility functions |
| `app/exceptions/` | Application exceptions |
| `app/tests/` | Unit tests and database fixtures |
| `migration/versions/` | Alembic migration history |

## Current limitations

Authorization is implemented for selected workflows, but isolation is not complete across the API. Single-task reads and tag/user read routes are currently unauthenticated; some user-route calls also need alignment with the updated DAO signatures.

Task updates currently clear tags when `tag_ids` is omitted. Tag assignment is looked up by ID without checking tag ownership. These behaviors need correction before using the application for private multi-user data.

The project is useful for examining the implementation and its trade-offs. It does not claim production readiness, complete access-control coverage, or comprehensive automated testing.

## Author

[Rostyslav Tarasov](https://github.com/loppify).

## License

[MIT](LICENSE).
