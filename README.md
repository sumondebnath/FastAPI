# FastAPI Installation Guide

A minimal [FastAPI](https://fastapi.tiangolo.com/) project set up with
[uv](https://docs.astral.sh/uv/) and locked to Python 3.14.

The only dependency is `fastapi[standard]`, which already bundles
[Uvicorn](https://www.uvicorn.org/) (the ASGI server), `httpx`, `jinja2`,
`python-multipart`, `email-validator`, and the `fastapi` CLI.

---

## Requirements

- Python **3.14+** (pinned via `.python-version`)
- Either **uv** (recommended) **or** pip

---

## Method 1 — Install with `uv` (recommended)

### 1. Install uv

```bash
# Linux / macOS
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows (PowerShell)
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"

# pipx alternative
pipx install uv
```

Restart your shell (or run `source ~/.bashrc`) afterwards, then verify:

```bash
uv --version
```

### 2. Create the project and install dependencies

This repository is already a uv project, so you only need to sync it:

```bash
# Creates .venv, downloads Python 3.14 if missing, installs from uv.lock
uv sync
```

To add a package later:

```bash
uv add uvicorn[standard]     # add to pyproject.toml + uv.lock
uv remove <package>          # remove it
uv lock --upgrade-package fastapi
```

### 3. Run the server

`uv run` executes inside the project environment, so you never need to
activate anything manually:

```bash
uv run fastapi dev main.py --reload        # with auto-reload
uv run uvicorn main:app --reload           # plain Uvicorn, with auto-reload
```

---

## Method 2 — Install with `pip`

Use this if you prefer a standard virtual environment workflow.

### 1. Create and activate a virtual environment

```bash
python3.14 -m venv .venv
source .venv/bin/activate        # macOS / Linux
# .venv\Scripts\activate         # Windows PowerShell / CMD
```

### 2. Install FastAPI and Uvicorn

Because `pyproject.toml` uses the `uv_build` backend, installing the project
itself is optional — just install the runtime dependencies:

```bash
pip install --upgrade pip
pip install "fastapi[standard]"
```

Or, to install everything from the lockfile-resolved versions:

```bash
pip install fastapi==0.142.2 uvicorn==0.54.0
```

Confirm it worked:

```bash
pip list | grep -E "fastapi|uvicorn"
```

---

## Create the application

Create `main.py` in the project root:

```python
from fastapi import FastAPI

app = FastAPI(title="Installation", version="0.1.0")


@app.get("/")
async def root() -> dict[str, str]:
    return {"message": "Hello from installation!"}


@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}
```

---

## Running the server with Uvicorn

`uvicorn` takes `module:app` (a Python file and a variable name, colon
separated — no `.py`, no quotes needed).

### With the virtual environment activated

```bash
uvicorn main:app --reload
```

### Without activating (uv)

```bash
uv run uvicorn main:app --reload
```

### Useful Uvicorn flags

| Command | What it does |
| --- | --- |
| `uvicorn main:app --reload` | Auto-reload on file changes (development) |
| `uvicorn main:app --host 0.0.0.0 --port 8000` | Listen on all interfaces |
| `uvicorn main:app --workers 4` | Multiple worker processes |
| `uvicorn main:app --log-level debug` | Verbose logs |
| `uvicorn main:app` | Production mode, no reloader |

Make the app importable from anywhere by naming the file `main.py` (module
`main`, variable `app`). If you keep it inside `src/installation/`, the import
string becomes:

```bash
uvicorn installation.main:app --reload
```

### Alternative — the FastAPI CLI

`fastapi[standard]` ships `fastapi`, a Typer-based wrapper around Uvicorn that
adds friendlier defaults:

```bash
uv run fastapi dev main.py --reload           # development, with reloader
uv run fastapi run main.py                    # production-style
```

### Access the app

| URL | Description |
| --- | --- |
| <http://127.0.0.1:8000> | Your API |
| <http://127.0.0.1:8000/docs> | Swagger UI (interactive) |
| <http://127.0.0.1:8000/redoc> | ReDoc |
| <http://127.0.0.1:8000/openapi.json> | OpenAPI schema |

Stop the server with `Ctrl+C`.

---

## Project structure

```
installation/
├── .python-version        # Python 3.14
├── pyproject.toml         # project metadata + dependencies
├── uv.lock                # pinned, reproducible dependency graph
├── README.md
└── src/
    └── installation/
        └── __init__.py    # contains main()
```

---

## Troubleshooting

**`uv: command not found`** — the installer adds `~/.local/bin` to your `PATH`.
Add `export PATH="$HOME/.local/bin:$PATH"` to your shell profile.

**Python 3.14 not found** — uv can install it for you: `uv python install 3.14`.

**`ModuleNotFoundError: No module named 'main'`** — Uvicorn needs the import
string, not the path: `uvicorn main:app`, not `uvicorn main.py`.

**`uvicorn` not found after a pip install** — you skipped the
`fastapi[standard]` extra or the virtual environment is not active. Run
`which uvicorn` to check.

**Port 8000 already in use** — pick another one: `uvicorn main:app --port 8001`.

---

## License

Add your license here.