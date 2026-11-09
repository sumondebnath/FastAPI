# FastAPI CRUD API

A [FastAPI](https://fastapi.tiangolo.com/) project managed with
[uv](https://docs.astral.sh/uv/) and locked to Python 3.14.

The API provides:

- Full CRUD for **posts**
- User registration and listing
- **JWT** login with Argon2 password hashing
- PostgreSQL persistence through **SQLAlchemy**
- Automatic Swagger UI / ReDoc documentation

---

## Tech stack

| Component | Version / Library |
| --- | --- |
| Language | Python 3.14 (pinned in `.python-version`) |
| Framework | `fastapi[standard]` 0.142.2 |
| ASGI server | Uvicorn 0.54.0 |
| ORM | SQLAlchemy 2.1.4 (sync engine) |
| Database | PostgreSQL (`psycopg2-binary` driver) |
| Validation | Pydantic 2.x |
| Password hashing | `pwdlib` with Argon2 |
| Tokens | `pyjwt` (HS256) |
| Package manager | uv |

---

## Requirements

- Python **3.14+**
- **uv** (recommended) or pip
- A running **PostgreSQL** server

---

## Getting started

### 1. Install dependencies

This repository is already a uv project, so sync it instead of creating a new one:

```bash
uv sync
```

This creates `.venv`, downloads Python 3.14 if needed, and installs the exact
versions from `uv.lock`.

### 2. Configure the database URL

Create a `.env` file in the project root (it is git-ignored):

```dotenv
DATABASE_URL="postgresql://<user>:<password>@localhost:5432/<database>"
```

For example:

```dotenv
DATABASE_URL="postgresql://sumon:password%40123@localhost:5432/fastapi"
```

> Passwords containing special characters must be URL-encoded, e.g. `@` becomes
> `%40`.

### 3. Create the database and tables

Create the database if it does not exist:

```bash
createdb fastapi
```

The project does **not** create tables automatically — the
`models.Base.metadata.create_all(...)` call in `app/main.py` is commented out.
Create them once with:

```bash
uv run python -c "from app.database import Base, engine; from app import models; Base.metadata.create_all(bind=engine)"
```

This creates the `users` and `posts` tables.

### 4. Run the server

```bash
# FastAPI CLI (development, with auto-reload)
uv run fastapi dev app/main.py

# or plain Uvicorn
uv run uvicorn app.main:app --reload
```

The import string is `app.main:app` — the `app` package, the `main` module,
and the `app` variable inside it.

---

## Access the API

| URL | Description |
| --- | --- |
| <http://127.0.0.1:8000/docs> | Swagger UI (interactive) |
| <http://127.0.0.1:8000/redoc> | ReDoc |
| <http://127.0.0.1:8000/openapi.json> | OpenAPI schema |

Stop the server with `Ctrl+C`.

---

## API endpoints

All routes are mounted under the `/api/v1` prefix.

### Posts

| Method | Path | Description |
| --- | --- | --- |
| `GET` | `/api/v1/posts/` | List all posts |
| `GET` | `/api/v1/posts/{post_id}` | Get a single post |
| `POST` | `/api/v1/posts/` | Create a post |
| `PUT` | `/api/v1/posts/{post_id}` | Update a post |
| `DELETE` | `/api/v1/posts/{post_id}` | Delete a post (204 No Content) |

### Users

| Method | Path | Description |
| --- | --- | --- |
| `GET` | `/api/v1/users/` | List all users |
| `POST` | `/api/v1/users/` | Register a user (201 Created) |

### Authentication

| Method | Path | Description |
| --- | --- | --- |
| `POST` | `/api/v1/auth/login` | Exchange credentials for a JWT |

---

## Example requests

### Create a user

```bash
curl -X POST http://127.0.0.1:8000/api/v1/users/ \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Jane Doe",
    "email": "jane@example.com",
    "password": "supersecret"
  }'
```

### Log in

The login route uses `OAuth2PasswordRequestForm`, so send **form data**. The
`username` field holds the user's email:

```bash
curl -X POST http://127.0.0.1:8000/api/v1/auth/login \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=jane@example.com&password=supersecret"
```

Response:

```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIs...",
  "token_type": "bearer"
}
```

### Create a post

```bash
curl -X POST http://127.0.0.1:8000/api/v1/posts/ \
  -H "Content-Type: application/json" \
  -d '{
    "title": "My first post",
    "content": "Hello from the API!",
    "author": "Jane Doe"
  }'
```

### List posts

```bash
curl http://127.0.0.1:8000/api/v1/posts/
```

### Update a post

```bash
curl -X PUT http://127.0.0.1:8000/api/v1/posts/1 \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Updated title",
    "content": "Updated content",
    "author": "Jane Doe"
  }'
```

### Delete a post

```bash
curl -X DELETE http://127.0.0.1:8000/api/v1/posts/1
```

---

## Data models

### User

| Field | Type | Notes |
| --- | --- | --- |
| `id` | integer | Primary key |
| `name` | string | Required |
| `email` | string | Unique, required |
| `password` | string | Stored as an Argon2 hash |
| `created_at` | timestamp | Server default `now()` |

### Post

| Field | Type | Notes |
| --- | --- | --- |
| `id` | integer | Primary key |
| `title` | string | Required |
| `content` | text | Required |
| `author` | string | Required |

---

## Project structure

```
installation/
├── app/
│   ├── __init__.py
│   ├── main.py             # FastAPI app + router registration
│   ├── database.py         # engine, SessionLocal, Base, get_db()
│   ├── models.py           # SQLAlchemy models (User, Post)
│   ├── schemas.py          # Pydantic request/response models
│   ├── oauth2.py           # JWT creation (HS256)
│   ├── utils.py            # Password hashing / verification
│   └── routers/
│       ├── post.py         # Post CRUD endpoints
│       ├── user.py         # User endpoints
│       └── auth.py         # Login endpoint
├── src/
│   └── installation/
│       └── __init__.py     # `installation` CLI entry point
├── .env                    # DATABASE_URL (git-ignored)
├── .python-version         # Python 3.14
├── pyproject.toml          # metadata + dependencies
├── requirements.txt        # pip-style pinned requirements
├── uv.lock                 # reproducible dependency graph
└── README.md
```

---

## Configuration

| Variable | Required | Description |
| --- | --- | --- |
| `DATABASE_URL` | Yes | SQLAlchemy PostgreSQL connection string |

It is read in `app/database.py` via `python-dotenv`.

---

## Development notes

- The JWT `SECRET_KEY` is currently hard-coded in `app/oauth2.py`. Move it to
  an environment variable before deploying.
- Tokens are issued by `/api/v1/auth/login`, but no route currently *requires*
  a valid token yet. Protected-route dependencies still need to be added.
- Tables are created manually (see step 3). For schema evolution, consider
  adding [Alembic](https://alembic.sqlalchemy.org/) migrations.
- `app/database.py` uses a synchronous engine with `psycopg2`. `asyncpg` is
  installed but not wired up.

---

## Troubleshooting

**`uv: command not found`** — the installer adds `~/.local/bin` to your `PATH`.
Add `export PATH="$HOME/.local/bin:$PATH"` to your shell profile.

**Python 3.14 not found** — uv can install it for you: `uv python install 3.14`.

**`ModuleNotFoundError: No module named 'app'`** — run commands from the
project root and use the import string `app.main:app`, not a file path.

**Database connection refused / authentication failed** — check that
PostgreSQL is running, the database exists, and `DATABASE_URL` is correct
(remember to URL-encode special characters in the password).

**`relation "posts" does not exist`** — the tables were never created. Run the
`create_all` command from step 3.

**Port 8000 already in use** — pick another one:
`uv run uvicorn app.main:app --port 8001`.

---

## License

Add your license here.
